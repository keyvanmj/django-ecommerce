# Generated by Django 3.2.5 on 2021-08-07 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_category', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('slug', 'parent')},
        ),
    ]
