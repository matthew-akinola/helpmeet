from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from Authentication.serializers import UserSerializer

from .models import Estate


class CreateEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = ('name', 'location', 'country')

    def save(self, **kwargs):
        user = self.context.get('user')
        if not user.is_manager:
            raise serializers.ValidationError(
                _("Only managers can create Estate Profile"))

        return super().save(manager=user, **kwargs)


class EstateSerializer(serializers.ModelSerializer):
    manager = UserSerializer()
    class Meta:
        model = Estate
        fields = ['id', 'public_id', 'name',
                  'profile_image', 'location', 'country', 'manager']


class JoinEstateSerializer(serializers.Serializer):
    link = serializers.URLField(required=False)
    code = serializers.CharField(required=False)
    address = serializers.CharField(required=False) 
