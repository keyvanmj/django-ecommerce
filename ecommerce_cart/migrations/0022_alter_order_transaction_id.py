# Generated by Django 3.2.5 on 2021-08-21 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_cart', '0021_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
