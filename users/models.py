from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import io

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []