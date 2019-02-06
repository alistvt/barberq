from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Barbery(models.Model):
    user = models.OneToOneField(User, related_name='barbery', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000, unique=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    
