# Generated by Django 3.2.5 on 2021-08-07 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_category', '0004_alter_category_parent'),
        ('ecommerce', '0015_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_set', to='ecommerce_category.category'),
        ),
    ]
