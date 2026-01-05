from dataclasses import fields
from logging import PlaceHolder
from operator import inv
from typing import Type
from django import forms
from matplotlib import widgets
from numpy import require
#for modelform
from .models import RegistrationModel,AdminModel
from django.core import validators       
# for mobile no
import re

class ForgotPasswordForm(forms.Form):
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'}),label_suffix=' ',required=True,error_messages={'required': 'Please Enter Email'})

class ForgotSuccessForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'txt_otp'}),max_length=9,required=True,label_suffix=' ',error_messages={'required': 'Please Enter OTP'})
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'txt_password1'}),required=True,label_suffix=' ',error_messages={'required': 'Please Enter New Password'})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'txt_password2'}),required=True,label_suffix=' ',error_messages={'required': 'Please Enter Confirm Password'})

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=RegistrationModel
        error_css_class='error'
        required_css_class='required'
        
        fields=['fname','lname','email','mobile','website','password','confirm']
        
        lable_suffix=['']
        blanks={'empid':True}
        labels={
            'fname':'First Name',
            'lname':'Last Name',
            'email':'Email',
            'mobile':'Mobile (+91)',
            'website':'Company Name',
            'password':'Password [6-32]',
            'confirm':'Confirm Password(Again)',
            }
        help_text={'fname':{'First Name'}}
        error_messages={
            'fname':{'required':'Enter First Name'},
            'lname':{'required':'Enter Last Name'},
            'email':{'required':'Enter Email'},
            'mobile':{'required':'Enter Mobile Number'},
            'website':{'required':'Enter Company Website'},
            'password':{'required':'Enter Password'},
            'confirm':{'required':'Enter Confirm Password'},
            }
        
        widgets={
            'empid':forms.HiddenInput(attrs={'class':'form-control'}),
            'fname':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name - Be Careful No Update Available For It'}),
            'lname':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name - Be Careful No Update Available For It'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email  - Be Careful No Update Available For It'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control','placeholder':'Mobile  - Be Careful No Update Available For It'}),
            'website':forms.URLInput(attrs={'class':'form-control','placeholder':'Company Name  - Be Careful No Update Available For It'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
            'confirm':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}),
            'date':forms.HiddenInput(attrs={'class':'form-control'}),
        }
    # check current password and confirm password is same or not
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        # mobile = cleaned_data['mobile']
        # print('mobile ',mobile)
        def invalid(mobile):
            pattern = re.compile('(0|91)?[-\s]?[6-9]\d{9}')
            print('mobile is valid')
            return pattern.match(mobile)
        try:
            fname = cleaned_data['fname']
            lname = cleaned_data['lname']
            mobile = cleaned_data['mobile']
            password = cleaned_data['password']
            confirm = cleaned_data['confirm']
            print('password form : ',password)
            print('password type : ',type(password))
            if fname is None:
                pass
            if lname is None:
                pass
            if mobile is None:
                pass
            if password is None:
                pass
            if confirm is None:
                pass
            if fname == lname:
                raise forms.ValidationError(
                    "first name and last name should not be same"
                )
            if len(password) <= 6 or len(password) >= 32:
                raise forms.ValidationError(
                    "password should be min  6 characters and max 32 characters"
                )
            if len(confirm) <= 6 or len(confirm) >= 32:
                raise forms.ValidationError(
                    "confirm password should be min  6 characters and max 32 characters"
                )
            if password != confirm:
                raise forms.ValidationError(
                    "password and confirm does not match"
                )
            if mobile:
               invalid(mobile) 
            else:
                raise forms.ValidationError(
                    "enter valid mobile number"
                )
        except KeyError as k:
            print('key is empty',k)
    
class AdminForm(forms.ModelForm):
    class Meta:
        model=AdminModel
        fields=['name','email','password','otp']
        labels={'name':'Name','password':'Password','email':'Email','otp':'OTP'}
        help_text={'name':{'Name'},'password':{'Password'},'email':{'Email'},'otp':{'OTP'}}
        error_messages={
            'name':{'required':'Enter Name'},
            'password':{'required':'Enter Password'},
            'email':{'required':'Enter Email'},
            'otp':{'required':'Enter otp'},
            }
    
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Full Name'}),
            'password':forms.PasswordInput(render_value=True, attrs={'class':'form-control','placeholder':'Password'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'otp':forms.EmailInput(attrs={'class':'form-control','placeholder':'OTP'}),

        }
    def clean(self):
        cleaned_data = super(AdminForm, self).clean()
        try:
            password = cleaned_data['password']
            print('password form : ',password)
            print('password type : ',type(password))
            if password is None:
                    pass
            if len(password) <= 6 or len(password) >= 32:
                raise forms.ValidationError(
                    "password should be min  6 characters and max 32 characters"
                )
        except KeyError as k:
            print('key AdminForm is empty',k)

class IndexForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),label='Username',min_length=5,max_length=25,required=True,label_suffix=' ',error_messages={'required': 'Please Enter Username'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}),label='Password',required=True,label_suffix=' ',error_messages={'required': 'Please Enter Password'})

# class OtpForm(forms.ModelForm):
#     class Meta:
#         model=OtpModel
#         fields=['mobile','otp']
#         labels={'mobile':'Mobile','otp':'OTP'}
#         help_text={'mobile':{'mobile'},'otp':{'OTP'}}
#         error_messages={
#             'mobile':{'required':'Enter Mobile No',
#             'otp':{'required':'Enter OTP',
#             }}}
    
#         widgets={
#             'mobile':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Mobile No.'}),
#             'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
#         }

