from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from ecommerce_cart.models import Order
from ecommerce_category.models import Category
from .forms import ProfileForm


@login_required
def profile_view(request,*args,**kwargs):
    if request.method == 'POST':
        p_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():

            p_form.save()
            messages.success(request, f'تصویر پروفایل شما بروزرسانی شد')
            return redirect('accounts:change_profile')

    else:
        p_form = ProfileForm(instance=request.user.profile)
    user = request.user.user_favourite.all()
    context = {
        'p_form': p_form,
        'fav_count' : user,
    }

    return render(request, 'avatars.html', context)