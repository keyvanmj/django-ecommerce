# Generated by Django 3.2.5 on 2021-07-26 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_profilemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]