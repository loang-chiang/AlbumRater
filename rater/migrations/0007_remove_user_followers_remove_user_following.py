# Generated by Django 5.0.4 on 2024-05-21 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rater', '0006_rating_likes_user_liked_ratings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
    ]
