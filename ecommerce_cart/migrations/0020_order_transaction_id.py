# Generated by Django 3.2.5 on 2021-08-21 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_cart', '0019_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
