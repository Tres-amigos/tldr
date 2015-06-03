from django import forms
from accounts import models


class AccountModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class TransferForm(forms.Form):
    source = AccountModelChoiceField(queryset=None)
    destination = AccountModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = models.Account.active.filter(primary_user=user)
        self.fields['destination'].queryset = models.Account.active.filter(primary_user=user)

class CreateAccountForm(forms.Form):
    account_name = forms.CharField(label='Account name', max_length=100)
