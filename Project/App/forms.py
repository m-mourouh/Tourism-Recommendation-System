from django import forms
from django.db import models
from numpy import unique
from .models import Client , Rating



class ClientForm(forms.ModelForm):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField()
    birthdate = forms.DateField()
    gender = forms.CharField(widget=forms.RadioSelect)
    h_version = forms.CharField(widget=forms.Select)
    password = forms.CharField(widget=forms.PasswordInput) 
    confirmpass = forms.CharField(widget=forms.PasswordInput) 
    
    class Meta:
        model = Client
        fields = ['firstname','lastname', 'email', 'birthdate','gender','h_version','password']


class ProfileForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    birthdate = forms.DateField()
    gender = forms.CharField(widget=forms.Select)
    h_version = forms.CharField(widget=forms.Select)
    password = forms.CharField(required=False,widget=forms.PasswordInput) 
    confirmpass = forms.CharField(required=False,widget=forms.PasswordInput) 
    address = forms.CharField(max_length=255)
    country = forms.CharField(max_length=100)   
    profile_img = forms.ImageField(required=False)
    
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['email']

