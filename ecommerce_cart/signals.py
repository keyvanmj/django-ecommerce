from ecommerce_cart.utils import unique_slug_generator
from django.db.models.signals import pre_save
from ecommerce_cart.models import Order
from .models import ORDER_STATUS



def order_transaction_id_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.transaction_id:
        instance.transaction_id = unique_slug_generator(instance)
pre_save.connect(order_transaction_id_pre_save_receiver,sender=Order)



def order_status_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.order_status or instance.order_status == 'درحال پردازش است':
        instance.order_status = 'سفارش کامل شد',instance
pre_save.connect(order_status_pre_save_receiver,sender=Order)



