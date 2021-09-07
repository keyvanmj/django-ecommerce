from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify

from ecommerce.models import Product
from django.db import models

from ecommerce_cart.utils import unique_slug_generator


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart : {str(self.id)}'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f'Cart : {str(self.cart.id)} CartProduct : {str(self.id)}'


ORDER_STATUS = (
    ('','سفارش دریافت شد'),
    ('','درحال پردازش است'),
    ('','در راه است'),
    ('','سفارش کامل شد'),
    ('','سفارش لغو شد')
)


class Order(models.Model):
    cart = models.OneToOneField(Cart,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200,verbose_name='نام و نام خانوادگی',blank=True,null=True)
    shipping_address = models.TextField(max_length=200,verbose_name='آدرس پستی')
    mobile = models.CharField(max_length=11,verbose_name='تلفن همراه')
    email = models.EmailField(blank=True,null=True,verbose_name='ایمیل')
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS,default=ORDER_STATUS[1])
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50,null=True)

    def __str__(self):
        return f'Order: {str(self.id)}'

    def save(self, *args, **kwargs):
        if self.transaction_id == 'درحال پردازش است' or self.transaction_id is None:
            value = ORDER_STATUS[3]
            self.order_status = slugify(value, allow_unicode=True)
        super(Order, self).save()



