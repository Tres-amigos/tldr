from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'text': 'Hello World!',
    })
    return HttpResponse(template.render(context))



@login_required(login_url='/login/')
def account(request):
    template = loader.get_template('account.html')
    context = RequestContext(request, {
        'text': 'Hello World!',
    })
    return HttpResponse(template.render(context))