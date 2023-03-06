from urllib.parse import unquote

from dj_rest_auth.registration.serializers import (RegisterSerializer,
                                                   SocialLoginSerializer)
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

# For Google Login


class CustomSocialLoginSerializer(SocialLoginSerializer):
    access_token = None
    id_token = None

    def validate(self, attrs):
        # update the received code to a proper format. so it doesn't throw error.

        attrs["code"] = unquote(attrs.get("code"))

        return super().validate(attrs)


class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove username from the login


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    password2 = None
    is_manager = serializers.BooleanField(required=False)

    def validate(self, data):
        return data
    
    def custom_signup(self, request, user):
        user_obj = get_user_model().objects.get(email=user)
        user_obj.is_manager = bool(request.data.get("is_manager", False))
        user_obj.save()

        pass

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ["name", "email","date_joined"]
    
    def get_name(self, user):
        return user.get_full_name()

