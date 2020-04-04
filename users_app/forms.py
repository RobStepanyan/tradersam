from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type':'username', 'id':'username', 'class':'form-control', 'placeholder':'Username', 'autofocus':'True'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'type':'email', 'id':'email', 'class':'form-control', 'placeholder':'Email Address'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type':'password', 'id':'password1', 'class':'form-control', 'placeholder':'Password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type':'password', 'id':'password2', 'class':'form-control', 'placeholder':'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLogInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type':'username', 'id':'username', 'class':'form-control', 'placeholder':'Username', 'autofocus':'True'}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type':'password', 'id':'password', 'class':'form-control', 'placeholder':'Confirm Passsword'}))
    
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'type':'checkbox', 'class':'custom-control-input border-0', 'id':'customCheck1'}))