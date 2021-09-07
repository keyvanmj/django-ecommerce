from django.urls import path
from .views import profile_view
urlpatterns = [
    path('accounts/change/profile/image',profile_view,name='avatar'),
]
