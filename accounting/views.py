from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import random
import urllib.parse as urlparse
from urllib.parse import parse_qs
from accounting.api.views import check_bibot_response
from accounting.models import *
from panel.forms import EnteranceForm

import urllib

enterance_field_types = ['CharField', 'TextField', 'IntegerField', 'BooleanField',
                         'ImageField', 'EmailField']

next_logged_in_url = '/o/applications/'


def login_view(request):
    # next_url_outh2 = request.GET['next']
    # client_id = request.GET['client_id']
    # scope = request.GET['scope']
    # redirect_uri = request.GET['redirect_uri']
    # authorize_url = '?next=' + next_url_outh2 + "&" + 'client_id=' + client_id + '&' + 'scope=' + scope + '&' + 'redirect_uri=' + redirect_uri
    # authorize_url=request.META['QUERY_STRING']

    if request.method == 'POST':
        authorize_url = request.META['QUERY_STRING']

        print('*********1********')
        user = authenticate(request, username=request.POST['phone'], password=request.POST['password'])
        print('*********user********', user)

        if user is not None:
            login(request, user)
            return redirect(urllib.parse.unquote(authorize_url.replace('next=', '')))
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است!')
    form = EnteranceForm(fields_name=["phone", "password"], fields_type=['CharField', 'CharField'])
    return render(request, 'auth_page.html', context={"form": form, 'next_url': '/auth/login_view'})


def start_login_view(request):
    # next_url_outh2 = request.GET['next']
    # print("**********next total***********",next_url_outh2)
    # authorize_url='?next='+next_url_outh2
    # # client_id = request.GET['client_id']
    # scope = request.GET['scope']
    # redirect_uri = request.GET['redirect_uri']
    # authorize_url='?next='+next_url_outh2 + "&" + 'client_id=' + client_id + '&' + 'scope=' + scope + '&' + 'redirect_uri=' + redirect_uri
    authorize_url = request.META['QUERY_STRING']
    print(authorize_url)
    if request.user.is_authenticated:
        return redirect(urllib.parse.unquote(authorize_url.replace('next=', '').replace('authorize/', 'authorize')))
    if request.method == 'POST':
        print("**********4444***********")

        phone = request.POST['phone']
        user = User.objects.filter(username=phone).first()
        profile = Profile.objects.filter(phone=phone).first()
        if not user:
            profile = Profile.objects.create(user=User.objects.create_user(username=phone), phone=phone)
            return verify_phone_view(request, phone, authorize_url)
        if not profile.phone_verified:
            return verify_phone_view(request, phone, authorize_url)
        form = EnteranceForm(fields_name=["phone", "password"], fields_type=['CharField', 'CharField'])
        form.initial["phone"] = phone

        return render(request, 'auth_page.html',
                      context={"form": form, 'next_url': '/auth/login_view' + '?' + authorize_url})

    else:
        form = EnteranceForm(fields_name=["phone"], fields_type=['CharField'])

        return render(request, 'auth_page.html',
                      context={"form": form, 'next_url': '/auth/start_login_view' + '?' + authorize_url})


def verify_phone_view(request, phone, authorize_url):
    user = request.user
    if user.is_authenticated:
        return redirect(urllib.parse.unquote(authorize_url))

    rand = random.randint(1001, 10000)
    r = requests.get(
        'http://ip.sms.ir/SendMessage.ashx?user=9366697781&pass=zMUcxrE83uQWtCK&text=کد تایید شما: ' +
        str(rand) + '&to=' + phone + '&lineNo=50002015068678'
    )
    if PendingAccount.objects.filter(phone=phone).count() < 10:
        PendingAccount.objects.create(phone=phone, verification_code=rand)
    else:
        messages.error(request, 'many attempts')

    form = EnteranceForm(fields_name=["phone", "code", "set_password"],
                         fields_type=['CharField', 'CharField', 'CharField'])
    form.initial["phone"] = phone

    return render(request, 'auth_page.html',
                  context={"form": form, 'next_url': "/auth/check_code_validity" + '?' + authorize_url})


def check_code_validity(request):
    # next_url_outh2 = request.GET['next']
    # client_id = request.GET['client_id']
    # scope = request.GET['scope']
    # redirect_uri = request.GET['redirect_uri']
    # authorize_url = '?next=' + next_url_outh2 + "&" + 'client_id=' + client_id + '&' + 'scope=' + scope + '&' + 'redirect_uri=' + redirect_uri
    authorize_url = request.META['QUERY_STRING']

    if request.method == 'POST':

        phone = request.POST['phone']
        code = request.POST['code']
        password = request.POST['set_password']
        print(password)
        user = User.objects.filter(username=phone).first()
        profile = Profile.objects.filter(user=user).first()
        if PendingAccount.objects.filter(phone=phone, verification_code=code).count():
            profile.phone_verified = True
            profile.save()
            PendingAccount.objects.filter(phone=phone).delete()
            user.set_password(password)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(urllib.parse.unquote(authorize_url.replace('next=', '')))

        else:
            messages.error(request, 'کد اشتباه است!')
            form = EnteranceForm(fields_name=["phone", "code", "set_password"],
                                 fields_type=['CharField', 'CharField', 'CharField'])
            form.initial["phone"] = phone
            return render(request, 'auth_page.html', context={"form": form, 'next_url': "/auth/check_code_validity"})
