import json

from django import template
from django.http import HttpResponse
from django.template.loader import render_to_string

from .. import search
from ..forms import SearchForm
from urllib.parse import urlencode

register = template.Library()

@register.inclusion_tag('tags/search_box.html')
def search_box(request):
    q = request.GET.get('q','')
    form = SearchForm({'q':q})
    results = search.products(q).get('products')
    data = {
        'form':form,
        'result':results
        }
    return data

@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request,page_obj):
    raw_params = request.GET.copy()
    page = raw_params.get('page',1)
    p = page_obj.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = urlencode(raw_params)
    return {'request':request,'paginator':page_obj,'p':p,'params':params}


