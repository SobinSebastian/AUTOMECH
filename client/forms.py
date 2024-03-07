from django import forms
from .models import *
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth.hashers import make_password
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

class ProfilesetupForm(forms.Form):
    contact_no = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}))
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    place = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    district = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}))
    pincode = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}))

# ////////////////// Admin Form //////////////////////

class CarMakeForm(forms.ModelForm):
    template_name = "form_snippet.html"
    class Meta:
        model = CarMake
        fields = ['make_name', 'make_Image']
        labels = {
            'make_name': 'Manufacture Name',
            'make_Image': ' Image',
        }
        widgets = {
            'make_name': forms.TextInput(attrs={'placeholder': 'Enter the manufacturer name','class': 'form-control'}),
            'make_Image': forms.ClearableFileInput(attrs={'accept': 'image/*','class': 'form-control file-upload-info'}),
        }

class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['model_name', 'make_company', 'model_Image']
        widgets = {
            'model_name': forms.TextInput(attrs={'placeholder': 'Enter the Model name','class': 'form-control'}),
            'make_company': forms.Select(attrs={'class': 'form-control'}, choices=[]),
            'model_Image': forms.ClearableFileInput(attrs={'accept': 'image/*','class': 'form-control file-upload-info'}),
        }

class FueltypeForm(forms.ModelForm):
    class Meta:
        model = Fueltype
        fields = ['fuel_name']

class ModelVariantForm(forms.ModelForm):
    class Meta:
        model = ModelVariant
        fields = ['variant_name','model', 'fuel_type', 'torque', 'bhp', 'engine', 'transmission', 'tyre_size']
        widgets = {
            'variant_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}, choices=[]),
            'torque': forms.TextInput(attrs={'class': 'form-control'}), 
            'bhp' : forms.TextInput(attrs={'class': 'form-control'}), 
            'engine' : forms.TextInput(attrs={'class': 'form-control'}),
            'transmission' : forms.Select(attrs={'class': 'form-control'}),
            'tyre_size' : forms.TextInput(attrs={'class': 'form-control'}),
        }


class NewVariantForm(forms.ModelForm):
    class Meta:
        model = ModelVariant
        fields = ['fuel_type', 'torque', 'bhp', 'engine', 'transmission', 'tyre_size']

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'placeholder': 'Enter the Category name','class': 'form-control'}),
        }

class ServiceListForm(forms.ModelForm):
    class Meta:
        model = ServiceList
        fields = [ 'service_name','service_category','description' ,'service_Image','tasks']
        widgets = {
             'service_name': forms.TextInput(attrs={'placeholder': 'Enter the Service name','class': 'form-control'}),
             'service_category': forms.Select(attrs={'class': 'form-control'}),
             'description' : forms.TextInput(attrs={'class': 'form-control'}),
             'service_Image' : forms.ClearableFileInput(attrs={'accept': 'image/*','class': 'form-control file-upload-info'}),
             'tasks': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }


   

class VehicleinfoForm(forms.ModelForm):

    model_variant = forms.ModelChoiceField(queryset=ModelVariant.objects.all(), required=False)

    class Meta:
        model = Vehicleinfo
        fields = ['vehicle_Regno','model_variant']



class ServiceCenterForm(forms.ModelForm):
     class Meta:
            model =ServiceCenter
            fields =[ 'place','city','pincode','phone_number','latitude','longitude' ]
            widgets = {
            'place': forms.TextInput(attrs={'placeholder': 'Enter the Place ','class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter the City ','class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Enter the Pincode ','class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter the Phone Number ','class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control'}),
        }
            

import random
import string

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

class MangaerAddFrom(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ('email','first_name', 'last_name') 

        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter the Place ','class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter the City ','class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter the Pincode ','class': 'form-control'}),
            }
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(generate_password())
        instance.username = instance.email
        if commit:
            instance.save()
        return instance

class MechanicAddFrom(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ('email','first_name', 'last_name') 

        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter the Email','class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter the First Name ','class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter the Last Name ','class': 'form-control'}),
            }
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(generate_password())
        instance.username = instance.email
        if commit:
            instance.save()
        return instance
    

class ServiceCenterUpdateForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=User.objects.filter(role="MANAGER"),
        widget=forms.Select(attrs={'class': 'form-control'}),)

    class Meta:
        model = ServiceCenter
        fields = ['manager']


class AvailableMechanicChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = forms.Select(attrs={'class': 'form-control'})
        super().__init__(*args, **kwargs)
    def label_from_instance(self, obj):
        return obj.get_full_name()

