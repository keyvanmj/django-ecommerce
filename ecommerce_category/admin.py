from django.contrib import admin
from . import models
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug','parent']
    search_fields = ['title','slug']

    prepopulated_fields = {'slug':('title',)}




