import itertools
import random
import string
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


print(random_string_generator())

print(random_string_generator(size=50))



def my_grouper(n,iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


class BaseFormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(
        label='تصویر امنیتی',
        widget=ReCaptchaV2Checkbox(api_params={
            'hl':'fa'
        }),
        error_messages={
            'required': 'لطفا تصویر امنیتی را تایید کنید'
        }
    )