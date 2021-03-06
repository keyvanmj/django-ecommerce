# Generated by Django 3.2.5 on 2021-07-13 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, default='all')),
                ('meta_keywords', models.CharField(default='ecommerce', help_text='Comma-delimited set of SEO keywords for meta tag', max_length=255, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(default='we have everything you need', help_text='Content for description meta tag', max_length=255, verbose_name='Meta Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='ecommerce_category.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['parent__id', '-created_at'],
            },
        ),
    ]
