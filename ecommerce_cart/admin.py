from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['transaction_id','full_name','order_status']


admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order,OrderAdmin)


