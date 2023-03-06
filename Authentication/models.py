import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from estate.models import Estate

from .managers import CustomUserManager


# Create your models here.
class User(AbstractUser):

    username = None
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_manager = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Profile (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.OneToOneField(Estate, on_delete=models.CASCADE)
    house_address = models.CharField(max_length=500)
