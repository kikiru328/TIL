# Generated by Django 5.1.6 on 2025-03-05 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0002_house_pets_allowed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='price',
            new_name='price_per_night',
        ),
    ]
