# Generated by Django 3.2.5 on 2021-07-23 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_cart', '0010_auto_20210723_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=200, verbose_name='نام و نام خانوادگی'),
        ),
    ]