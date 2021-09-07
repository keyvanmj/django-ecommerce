from django.urls import path
from . import views
urlpatterns = [
    path('category/<hierarchy>', views.CategoryView.as_view(), name='category_view'),
]


