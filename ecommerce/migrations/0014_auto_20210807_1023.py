# Generated by Django 3.2.5 on 2021-08-07 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_category', '0002_alter_category_unique_together'),
        ('ecommerce', '0013_alter_product_favourite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='ecommerce_category.category'),
        ),
    ]
