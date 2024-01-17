from django import forms
from .models import *
from django.utils import timezone
from datetime import datetime, time
class LoginForm(forms.Form):
    email=forms.EmailField(label="email" ,max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    email = forms.EmailField()



class ProfileEditForm(forms.Form):
        contact_no = forms.CharField(max_length=15, required=True)
        address = forms.CharField(max_length=100, required=True)
        place = forms.CharField(max_length=100, required=True)
        city = forms.CharField(max_length=100, required=True)
        district = forms.CharField(max_length=100, required=True)
        pincode = forms.CharField(max_length=10, required=True)

class ProfileForm(forms.Form):
        f_name = forms.CharField(max_length=100, required=True)
        l_name = forms.CharField(max_length=100, required=True)
        contact_no = forms.CharField(max_length=10, required=True)
        address = forms.CharField(max_length=100, required=True)
        place = forms.CharField(max_length=100, required=True)
        city = forms.CharField(max_length=100, required=True)
        district = forms.CharField(max_length=100, required=True)
        pincode = forms.CharField(max_length=6, required=True)

class ProfileImage(forms.Form):
       profile_picture = forms.ImageField()

# ////////////////// Admin Form //////////////////////

class CarMakeForm(forms.ModelForm):
    class Meta:
        model = CarMake
        fields = ['make_name', 'make_Image']

class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['model_name', 'make_company', 'model_Image']

class FueltypeForm(forms.ModelForm):
    class Meta:
        model = Fueltype
        fields = ['fuel_name']

class ModelVariantForm(forms.ModelForm):
    class Meta:
        model = ModelVariant
        fields = ['model', 'fuel_type', 'torque', 'bhp', 'engine', 'transmission', 'tyre_size']
