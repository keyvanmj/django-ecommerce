from django import forms
from .models import ContactUs
from django.contrib.auth.models import User
from ecommerce.utils import BaseFormWithCaptcha

class ContactForm(forms.ModelForm,BaseFormWithCaptcha):

    class Meta:
        model = ContactUs
        fields = ('first_name', 'last_name', 'number', 'email', 'title', 'descriptions')

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='نام کاربری',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'نام کاربری را وارد نمایید', 'class': 'form-control'})
                               )
    password = forms.CharField(label='کلمه ی عبور',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'کلمه ی عبور را وارد نمایید', 'class': 'form-control'})
                               )
    # remember_me = forms.BooleanField(required=False)


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=150, label='ایمیل',
                             widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد نمایید'})
                             )
    username = forms.CharField(max_length=100, label='نام کاربری',
                               widget=forms.TextInput(attrs={'placeholder': 'نام کاربری را وارد نمایید'})
                               )
    password = forms.CharField(label='کلمه ی عبور',
                               widget=forms.PasswordInput(attrs={'placeholder': 'کلمه ی عبور را وارد نمایید'})
                               )
    password2 = forms.CharField(label='تکرار کلمه ی عبور',
                                widget=forms.PasswordInput(attrs={'placeholder': 'تکرارکلمه ی عبور را وارد نمایید'})
                                )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('کلمه عبور باید مشابه هم باشند')
        return data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('تعداد کلمه عبور وارد شده باید8عدد باشد')
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('این نام کاربری ازقبل وجود دارد')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('این ایمیل از قبل وجود دارد')
        elif 'gmail.com' not in email:
            raise forms.ValidationError('ایمیل وارد شده باید شامل gmail.com باشد')

        return email


