from django.contrib import admin
from django.utils.html import format_html

from . import models





class ProductInline(admin.TabularInline):
    model = models.Product
    extra = 3

    list_display = ['image_tag']

class ProductAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.list_image.url))

    image_tag.short_description = "Image"

    class Meta:
        model = models.Product
    list_display = ['__str__', 'price', 'slug', 'created', 'active', 'image_tag']





admin.site.register(models.ContactUs)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Image)
