from django.urls import path
from . import views

urlpatterns = [
    path('products/filter',views.FilterProduct.as_view(),name='filter_product'),
    path('products/filter-by-categories/',views.CheckboxFilterView.as_view(),name='checkbox_filter_partial'),
]

