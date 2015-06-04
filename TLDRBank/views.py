from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from .forms import TransferForm
from accounts import models, exceptions
from .facade import transfer as accountTransfer
from decimal import Decimal
from django.contrib.auth.models import User





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
            amount = form.cleaned_data['amount']
            try:
                trans = accountTransfer(source=source, destination=destination, amount=amount, user=user)
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
