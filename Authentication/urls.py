from dj_rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


urlpatterns = [
    path("register/", CustomRegisterView.as_view()),
    path("login/google/", GoogleLogin.as_view(), name="google-rest"),
   
] 


# dj_rest_auth_urls


urlpatterns += [
    # URLs that do not require a session or valid token
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
]

if getattr(settings, "REST_USE_JWT", False):
    from dj_rest_auth.jwt_auth import get_refresh_view
    from rest_framework_simplejwt.views import TokenVerifyView

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]
