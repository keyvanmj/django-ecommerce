# Generated by Django 3.2.5 on 2021-07-31 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_userip'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserIp',
        ),
    ]