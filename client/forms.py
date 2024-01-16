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

class ModelForm(forms.ModelForm):
    model_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    model_Image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control file-upload-info'})
    )
    class Meta:
        model = CarModel
        fields = ['model_name', 'make_company', 'model_Image']
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        # Customize the 'Make' field widget
        self.fields['make_company'].widget = forms.Select(
            attrs={'class': 'form-control'},
            choices=[(make.pk, make.make_name) for make in CarMake.objects.all()]
        )
class MakeForm(forms.ModelForm):
    make_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'oninput': 'validateMakeName(this)'})
    )

    class Meta:
        model = CarMake
        fields = ['make_name']

