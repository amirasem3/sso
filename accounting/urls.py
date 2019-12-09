from django.urls import path, include

from accounting.views import *

urlpatterns = [

    path('start_login_view', start_login_view, name='start_login_view'),
    path('login_view', login_view, name='login_view'),
    path('check_code_validity', check_code_validity, name='check_code_validity'),
    path('rest-auth/', include('rest_auth.urls')),
    path('api/', include('accounting.api.urls')),
]
