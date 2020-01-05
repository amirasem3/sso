from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from accounting.models import *
from panel.forms import *


@login_required
def panel(request):
    if request.method == 'GET':
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        return render(request, 'panel.html', {"profile": profile})
    else:
#         post request
        pass
#     reload the inputs to profile
#         todo read inputs and add image inputs to template


def get_profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    if request.method == 'GET':
        if profile:
            print("before from creation ***")
            form = ProfileForm(instance=profile)
            print("after from creation ***")

            return render(request, 'profile.html', {'form': form, 'profile': profile})
        else:
            form = ProfileForm(instance=Profile())
            return render(request, 'profile.html', {'form': form})

    else:
        form = ProfileForm(request.POST, instance=profile)
        print(form.is_valid(), "**In post **")
        if form.is_valid():
            # save image

            form.save()



        return render(request, 'profile.html', {'form': form, 'profile': profile})

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
