from functools import wraps

from django.http import Http404
from django.shortcuts import redirect


def admin_required(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.user.is_superuser:
            return func(request,*args,**kwargs)
        return redirect('/')
    return wrapper