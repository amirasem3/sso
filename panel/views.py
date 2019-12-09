from django.http import HttpResponse
from django.shortcuts import render

from accounting.models import *
from panel.forms import *


def panel(request):
    return render(request, 'panel.html')


def get_profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if request.method == 'GET':
        if profile:
            print("before from creation ***")
            form = ProfileForm(instance=profile)
            print("after from creation ***")

            return render(request, 'profile.html', {'form': form})
        else:
            form = ProfileForm(instance=Profile())
            return render(request, 'profile.html', {'form': form})

    else:
        form = ProfileForm(request.POST,instance=profile)
        print(form.is_valid(),"**In post **")
        if form.is_valid():
            form.save()
        return render(request, 'profile.html', {'form': form})






# def sign_up(request):
#     user = request.user
#     if not user.is_authenticated:
#         profile=Profile.objects.(user=user).first()
#         if profile:
#             form=ProfileForm(instance=profile)
#             print(form,"****")
#
#
#     return render(request, 'panel.html')
