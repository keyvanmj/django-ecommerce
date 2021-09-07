from django.db import models
from django.db.models.signals import post_save,pre_save
from ecommerce.models import unique_slug_generator, Product


class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    product = models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return self.title

def tag_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(tag_pre_save_receiver,sender=Tag)