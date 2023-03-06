import uuid

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

from utils.estate_code_generator import generate_short_id

# Create your models here.


class Estate(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    name = models.CharField(max_length=200, unique=True, blank=False)
    profile_image = models.ImageField(
        upload_to="estate/", null=True, blank=True)
    location = models.CharField(max_length=500)
    country = CountryField()
    public_id = models.CharField(
        max_length=15, default=generate_short_id, unique=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"
