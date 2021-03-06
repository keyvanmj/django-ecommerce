from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    title = models.CharField(max_length=150,verbose_name='عنوان سایت')
    address = models.CharField(max_length=300,verbose_name='آدرس')
    phone = models.CharField(max_length=50,verbose_name='تلفن ثابت')
    mobile = models.CharField(max_length=50,verbose_name='تلفن همراه')
    fax = models.CharField(max_length=50,verbose_name='فکس')
    email = models.EmailField(max_length=50,verbose_name='ایمیل')
    about_us = models.TextField(verbose_name='درباره ی ما')
    copy_right = models.CharField(max_length=200,verbose_name='کپی رایت')

    def __str__(self):
        return self.title
