# Generated by Django 5.0.4 on 2024-05-21 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rater', '0008_rating_notes_alter_rating_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='notes',
            new_name='review',
        ),
    ]
