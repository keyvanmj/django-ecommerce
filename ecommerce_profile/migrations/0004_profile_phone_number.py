# Generated by Django 3.2.5 on 2021-08-10 09:05

import accounts.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_profile', '0003_profile_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[accounts.forms.phone_valid]),
        ),
    ]
