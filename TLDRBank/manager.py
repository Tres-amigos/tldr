from django.db import models
from django.db import transaction
from accounts import exceptions



class PostingManager(models.Manager):
    """
    Custom manager to provide a new 'create' method to create a new transfer.

    Apparently, finance people refer to "posting a transaction"; hence why this
    """

    def create(self, source, destination, amount, parent=None,
               user=None, merchant_reference=None, description=None):
        # Write out transfer (which involves multiple writes).  We use a
        # database transaction to ensure that all get written out correctly.
        self.verify_transfer(source, destination, amount, user)

        with transaction.atomic():

            transfer = self.get_queryset().create(
                source=source,
                destination=destination,
                amount=amount,
                parent=parent,
                user=user,
                merchant_reference=merchant_reference,
                description=description
            )

            # Create transaction records for audit trail
            transfer.transactions.create(
                account=source, amount=-amount)
            transfer.transactions.create(
                account=destination, amount=amount)
            # Update the cached balances on the accounts
            source.save()
            destination.save()
            return self._wrap(transfer)

    def _wrap(self, obj):
        # Dumb method that is here only so that it can be mocked to test the
        # transaction behaviour.
        return obj

    def verify_transfer(self, source, destination, amount, user=None):
        """
        Test whether the proposed transaction is permitted.  Raise an exception
        if not.
        """
        if amount <= 0:
            raise exceptions.InvalidAmount("Debits must use a positive amount")
        if not source.is_open():
            raise exceptions.ClosedAccount("Source account has been closed")
        if not source.can_be_authorised_by(user):
            raise exceptions.AccountException(
                "This user is not authorised to make transfers from "
                "this account")
        if not destination.is_open():
            raise exceptions.ClosedAccount(
                "Destination account has been closed")
        if not source.is_debit_permitted(amount):
            msg = "Unable to debit %.2f from account #%d:"
            raise exceptions.InsufficientFunds(
                msg % (amount, source.id))