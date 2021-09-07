from datetime import datetime
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
from Django_ECommerce import settings


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True,null=True)
    phone_number = models.PositiveIntegerField(null=True,blank=True)
    image = models.ImageField(default='profiles/not-pictured-circle.png',upload_to='profiles')
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)


    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
