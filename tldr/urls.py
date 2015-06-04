"""tldr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from TLDRBank import views

urlpatterns = [
    url(r'^$',  views.index, name='index'),
    url(r'^accounts/profile/', views.accounts, name='profile'),
    url(r'^accounts/transfer/', views.transfer, name='transfer'),
    url(r'^accounts/create/', views.createAccount, name='create_account'),
    url(r'^accounts/transferlist/', views.transferList, name='transferlist'),

    url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
]