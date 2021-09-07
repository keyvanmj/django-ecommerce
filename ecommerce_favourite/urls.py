from django.urls import path
from .views import add_favourite,remove_favourite,favourite_view
urlpatterns = [
    path('',favourite_view,name='favouriteview'),
    path('<int:pk>/add',add_favourite,name='addtofavourite'),
    path('<int:pk>/remove',remove_favourite,name='removefavourite'),
]