from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.core import validators
from django.urls import reverse
from django.utils.text import slugify
from ecommerce_category.models import Category
from ecommerce_manager.models import ProductManager, AbstractModel
from user_ip.models import IPAddress
from .utils import random_string_generator
from ecommerce_manager.models import FeaturedProductManager


def random_seller(instance, new_seller=None):
    if new_seller is not None:
        seller = new_seller
    else:
        seller = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(seller=seller).exists()
    if qs_exists:
        new_seller = "{seller}-{randstr}".format(
            seller=seller,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_seller)
    return seller


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug





class ContactUs(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    number = models.IntegerField(verbose_name='تلفن همراه')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    descriptions = models.TextField(verbose_name='توضیحات')

    def __str__(self):
        return f'from {self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = 'Contact Us'


class Product(AbstractModel):
    title = models.CharField(
        max_length=100)

    price = models.DecimalField(
        max_digits=10, decimal_places=2)

    descriptions = models.TextField()

    created = models.DateTimeField(
        auto_now_add=True)

    list_image = models.ImageField(
        blank=True, default='/assets/img/no-image-found-360x260.png', upload_to='products')

    slug = models.SlugField(
        max_length=200, blank=True)

    active = models.BooleanField(
        default=False)

    digital = models.BooleanField(
        default=False
    )

    specification = models.TextField(
        default='This product has no specifications', blank=True)

    brand = models.CharField(max_length=100,default='متفرقه')

    seller = models.CharField(max_length=50, default='E-Commerce', blank=True)

    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE)

    hits = models.ManyToManyField(IPAddress,through='ProductHit',blank=True,related_name='hits')

    favourite = models.ManyToManyField(User,related_name='user_favourite',blank=True)

    objects = ProductManager()

    featured = FeaturedProductManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

    def save_base(self, *args, **kwargs):
        if not self.seller:
            value = 'E-Commerce'
            self.seller = slugify(value, allow_unicode=True)
        super().save_base(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug':self.slug,'pk':self.pk})

    def get_cat_list(self):
        k = self.category
        breadcrumb = ['dummy']
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]



def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)




class Image(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Image')
    image = models.ImageField(upload_to='carousel')

    def __str__(self):
        return self.name


class ProductHit(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)