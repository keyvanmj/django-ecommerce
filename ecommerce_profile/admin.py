from django.contrib import admin
from .models import Profile




class OnlineAdmin(admin.ModelAdmin):
    list_display = ['user','is_online','last_seen']

admin.site.register(Profile,OnlineAdmin)