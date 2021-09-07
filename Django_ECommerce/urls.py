from django.conf.urls.static import static
from django.contrib.auth.models import Group

from . import settings
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from accounts.decorators import admin_required


admin.site.login = admin_required(admin.site.login)

urlpatterns = [
    path('', include('ecommerce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('accounts.urls')),
    path('', include('ecommerce_profile.urls')),
    path('', include('ecommerce_category.urls')),
    path('cart/', include('ecommerce_cart.urls')),
    path('', include('ecommerce_comment.urls')),
    path('', include('ecommerce_filter.urls')),
    path('favourite/', include('ecommerce_favourite.urls')),
    path('search/',include('ecommerce_search.urls')),
    path('admin/', admin.site.urls),
    ]

handler404 = 'ecommerce.views.handle_404_error'

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