class ServicesSlotsForm(forms.ModelForm):
    class Meta:
        model = ServicesSlots
        fields = ['slotname', 'allocated_mech']
        widgets = {
            'slotname': forms.TextInput(attrs={'placeholder': 'Enter the Slot Name','class': 'form-control'}),
            'allocated_mech': forms.Select(attrs={'class': 'form-control'}),
            }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['allocated_mech'] = AvailableMechanicChoiceField(queryset=self.get_available_mechanics())

    
    def get_available_mechanics(self):
        service_center_instance = self.user.servicecenter
        mechanic_list = mechanicList.objects.filter(service_center=service_center_instance).values_list('mechanic', flat=True)
        existing_slot = ServicesSlots.objects.values_list('allocated_mech', flat=True)
        allocated_mechanics = Client.objects.filter(pk__in=existing_slot)
        available_mechanics = Client.objects.filter(pk__in=mechanic_list).exclude(pk__in=allocated_mechanics)
        
        return available_mechanics

    def clean(self):
        cleaned_data = super().clean()
        service_center_instance = self.user.servicecenter
        cleaned_data['service_center'] = service_center_instance
        allocated_mech = cleaned_data.get('allocated_mech')
        existing_slot = ServicesSlots.objects.filter(allocated_mech=allocated_mech, service_center=service_center_instance).exclude(pk=self.instance.pk).first()
        if existing_slot:
            raise forms.ValidationError("Mechanic is already associated with another slot in this service center.")

        return cleaned_data
    


class SlotsMechAddForm(forms.Form):
    slotslug = forms.CharField()
    class Meta:
        fields = ['Mechanic','slotslug']
        widgets = {
            'Mechanic': forms.Select(attrs={'class': 'form-control'}),
            }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['Mechanic'] = AvailableMechanicChoiceField(queryset=self.get_available_mechanics())

    
    def get_available_mechanics(self):
        service_center_instance = self.user.servicecenter
        mechanic_list = mechanicList.objects.filter(service_center=service_center_instance).values_list('mechanic', flat=True)
        existing_slot = ServicesSlots.objects.values_list('allocated_mech', flat=True)
        allocated_mechanics = Client.objects.filter(pk__in=existing_slot)
        available_mechanics = Client.objects.filter(pk__in=mechanic_list).exclude(pk__in=allocated_mechanics)
        
        return available_mechanics

class ServicePriceForm(forms.ModelForm):
    class Meta:
        model = ServicePrice
        fields = ['variant', 'service', 'price']
        widgets = {
            'price': forms.TextInput(attrs={'placeholder': 'Enter the Price','class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'variant': forms.Select(attrs={'class': 'form-control'}),
            }
 

class VehicleaddForm(forms.ModelForm):
    make_company = forms.ModelChoiceField(
        queryset=CarMake.objects.all(),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Select the Make', 'class': 'form-control'})
    )
    model_name = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Select the Model', 'class': 'form-control'})
    )
    model_variant = forms.ModelChoiceField(
        queryset=ModelVariant.objects.all(),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Select the Variant', 'class': 'form-control'})
    )

    class Meta:
        model = Vehicleinfo
        fields = ['vehicle_Regno', 'make_company', 'model_name', 'model_variant']
        widgets = {
            'vehicle_Regno': forms.TextInput(attrs={'placeholder': 'Enter the Registration Number', 'class': 'form-control'}),
        }

class VehiclecostForm(forms.Form):
    make_company = forms.ModelChoiceField(
        queryset=CarMake.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    model_name = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    model_variant = forms.ModelChoiceField(
        queryset=ModelVariant.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        fields = ['make_company','model_name', 'model_variant']



class AvailableslotChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = forms.Select(attrs={'class': 'form-control'})
        super().__init__(*args, **kwargs)
    def label_from_instance(self, obj):
        return obj.get_full_name()

#///////////////////// FORMS FOR BLOG START ////////////////////////////////
from tinymce.widgets import TinyMCE
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video']
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['accept'] = 'image/*'
        self.fields['video'].widget.attrs['accept'] = 'video/*'
#\\\\\\\\\\\\\\\\\\\\\ FORMS FOR BLOG END   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#///////////////////// FORM FOR TASK ///////////////////////////////////////
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name']
        widgets = {
            'task_name': forms.TextInput(attrs={'placeholder': 'Enter The Service Task', 'class': 'form-control'}),
        }