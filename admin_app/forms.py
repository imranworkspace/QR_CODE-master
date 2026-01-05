from dataclasses import fields
from logging import PlaceHolder
from operator import inv
from typing import Type
from django import forms
from matplotlib import widgets
from numpy import require
#for modelform
from .models import AdminLoginModel
from django.core import validators       
# for mobile no
import re

class IndexAdminForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),label='Username',min_length=5,max_length=25,required=True,label_suffix=' ',error_messages={'required': 'Please Enter Username'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}),label='Password',required=True,label_suffix=' ',error_messages={'required': 'Please Enter Password'})
