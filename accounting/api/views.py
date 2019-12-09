from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.crypto import random
from rest_framework.decorators import api_view
import rest_auth.views
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from rest_framework import viewsets

from accounting.models import Profile, PendingAccount

from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required

from rest_framework import permissions
from oauth2_provider.contrib.rest_framework import TokenHasScope

import random
import string

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
import requests

from accounting.models import User


# Sfrom panel.models import EmailTasks


def check_bibot_response(request):
    if request.POST.get('bibot-response') is not None:
        if request.POST.get('bibot-response') != '':
            r = requests.post('https://api.bibot.ir/api1/siteverify/', data={
                'secretkey': '8a92e433df605a0a24e03a182db4d605',
                'response': request.POST['bibot-response']
            })
            print(r.json())
            if r.json()['success']:
                return True
            else:
                messages.error(request, 'کپچا به درستی حل نشده است!')
                return False
        else:
            messages.error(request, 'کپچا به درستی حل نشده است!')
            return False
    return False


def login_view(request):
    if request.method == 'POST':
        if check_bibot_response(request):
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user and user.verified:
                login(request, user)
                return redirect('/panel/')
            elif not user:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است!')
            else:
                messages.error(request, 'لطفا حساب خود را فعال کنید!')

    return render(request, 'login.html')


@api_view(['GET'])
def verify_email(request):
    if User.objects.filter(username=request.GET['email'], EmailVerificationCode=request.GET['code']).count() > 0:
        user = User.objects.get(username=request.GET['email'])
        user.verified = True
        user.emailVerified = True
        user.save()
        if request.user and request.user.is_authenticated:
            logout(request)
        login(request, user)
        return True
    return False


def sign_up_view(request):
    if request.method == 'POST':
        if check_bibot_response(request):
            user = User.objects.filter(username=request.POST['email']).first()
            if user:
                if user.verified:
                    messages.error(request, 'حساب کاربری شما فعال می‌باشد!')
                return HttpResponse(True)
            # return render(request, 'sign_up.html')
            else:
                user.set_password(request.POST['password'])
                user.EmailVerificationCode = ''.join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(80))
                user.save()
                return HttpResponse(True)
        # return render(request, 'activation_email_sent.html')
        else:
            messages.error(request, 'حساب کاربری موجود نیست! با پشتیبانی در ارتباط باشید.')
            return HttpResponse(True)
    # return render(request, 'sign_up.html')
    # return render(request, 'sign_up.html')
    return HttpResponse(True)


def forgot_password(request):
    if request.method == 'POST':
        if check_bibot_response(request):
            user = User.objects.filter(username=request.POST['email']).first()
            if user:
                if user.verified:
                    user.EmailVerificationCode = ''.join(
                        random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(80))
                    user.save()
                    return render(request, 'activation_email_sent.html', context={'forget_pass': True})
                else:
                    messages.error(request, 'فرایند ثبت‌نام تکمیل نشده است!')
                    return render(request, 'sign_up.html')
            else:
                messages.error(request, 'کاربری با این شماره موجود نیست!')
                return render(request, 'forgot_password.html')
    return render(request, 'forgot_password.html')


@api_view(['GET', 'POST', 'OPTIONS'])
def auth(request):
    params = request.query_params
    phone = params['phone']
    user = request.user
    password = params['pass']

    if user.is_authenticated:
        return HttpResponse(True)
        # token = random.randint(1001, 10000)
        # return Response({"loggedin": True, 'token': token})
    user = authenticate(request, username=phone, password=password)
    profile = Profile.objects.filter(user=user).first()
    if user and profile and profile.phone_verified:
        login(request, user)
        token = random.randint(1001, 10000)
        return HttpResponse(True)
    else:
        messages.error(request, 'نام کاربری یا رمز عبور اشتباه است!')
    return HttpResponse(False)


def reset_pass(request):
    if verify_email(request):
        return render(request, 'update_password.html')
    return redirect('/')


@api_view(['GET'])
def check_verify_phone(request):
    params = request.query_params
    phone = params['phone']
    code = int(params['code'])
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if user.is_authenticated():
        HttpResponse(True)
    if not profile:
        return HttpResponse(False)

    if not profile.phone_verified:
        if PendingAccount.objects.filter(phone=phone, verification_code=code).count():
            profile.phone_verified = True
            profile.save()
            PendingAccount.objects.filter(phone=phone).delete()
            return HttpResponse(True)
        else:
            HttpResponse(True)
    else:
        HttpResponse(True)


@api_view(['GET', 'POST'])
def verify_phone(request):
    params = request.query_params
    phone = params['phone']
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if user.is_authenticated():
        pass
    elif not profile:
        profile = Profile.objects.create(user=user)
    if not profile.phone_verified:
        rand = random.randint(1001, 10000)
        if PendingAccount.objects.filter(phone=phone).count() < 10:
            PendingAccount.objects.create(phone=phone, verification_code=rand)
        else:
            messages.error(request, 'many attempts')

    return render(request, 'auth_page.html')


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        return HttpResponse('Hello, OAuth2!\n' + str(current_user))


class ProfileViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['read']

    def get_user_obj(self, user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        profile = self.get_user_obj(request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @classmethod
    def get_extra_actions(cls):
        return []


@login_required()
def secret_page(request, *args, **kwargs):
    current_user = request.user
    return HttpResponse('Secret contents!\n' + str(current_user), status=200)
