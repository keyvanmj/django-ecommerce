# Generated by Django 3.2.5 on 2021-07-26 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_cart', '0018_rename_customer_cart_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
