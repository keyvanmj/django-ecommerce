import json
from json import dumps as j_dumps
from django.core import serializers
from django.core.paginator import EmptyPage, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView
from .forms import CategoryProductFilter
from ecommerce.models import Product
from ecommerce_category.models import Category



class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise



class FilterProduct(ListView):
    template_name = 'products/product_list.html'
    paginator_class = SafePaginator
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.filter(active=True).filter_products(request=self.request)




    def get_context_data(self, *args, **kwargs):
        context = super(FilterProduct, self).get_context_data(*args, **kwargs)
        context['action'] = self.request.GET.get('action')
        context['form'] = CategoryProductFilter
        context['category'] = Category.objects.all()

        return context






class CheckboxFilterView(FormView,ListView):
    template_name = 'products/product_list.html'
    paginator_class = SafePaginator
    paginate_by = 8
    form_class = CategoryProductFilter


    def get_queryset(self):
        q = {k: v for k, v in self.request.GET.items() if v}
        queries = [(
            Q(category__slug__iexact=value) |
            Q(category__parent__slug__iexact=value) |
            Q(category__parent__parent__slug__iexact=value)
        ) for value in q.keys()]
        try:
            query = queries.pop()
            for item in queries:
                query |= item

            if q:
                if ('all', 'همه') in list(self.request.GET.items()):
                    for field_name,field in CategoryProductFilter().fields.items():
                        if field_name in q:
                            field.widget.attrs['checked'] = True
                    return Product.objects.all()

                else:
                    product = Product.objects.filter(query)
                    for field_name,field in self.get_form().fields.items():
                        if field_name in q:
                            field.widget.attrs['checked'] = True


                    return product
            else:
                return Product.objects.get_active_products()
        except:
            return Product.objects.all()


    def get_context_data(self, **kwargs):
        context = super(CheckboxFilterView, self).get_context_data(**kwargs)
        category = Category.objects.all()
        q = {k: v for k, v in self.request.GET.items() if v}
        context['category'] = category
        context['cat_q'] = q
        return context

