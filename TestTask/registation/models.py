from django.db import models


class ProfileModel(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    photo_profile = models.ImageField(upload_to='images/')