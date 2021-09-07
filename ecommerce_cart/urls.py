from django.urls import path
from .views import *
urlpatterns = [
    path('add-to-cart/<int:pro_id>',AddToCartView.as_view(),name='addtocart'),
    path('my-cart',MyCartView.as_view(),name='mycart'),
    path('manage-cart/<int:cp_id>',ManageCartView.as_view(),name='managecart'),
    path('empty-cart',EmptyCartView.as_view(),name='emptycart'),
    path('remove-cart',RemoveCartView.as_view(),name='removecart'),
    path('checkout',CheckoutView.as_view(),name='checkout'),
    path('profile',CustomerProfileView.as_view(),name='profileview'),
    path('profile/order/<int:pk>',CustomerOrderDetailView.as_view(),name='customerorderdetail'),
    path('information',CustomerInfo.as_view(),name='customer_information'),
    path('shopping-complete/<int:pk>',CompleteShopping.as_view(),name='shopping_complete'),
]


