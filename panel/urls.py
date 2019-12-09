from django.urls import path

from panel.views import *

urlpatterns = [
    path('', panel, name='panel'),
    path('get_profile', get_profile, name='get_profile'),
]
