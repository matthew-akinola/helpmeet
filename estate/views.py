from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Authentication.models import Profile

from .models import Estate
from .serializers import (CreateEstateSerializer, EstateSerializer,
                          JoinEstateSerializer)

# Create your views here.


class EstateViewSet(ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Estate.objects.all()
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.request.method in [ 'POST' , 'PUT']:
            return CreateEstateSerializer
        return EstateSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(EstateSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)


class JoinEstate(GenericAPIView):
    serializer_class = JoinEstateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = JoinEstateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        link = serializer.validated_data.get('link', None)
        code = serializer.validated_data.get('code', None)
        address = serializer.validated_data.get('address', None)

        if link:
            # ? Given that the link is in this format 'http://www.safemeet.com/join2983404913'
            code = link.split('/')[3].strip('join')

        estate_obj = get_object_or_404(Estate, public_id=code)

        profile, created = Profile.objects.get_or_create(
            user=request.user, estate=estate_obj, house_address=address)
        
        if profile:
            return Response({'detail': f'Already a Member of {estate_obj.name}'})
        

        return Response({'detail': f'Welcome to {estate_obj.name}'}, status=status.HTTP_200_OK)


class RegisterManager(CreateAPIView):
    {}.values()
    pass
