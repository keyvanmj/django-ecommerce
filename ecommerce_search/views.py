import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet
from django.db.models.fields.files import ImageFieldFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, FormView, TemplateView
from ecommerce_category.models import Category
from ecommerce_filter.forms import CategoryProductFilter
from ecommerce_stats import stats
from .forms import SearchForm
from ecommerce.models import Product
from ecommerce_search import search
from .models import SearchTerm



class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o,QuerySet):
            try:
                return str(o)
            except TypeError:
                return ''
        if isinstance(o, ImageFieldFile):
            try:
                return str(o)
            except ValueError:
                return ''
        raise TypeError(repr(o) + "is not JSON serializable")


class JSONResponseMixin:
    def render_to_json_response(self,context,**response_kwargs):
        return JsonResponse(self.get_data(context),**response_kwargs)

    def get_data(self,context):
        return context

class JSONView(JSONResponseMixin,TemplateView):
    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax and self.request.method == 'GET':
            q = self.request.GET.get('q')
            res = None
            results = search.products(q).get('products')
            if len(results) > 0 and len(q) > 0:
                data = []
                for p in results:
                    item = {
                        'get_absolute_url': p.get_absolute_url(),
                        'name': p.title,
                        'price': p.price,
                        'list_image': p.list_image.url,
                        'seller': p.seller,
                        'hits': json.dumps(p.hits.count(),cls=ExtendedEncoder),
                    }
                    data.append(item)
                res = data
            else:
                res = 'هیچ موردی یافت نشد'
            return JsonResponse({'data': res})
        return self.render_to_json_response(context,**response_kwargs)


class Result(ListView):
    template_name = 'products/product_list.html'
    paginate_by = 8


    def get_queryset(self):
        q = self.request.GET.get('q')
        product = search.products(q).get('products')
        stats.log_product_view(self.request,product)
        if q is not None:
            return search.products(q).get('products')
        return Product.objects.get_active_products()

    def get_context_data(self, *args, **kwargs):

        context = super(Result, self).get_context_data(*args,**kwargs)
        q = self.request.GET.get('q', '')
        search.store(self.request, q)
        context['q'] = q
        results = search.products(q).get('products')
        context['products'] = results
        context['category'] = Category.objects.all()
        context['result'] = f' شما در جستجو {q}هستید '
        context['form'] = CategoryProductFilter
        return context
