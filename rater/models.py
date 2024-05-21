from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.db import models

# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    saved_albums = models.ManyToManyField('Album', related_name='album_saved_by', symmetrical=False, blank=True)
    liked_ratings = models.ManyToManyField('Rating', related_name='liked_by', symmetrical=False, blank=True)
    ratings = models.ManyToManyField('Rating', related_name='rated_by', symmetrical=False, blank=True)

class Album(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    name = models.CharField(max_length=1000)
    img = models.CharField(max_length=1000)
    release = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} with id {self.id}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_creator')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    likes = models.IntegerField() 

    def __str__(self):
        return f"{self.user} gave {self.rating} stars to {self.album}"