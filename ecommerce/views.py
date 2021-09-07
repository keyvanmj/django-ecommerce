from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView
from ecommerce_cart.models import Order, Cart
from ecommerce_cart.views import EcomMixin
from ecommerce_category.models import Category
from ecommerce_comment.forms import CommentForm
from ecommerce_comment.models import Comment
from ecommerce_filter.forms import CategoryProductFilter
from ecommerce_profile.models import Profile
from ecommerce_stats import stats
from site_settings.models import SiteSetting
from Django_ECommerce.settings import PRODUCT_PER_ROW
from .models import Product
from .forms import ContactForm
from persiantools import jdatetime
from .utils import my_grouper


class ProductList(EcomMixin, ListView):
    template_name = 'products/product_list.html'
    paginate_by = 8
    context_object_name = 'products'


    def get_queryset(self):
        return Product.objects.get_active_products()

    def get_context_data(self, *args, **kwargs):
        kwargs['counter'] = Product.objects.count()
        context = super(ProductList, self).get_context_data(*args, **kwargs)
        context['category'] = Category.objects.all
        context['form'] = CategoryProductFilter
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'products'
    form_class = CommentForm
    success_url = '/'


    def get_slug_field(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        cat = Category.objects.all()
        context['category'] = cat
        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)
        comments = product.comments.filter(status=True).order_by('-publish')
        context['comments'] = comments


        # related products
        related_products = Product.objects.get_active_products().filter(
            Q(category__product=product) |
            Q(category__parent__product=product) |
            Q(category__children__product=product)

        ).distinct().exclude(pk=self.kwargs['pk'])
        grouped_related_product = my_grouper(4,related_products)
        context['related'] = len([x for x in related_products])
        context['related_product'] = grouped_related_product

        # end related products

        # breadcrumbs
        instance = get_object_or_404(Product, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        breadcrumbs_link = instance.get_cat_list()
        category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
        breadcrumbs = zip(breadcrumbs_link, category_name)
        context['instance'] = instance
        context['breadcrumbs'] = breadcrumbs
        # end breadcrumbs
        if self.request.user.is_authenticated:
            context['form'] = CommentForm(instance=self.request.user)
        else:
            return context
        return context


    def post(self, request, *args, **kwargs):
        profile = Profile.objects.all()[:0]
        n = None
        for i in profile:
            n=i.user
        new_comment = Comment(content=request.POST.get('content'),
                              email=request.POST.get('email'),
                              author=request.user,
                              image=n,
                              product=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)



def home_page(request):
    user = User.objects.all()
    all_product = Product.objects.all()
    today = jdatetime.JalaliDateTime.now().strftime(" %A %d %B %Y ساعت  %X",locale='fa')
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCT_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    category = Category.objects.all()
    product_slug = Product.objects.filter(active=True).filter_products(request=request)
    last_month = datetime.today() - timedelta(days=30)
    most_view = Product.objects.filter(active=True).annotate(count=Count(
        'hits', filter=Q(producthit__created__gte=last_month))).order_by('-count', '-created')[:5]
    favourite_product = Product.objects.filter(active=True).annotate(count=Count(
        'hits', filter=Q(producthit__created__gte=last_month))).order_by('-favourite', '-count','-created','-hits')[:8]
    most_sell = Product.objects.most_sell_products()


    context = {
        'usr':user,
        'today':today,
        'search_recs':search_recs,
        'featured':featured,
        'recently_viewed':recently_viewed,
        'view_recs':view_recs,
        'category':category,
        'most_view':most_view,
        'product_slug':product_slug,
        'favourite_product':favourite_product,
        'most_sell':most_sell,
        'moment_recommended':all_product,
    }
    return render(request, 'home_page.html', context)


# header render partial
def header(request, *args, **kwargs):
    category = Category.objects.all()

    context = {
        'content': 'This is for Header',
        'category':category,
        'form':CategoryProductFilter()
    }
    return render(request, 'shared/header.html', context)


# footer render partial
def footer(request, *args, **kwargs):
    settings = SiteSetting.objects.first()
    user_count = User.objects.count()
    product_count = Product.objects.get_active_products().count()
    online_count = Profile.objects.filter(is_online=True).count()


    context = {
        'settings': settings,
        'user_count': user_count,
        'product_count': product_count,
        'on_count': online_count,

    }
    return render(request, 'shared/footer.html', context)


def responsive_nav(request):
    context = {
        'category':Category.objects.all()
    }
    return render(request,'shared/reponsive_nav.html',context)


# mini footer render partial
def mini_footer(request, *args, **kwargs):
    context = {}
    return render(request, 'shared/mini_footer.html', context)


# side bar render partial
def side_bar(request, *args, **kwargs):
    order = Order.objects.all()
    cart = Cart.objects.all()
    user = request.user.user_favourite.all()

    cart_count = request.user.cart_set.all()
    c = None
    for i in cart_count:
        c = i.cartproduct_set
    context = {
        'order': order,
        'cart': cart,
        'fav_count':user,
        'cart_count':c,
    }
    return render(request, 'shared/sidebar.html', context)


@login_required()
def contact_us(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            f_name = form.cleaned_data.get('first_name')
            l_name = form.cleaned_data.get('last_name')
            number = form.cleaned_data.get('number')
            email = form.cleaned_data.get('email')
            title = form.cleaned_data.get('title')
            descriptions = form.cleaned_data.get('descriptions')
            form.save()
            form = ContactForm()
            return HttpResponseRedirect('/contact-us', 'successfully sent')
        else:
            return render(request, 'shared/errors/error.html')

    context = {
        'content': 'با ما در ارتباط باشید',
        'form': form
    }
    return render(request, 'contact_page.html', context)


def handle_404_error(request,exception):
    return render(request,'status/404.html',{})