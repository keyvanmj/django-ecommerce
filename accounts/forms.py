from datetime import timedelta
from django.shortcuts import render
from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _





class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('کلمه عبور'), strip=False,
                               widget=forms.PasswordInput(attrs={'id': 'myInput', 'type': 'password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('مرا بخاطر بسپار'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('شما کلمه عبور نامعتبر را وارد کردید.'))

        return password


class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('نام کاربري'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('شما نام کاربری نامعتبر را وارد کردید.'))

        if not user.is_active:
            raise ValidationError(_('این حساب فعال نیست.'))

        self.user_cache = user

        return username


class SignInViaEmailForm(SignIn):
    email = forms.EmailField(label=_('ایمیل'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('شما آدرس ایمیل نامعتبر را وارد کردید.'))

        if not user.is_active:
            raise ValidationError(_('این حساب فعال نیست.'))

        self.user_cache = user

        return email


class SignInViaEmailOrUsernameForm(SignIn):
    email_or_username = forms.CharField(label=_('ایمیل با نام کاربری'))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email_or_username', 'password', 'remember_me']
        return ['email_or_username', 'password']

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('شما آدرس ایمیل یا نام کاربری نامعتبر را وارد کردید.'))

        if not user.is_active:
            raise ValidationError(_('این حساب فعال نیست.'))

        self.user_cache = user

        return email_or_username


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS

    email = forms.EmailField(label=_('ایمیل'), help_text=_('اجباری. آدرس ایمیلی را که ازقبل وجود دارد را وارد کنید.'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(_('شما نمیتوانید از این آدرس ایمیل استفاده کنید.'))

        return email


class ResendActivationCodeForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_('ایمیل یا نام کاربری'))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('شما آدرس ایمیل یا نام کاربری نامعتبر را وارد کردید.'))

        if user.is_active:
            raise ValidationError(_('این حساب در حال حاضر فعال است.'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('کد فعال سازی پیدا نشد.'))

        now_with_shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('کد فعال سازی ارسال شد. شما میتوانید در 24 ساعت آینده کد جدید را دوباره دزخواست کنید.'))

        self.user_cache = user

        return email_or_username


class ResendActivationCodeViaEmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('ایمیل'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('شما آدرس ایمیل نامعتبر را وارد کردید.'))

        if user.is_active:
            raise ValidationError(_('این حساب در حال حاضر فعال است.'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('کد فعال سازی پیدا نشد.'))

        now_with_shift = timezone.now() - timedelta(hours=24)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('کد فعال سازی ارسال شد. شما میتوانید در 24 ساعت آینده کد جدید را دوباره دزخواست کنید.'))

        self.user_cache = user

        return email


class RestorePasswordForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('ايميل'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('شما آدرس ایمیل نامعتبر را وارد کردید.'))

        if not user.is_active:
            raise ValidationError(_('این حساب فعال نیست.'))

        self.user_cache = user

        return email


class RestorePasswordViaEmailOrUsernameForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_('ایمیل یا نام کاربری'))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('شما آدرس ایمیل یا نام کاربری نامعتبر را وارد کردید.'))

        if not user.is_active:
            raise ValidationError(_('این حساب فعال نیست.'))

        self.user_cache = user

        return email_or_username

def phone_valid(value):
    if len(value) >= 12:
        raise ValidationError(f'حداکثر عدد وارد شده باید 11 رقم باشد.({len(value)}عدد وارد شده)')
    elif len(value) <= 10:
        raise ValidationError(f'حداقل عدد وارد شده باید 11 رقم باشد.({len(value)}عدد وارد شده)')
    elif '-' in value:
        raise ValidationError(f'فرمت تلفن همراه وارد شده اشتباه است.')





class ChangeProfileForm(forms.Form):
    first_name = forms.CharField(label=_('نام'), max_length=30, required=False)
    last_name = forms.CharField(label=_('نام خانوادگي'), max_length=150, required=False)
    phone_number = forms.CharField(label=_('تلفن همراه'),widget=forms.NumberInput,validators=[phone_valid])



class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label=_('ایمیل'))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if email == self.user.email:
            raise ValidationError(_('لطفا ایمیل دیگری را وارد نمایید.'))

        user = User.objects.filter(Q(email__iexact=email) & ~Q(id=self.user.id)).exists()
        if user:
            raise ValidationError(_('شما نمیتوانید از این ایمیل استفاده کنید.'))

        return email


class RemindUsernameForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('ایمیل'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('شما آدرس ایمیل نامعتبر را وارد کردید.'))

        if not user.is_active:
            raise ValidationError(_('این حساب فعال نیست.'))

        self.user_cache = user

        return email

