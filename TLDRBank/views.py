from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from .forms import TransferForm, CreateAccountForm
from accounts import models, exceptions
from .facade import transfer as accountTransfer
from decimal import Decimal
from django.contrib.auth.models import User
import datetime




# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'text': 'Hello World!',
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/accounts/login/')
def accounts(request):
    template = loader.get_template('accounts.html')
    active_accounts = models.Account.active.filter(primary_user=request.user)

    context = RequestContext(request, {
        'active_accounts': active_accounts,
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/accounts/login/')
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.user, request.POST)
        text = 'Failed the transfer'
        if form.is_valid():
            user = request.user
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']

            try:
                trans = accountTransfer(source=source, destination=destination, amount=Decimal('10.00'), user=user)
                text = 'Successful transfer'
            except exceptions.AccountException as e:
                text = 'Failed the transfer: %s' % e

        template = loader.get_template('index.html')
        context = RequestContext(request, {
            'text': text,
        })
        return HttpResponse(template.render(context))
    else:
        form = TransferForm(request.user)
        return render(request, 'transfer.html', {'form': form})


@login_required(login_url='/accounts/login')
def createAccount(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        text = 'Creation of account has failed'
        if form.is_valid():
            account_name = form.cleaned_data['account_name']
            user = request.user
            user_account = models.Account.objects.create(primary_user=user, name=account_name)
            text = 'Successful creation of account.'

        template = loader.get_template('index.html')
        context = RequestContext(request, {
            'text': text,
        })
        return HttpResponse(template.render(context))
    else:
        form = CreateAccountForm()
        return render(request, 'new_account.html', {'form': form})
