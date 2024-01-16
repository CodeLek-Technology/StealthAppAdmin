from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile")
    phone_no = models.CharField(max_length = 13, unique= True, blank= True, null= True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return "{}".format(self.username)