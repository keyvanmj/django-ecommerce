# Generated by Django 3.2.5 on 2021-07-31 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_ip', '0001_initial'),
        ('ecommerce', '0007_delete_userip'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='hits', to='user_ip.IPAddress'),
        ),
    ]