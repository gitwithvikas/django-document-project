from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    aadhar_card = models.ImageField(upload_to='documents/', null=True, blank=True)
    pan_card = models.ImageField(upload_to='documents/', null=True, blank=True)
    voter_id_proof = models.ImageField(upload_to='documents/', null=True, blank=True)
    marksheet = models.ImageField(upload_to='documents/', null=True, blank=True)
