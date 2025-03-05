# Generated by Django 5.1.6 on 2025-03-05 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=140)),
            ],
        ),
    ]
