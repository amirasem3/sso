from django.urls import path, include


from accounting.api.views import *

urlpatterns = [

    path('check_verify_phone', check_verify_phone, name='check_verify_phone'),
    path('auth', auth, name='auth'),
    path('check_bibot_response', check_bibot_response, name='check_bibot_response'),
    path('login_view', login_view, name='login_view'),
    path('verify_email', verify_email, name='verify_email'),
    path('sign_up_view', sign_up_view, name='sign_up_view'),
    path('forgot_password', forgot_password, name='forgot_password'),

    path('get_user_info/', ProfileViewSet.as_view()),

    path('hello', ApiEndpoint.as_view()),
    path('secret', secret_page, name='secret')
]
