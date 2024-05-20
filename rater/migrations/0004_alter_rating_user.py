# Generated by Django 5.0.4 on 2024-05-20 03:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rater', '0003_album_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
