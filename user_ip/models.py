from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'{self.ip_address}'
