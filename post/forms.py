from django import forms
from django.contrib.auth.models import User

# from .models import Profile


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# 用户注册表单
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if User.objects.filter(email=data).exists():
    #         raise forms.ValidationError('Email already in use.')
    #     return data


class SearchForm(forms.Form):
    keywords = forms.CharField(label="")

