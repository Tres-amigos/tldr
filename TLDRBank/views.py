import calendar
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from .forms import TransferForm, CreateAccountForm
from accounts import models, exceptions
from .facade import transfer as accountTransfer
from wkhtmltopdf.views import PDFTemplateResponse
from django.views import generic

from TLDRBank import models as bankmodel


# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'text': '',
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




@login_required(login_url='/account/login')
def transferList(request):
    transfers = models.Transfer.objects.filter(user=request.user)
    return render(request, 'transfer_list.html', {'transfers': transfers})


@login_required(login_url='/account/login')
def MyPDFView(request):

    from datetime import date, datetime, timedelta
    today = datetime.today()
    this_first = date(today.year, today.month, 1)
    prev_end = this_first - timedelta(days=1)
    prev_first = date(prev_end.year, prev_end.month, 1)
    dates = prev_first, prev_end


    transfers = models.Transfer.objects.filter(user=request.user).exclude(date_created__gte=dates[1])\
        .filter(date_created__gte=dates[0])

    active_accounts = models.Account.active.filter(primary_user=request.user)

    total_balance = 0
    for account in active_accounts:
        total_balance += account.balance


    context = {'customername': request.user.email, 'transfers': transfers, 'month': calendar.month_name[prev_end.month],
               'year': today.year, 'totalbalance': total_balance}
    response = PDFTemplateResponse(request=request,
                                   template='pdf.html',
                                   filename=("bankstatement-%s.pdf" % calendar.month_name[prev_end.month]),
                                   context=context,
                                   show_content_in_browser=False,
                                   )
    return response