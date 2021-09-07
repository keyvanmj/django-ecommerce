from django.contrib.auth.models import User
from django.db import models

from ecommerce.models import Product


class Page(models.Model):
    class Meta:
        abstract = True

    date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=50,default='')


class ProductView(Page):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.product} / {self.date} / {self.user} / {self.ip_address}'
