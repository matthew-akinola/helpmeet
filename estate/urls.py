from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EstateViewSet, JoinEstate

router = DefaultRouter()
router.register('', EstateViewSet, basename='estate')


urlpatterns = [
    path("join/", JoinEstate.as_view(), name="")
] + router.urls
