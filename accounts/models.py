from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.conf import settings

class User(AbstractUser):
    nickname=models.CharField(max_length=100)
    # img=models.ImageField(upload_to='',blank=True)
    image=models.CharField(max_length=200,null=True)
    profile_content=models.TextField(blank=True)


