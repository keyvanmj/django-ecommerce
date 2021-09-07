from django.contrib import admin
from .models import SearchTerm

class SearchAdmin(admin.ModelAdmin):
    list_display = ('__str__','ip_address','search_date')
    list_filter = ('ip_address','user','q')
    exclude = ('user',)

admin.site.register(SearchTerm,SearchAdmin)
