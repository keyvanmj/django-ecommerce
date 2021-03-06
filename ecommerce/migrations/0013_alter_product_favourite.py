# Generated by Django 3.2.5 on 2021-08-04 08:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0012_alter_product_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='favourite',
            field=models.ManyToManyField(blank=True, related_name='user_favourite', to=settings.AUTH_USER_MODEL),
        ),
    ]
