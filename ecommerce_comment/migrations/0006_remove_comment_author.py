# Generated by Django 3.2.5 on 2021-08-08 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_comment', '0005_comment_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]
