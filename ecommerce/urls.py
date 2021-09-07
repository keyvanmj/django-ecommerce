from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('header', views.header, name='header'),
    path('footer', views.footer, name='footer'),
    path('mini-footer', views.mini_footer, name='mini_footer'),
    path('contact-us', views.contact_us, name='contact'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<slug:slug>/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('sidebar',views.side_bar,name='sidebar'),
    path('responsive-nav',views.responsive_nav,name='responsive_nav')

]






