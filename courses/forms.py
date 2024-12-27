from django import forms
from courses.models import *
from django.core import validators
class UserMF(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
        help_texts = {'username':''}
        widgets = {
            'username':forms.TextInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the username',
            }),
            'email':forms.EmailInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the Email'
            }),
            'password':forms.PasswordInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the Password'
            }),
        }

class ProfileMF(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','address','profile_pic']
        widgets = {
            'address':forms.Textarea(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the Address',
            }),
            'first_name':forms.TextInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the first_name'
            }),
            'last_name':forms.TextInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the last-name'
            }),
        }
    

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the username',
            }))
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the Password'
            }))