import os
import base64
from ecommerce_search.models import SearchTerm
from Django_ECommerce.settings import PRODUCT_PER_ROW
from ecommerce_search import search
from .models import ProductView
from ecommerce.models import Product

def tracking_id(request):
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36)).decode('utf8')
        return request.session['tracking_id']


def recommended_from_search(request):
    common_words = frequent_search_words(request)
    matching = []
    for word in common_words:
        results = search.products(word).get('products',[])
        for r in results:
            if len(matching) < PRODUCT_PER_ROW and r not in matching:
                matching.append(r)
    return matching

def frequent_search_words(request):
    searches = SearchTerm.objects.filter(tracking_id=tracking_id(request)).values('q').order_by('-search_date')[:10]
    search_string = ' '.join([_search['q'] for _search in searches])
    return sort_words_by_frequency(search_string)[:3]

def sort_words_by_frequency(some_string):
    words = some_string.split()
    ranked_words = [[word,words.count(word)] for word in set(words)]
    sorted_words = sorted(ranked_words,key=lambda word:-word[1])
    return [p[0] for p in sorted_words]


def log_product_view(request,product):
    t_id = tracking_id(request)
    try:
        v,t = ProductView.objects.get_or_create(tracking_id=t_id,product=product[0])
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        v.ip_address = ip
        v.tracking_id = t_id
        v.user = None
        if request.user.is_authenticated:
            v.user = request.user
        v.save()
    except ProductView.DoesNotExist:
        v = ProductView()
        v.product = product
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        v.ip_address = ip
        v.tracking_id = t_id
        v.user = None
        if request.user.is_authenticated:
            v.user = request.user
        v.save()
    except IndexError:
        pass

def recommended_from_views(request):
    t_id = tracking_id(request)
    viewed = get_recently_viewed(request)
    if viewed:
        productviews = ProductView.objects.filter(product__in=viewed).values('tracking_id')
        t_ids = [v['tracking_id'] for v in productviews]
        if t_ids:
            all_viewed = Product.objects.filter(productview__tracking_id__in=t_ids)
            if all_viewed:
                other_viewed = ProductView.objects.filter(product__in=all_viewed).exclude(product__in=viewed)
                if other_viewed:
                    return Product.objects.filter(productview__in=other_viewed).distinct()


def get_recently_viewed(request):
    t_id = tracking_id(request)
    views = ProductView.objects.filter(tracking_id=t_id).values('product_id').order_by('-date')[0:PRODUCT_PER_ROW]
    product_ids = [v['product_id'] for v in views]
    return Product.objects.filter(id__in=product_ids)