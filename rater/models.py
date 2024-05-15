from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name='is_following', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    saved_albums = models.SomeField()