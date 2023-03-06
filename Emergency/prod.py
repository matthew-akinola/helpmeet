import os

import dj_database_url

from .settings import *

SECRET_KEY = config('SECRET_KEY')

DEBUG = config("DEBUG", False)

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

DATABASES = {"default": dj_database_url.config()}
# DATABASES = {
#     "default": dj_database_url.parse(
#         config("RAILWAY_DB_URL", ""),
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }


DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUD_NAME", ""),
    "API_KEY": config("CLOUD_API_KEY", ""),
    "API_SECRET": config("CLOUD_API_SECRET", ""),
}




SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis-13115.c261.us-east-1-4.ec2.cloud.redislabs.com", 13115)],
            "password": "",
            # "db": 0,
        },
    },
}


CELERY_BROKER_URL = REDIS_URL


EMAIL_PORT = "443"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
