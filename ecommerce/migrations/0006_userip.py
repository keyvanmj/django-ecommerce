# Generated by Django 3.2.5 on 2021-07-31 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.TextField(default=None)),
            ],
        ),
    ]