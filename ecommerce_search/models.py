from django.contrib.auth.models import User
from django.db import models

class SearchTerm(models.Model):
    q = models.CharField(max_length=50,blank=True)
    search_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=50,default='')

    def __str__(self):
        return self.q