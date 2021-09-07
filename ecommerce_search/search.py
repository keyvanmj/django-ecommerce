from .models import SearchTerm
from ecommerce.models import Product
from django.db.models import Q
from ecommerce_stats import stats



STRIP_WORDS = ['']

# store the search in database


def _prepare_words(search_text):
    words =''
    try:
        words = search_text.split()
    except:
        pass


    for common in STRIP_WORDS:
        try:
            if common in STRIP_WORDS:
                words.remove(common)
        except:
            pass
    return words[0:5]



def store(request,q):
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        term.ip_address = ip
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated:
            term.user = request.user
        term.save()



# get product matching the search text

def products(search_text):
    words = _prepare_words(search_text)
    products = Product.objects.get_active_products()
    results = {}
    results['products'] = Product.objects.get_active_products().order_by('-created')

    for word in words:
        products = products.filter(
            Q(title__icontains=word) |
            Q(descriptions__icontains=word) |
            Q(brand__icontains=word) |
            Q(tag__title__icontains=word) |
            Q(category__title__icontains=word) |
            Q(category__slug__icontains=word) |
            Q(category__parent__slug__icontains=word) |
            Q(category__parent__title__icontains=word) |
            Q(category__title__icontains=word) |
            Q(category__parent__title__icontains=word) |
            Q(category__children__slug__icontains=word)
        )
        results['products'] = products.distinct()
    return results
