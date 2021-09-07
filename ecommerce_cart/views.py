from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseGone, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls.resolvers import URLResolver
from django.dispatch.dispatcher import logger
from django.template import RequestContext
from django.shortcuts import redirect
from Django_ECommerce import settings
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import CheckoutForm
from ecommerce.models import *
from random import choice
from .models import *
import datetime
import decimal
import uuid


class EcomMixin(View):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user:
                cart_obj.user = request.user
                cart_obj.save()

        return super(EcomMixin, self).dispatch(request, *args, **kwargs)


class AddToCartView(TemplateView):
    template_name = 'my_cart.html'

    def get(self, request, *args, **kwargs):
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)
        # check if cart exists
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            current_product_cart = cart_obj.cartproduct_set.filter(
                product=product_obj
            )
            # item already exists in cart
            if current_product_cart.exists():
                cartproduct = current_product_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
                messages.info(request, 'سبد خرید شماآپدیت شده است',extra_tags='info')
                return redirect(request.META.get('HTTP_REFERER'))
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, quantity=1,
                                                         rate=product_obj.price,
                                                         subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()
                messages.success(request,'محصول شما با موفقیت به سبد خرید اضافه شد.')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, quantity=1,
                                                     rate=product_obj.price,
                                                     subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()
            messages.success(request, 'محصول شما با موفقیت به سبد خرید اضافه شد')
            return redirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MyCartView(TemplateView):
    template_name = 'my_cart.html'

    def get_context_data(self, **kwargs):
        context = super(MyCartView, self).get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        cart_obj = CartProduct.objects.all()
        if cart is not None:
            if not cart_obj:
                cart.total = 0
                cart.save()

            elif cart_obj is None:
                return redirect('emptycart')

            return context

    def get(self, request, *args, **kwargs):
        cart_obj = CartProduct.objects.all()
        context = super(MyCartView, self).get(request, *args, **kwargs)
        cart_id = self.request.session.get('cart_id')
        order = Order.objects.all()

        if not cart_obj:
            return redirect('emptycart')
        return context


class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        cart_id = request.session.get('cart_id', None)

        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass

        return redirect('mycart')


class EmptyCartView(EcomMixin, TemplateView):
    template_name = 'empty_cart.html'

    def get(self, *args, **kwargs):
        cart_obj = CartProduct.objects.all()
        context = super(EmptyCartView, self).get(*args, **kwargs)
        if cart_obj:
            return redirect('mycart')
        return context


class RemoveCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('mycart')


class CheckoutView(EcomMixin, CreateView, LoginRequiredMixin):
    template_name = 'checkout.html'
    form_class = CheckoutForm


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cart_p = CartProduct.objects.all()
        cart_id = self.request.session.get('cart_id', None)
        if not cart_p.exists():
            return redirect('emptycart')
        elif cart_id is None:
            return redirect('mycart')
        return super(CheckoutView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def get_success_url(self):
        success_url = reverse_lazy('shopping_complete', args=(self.object.pk,))
        return success_url

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            # form.instance.order_status = 'درحال پردازش است'
            del self.request.session['cart_id']

        else:
            return redirect('home')
        return super(CheckoutView, self).form_valid(form)


class CustomerProfileView(TemplateView, LoginRequiredMixin, EcomMixin):
    template_name = 'customer_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerProfileView, self).get_context_data(**kwargs)
        customer = self.request.user
        context['customer'] = customer
        orders = Order.objects.filter(cart__user=customer).order_by('-created_at')
        context['orders'] = orders
        return context


class CustomerOrderDetailView(DetailView, LoginRequiredMixin):
    template_name = 'customer_order_detail.html'
    model = Order
    context_object_name = 'ord_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            order_id = self.kwargs['pk']
            order = Order.objects.get(id=order_id)
            if request.user != order.cart.user:
                return redirect('profileview')
        else:
            return redirect('accounts:log_in')
        return super(CustomerOrderDetailView, self).dispatch(request, *args, **kwargs)


class CustomerInfo(TemplateView, LoginRequiredMixin, EcomMixin):
    template_name = 'customer_info.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerInfo, self).get_context_data(**kwargs)
        customer = self.request.user
        joined_on = customer.date_joined
        context['customer'] = customer
        context['created_at'] = joined_on
        order = Order.objects.filter(cart__user=self.request.user)
        context['address'] = list(x.shipping_address for x in order)
        return context


class CompleteShopping(DetailView, LoginRequiredMixin):
    template_name = 'shopping_complete_buy.html'



    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        order = Order.objects.filter(cart__user=self.request.user)
        try:
            if order:
                return order

            else:
                return redirect('/')
        except:
            raise Http404()


    def get_context_data(self, **kwargs):
        context = super(CompleteShopping, self).get_context_data(**kwargs)
        orderId = self.kwargs['pk']
        order = Order.objects.filter(id=orderId)
        context['all_order'] = order
        return context
