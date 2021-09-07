from django.contrib import admin
from . import models

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product','email','publish','status',)
    list_filter = ('status','publish',)
    search_fields = ('email','content',)
    actions = ['approve_comments']

    def approve_comments(self,request,queryset):
        queryset.update(status=True)
