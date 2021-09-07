from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import *
from ecommerce.models import Product


@login_required
def favourite_view(request):
    product = Product.objects.filter(favourite=request.user)


    context = {
        'product':product,
    }
    return render(request,'favourite.html',context)




@login_required
def add_favourite(request, pk):
    product = get_object_or_404(Product,pk=pk)
    if not product.favourite.filter(id=pk).exists():
        product.favourite.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def remove_favourite(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if not product.favourite.filter(id=pk).exists():
        product.favourite.remove(request.user)
    else:
        product.favourite.remove(request.user)


    return HttpResponseRedirect(request.META['HTTP_REFERER'])

