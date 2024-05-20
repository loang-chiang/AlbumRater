from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.db import models

# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    followers = models.ManyToManyField('self', related_name='is_following', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    saved_albums = models.ManyToManyField('Album', related_name='saved_by', symmetrical=False, blank=True)

class Album(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name} with id {self.id}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_creator')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user} gave {self.rating} stars to {self.album}"