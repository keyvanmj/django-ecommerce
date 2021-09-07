from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from ecommerce.models import Product
from ecommerce_profile.models import Profile


class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    image = models.OneToOneField(Profile,null=True,on_delete=models.CASCADE,blank=True)

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.author)