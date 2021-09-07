# Generated by Django 3.2.5 on 2021-07-13 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecommerce_category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.TextField(verbose_name='نظر خود را وارد نمایید')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('number', models.IntegerField(verbose_name='تلفن همراه')),
                ('email', models.EmailField(max_length=100, verbose_name='ایمیل')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('descriptions', models.TextField(verbose_name='توضیحات')),
            ],
            options={
                'verbose_name_plural': 'Contact Us',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descriptions', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('list_image', models.ImageField(blank=True, default='/assets/img/no-image-found-360x260.png', upload_to='products')),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('specification', models.TextField(blank=True, default='This product has no specifications')),
                ('brand', models.CharField(default='متفرقه', max_length=100)),
                ('seller', models.CharField(blank=True, default='E-Commerce', max_length=50)),
                ('category', models.ManyToManyField(blank=True, related_name='product_category', to='ecommerce_category.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='carousel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Image', to='ecommerce.product')),
            ],
        ),
    ]