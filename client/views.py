from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.conf import settings
from .forms import *
from .admin_views import *
from .manager_views import *
from .cart_views import *
from .mechanic_views import *
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import razorpay
def index(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
           return redirect('admin_home')
        elif request.user.role == 'MECHANIC':
           return redirect('/mechanic_index')
        elif request.user.role == 'MANAGER':
           return redirect('manager_home')
        if not UserInfo.objects.filter(client=request.user).exists():
            return redirect('profile_setup')
    categories = ServiceCategory.objects.all()
    # services = ServiceList.objects.all()
    make = CarMake.objects.all()
    context={'categories':categories,'makes':make}
    return render(request,'client/index.html',context)
    
def profilesetup(request):
   return render(request,'account/profilesetup.html') 

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomSignupForm
    def form_valid(self, form):
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        confirmpassword = form.cleaned_data['password2']
        email=username
        print(username)
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.error(self.request, 'User with this email already exists. Please sign in.')
                return redirect('account_login')
            else:
                user = Client.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
                # Additional logic for sending email
                subject = 'Subject of the email'
                message = 'Body of the email'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)

                return redirect('account_login')  # Replace with the URL for your login page
        else:
            # Handle the case when passwords don't match
            messages.error(self.request, 'Passwords do not match.')
            return redirect('/')
        


@login_required
def profileview(request):
    user=request.user
    id=user.id
    user_to_update = User.objects.get(id=id)
    #user_info = UserInfo.objects.get(user=user_to_update)
    try:
        user_info = UserInfo.objects.get(client=user_to_update)
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            form1 = ProfileImage(request.POST,request.FILES) 
            if form1.is_valid():
                user_info.profile_picture=form1.cleaned_data['profile_picture']
                user_info.save()  
                return redirect('account_profile')
            if form.is_valid():
                user_to_update.first_name =form.cleaned_data['f_name']
                user_to_update.last_name = form.cleaned_data['l_name']
                user_info.user=user
                user_info.contact_no = form.cleaned_data['contact_no']
                user_info.address = form.cleaned_data['address']
                user_info.place = form.cleaned_data['place']
                user_info.city = form.cleaned_data['city']
                user_info.district = form.cleaned_data['district']
                user_info.pincode = form.cleaned_data['pincode']
                user_info.save()
                user_to_update.save()
                return redirect('account_profile')
        else:
            form = ProfileForm()
            form1 = ProfileImage()
        response=render(request,'client/profile.html',{'form':form,'form1':form1,'uinfo':user_info})
        response['Cache-Control']='no-store,must-revalidate'
        return response

    except UserInfo.DoesNotExist:
        user_info = UserInfo()
        form = ProfileForm(request.POST)
        form1 = ProfileImage(request.POST,request.FILES) 
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            form1 = ProfileImage(request.POST,request.FILES) 
            if form1.is_valid():
                user_info.profile_picture=form1.cleaned_data['profile_picture']
                user_info.save()  
                return redirect('account_profile')
            if form.is_valid():
                user_to_update.first_name =form.cleaned_data['f_name']
                user_to_update.last_name = form.cleaned_data['l_name']
                user_info.client=user
                user_info.contact_no=form.cleaned_data['contact_no']
                user_info.place=form.cleaned_data['place']
                user_info.city=form.cleaned_data['city']
                user_info.district=form.cleaned_data['district']
                user_info.pincode=form.cleaned_data['pincode']
                user_info.save()
                user_to_update.save()
                return redirect('account_profile')
        messages.warning(request, 'Please Update Your Details!')
        response=render(request,'client/profile.html',{'form':form,'form1':form1})
        response['Cache-Control']='no-store,must-revalidate'
        return response



def add_vehicle(request):
    if request.method == "POST":
       form = VehicleaddForm(request.POST)
       form.instance.client = request.user
       if form.is_valid():
            form.save()
    else:
        form = VehicleaddForm()
    context =  {'form': form,'all_car_makes' : CarMake.objects.all()}
    return render(request, 'client/add_vehicle.html', context)

def edit_vehicle(request, id):
   vehicle = Vehicleinfo.objects.get(id=id)
   if request.method == "POST":
       form = AddVehicleForm(request.POST, instance=vehicle)
       form.instance.client = request.user
       if form.is_valid():
           form.save()
           return redirect('vehicle')
   else:
       form = AddVehicleForm(instance=vehicle)
   return render(request, 'client/edit_vehicle.html', {'form': form})



def vehicle(request):
    vehicleinfo=Vehicleinfo.objects.filter(client=request.user)
    print(vehicleinfo)
    return render(request,'client/vehicle.html',{'vehicles':vehicleinfo})


def map_view(request):
    service_centers = ServiceCenter.objects.all()
    return render(request, 'client/map_view.html', {'service_centers': service_centers})

def get_category_data(request, category_slug):
    variant = None
    vehicle = None
    if request.user.is_authenticated:
        vehicle = get_object_or_404(Vehicleinfo, client=request.user)
        variant = vehicle.model_variant
    category = get_object_or_404(ServiceCategory, slug=category_slug)
    category_data = ServiceList.objects.filter(service_category=category)
    service_prices = ServicePrice.objects.filter(variant=variant)
    services_with_prices = []
    for service in category_data:
        price = next((price for price in service_prices if price.service == service), None)
        if price:
            services_with_prices.append((service, price))
        else:
            services_with_prices.append((service,price))
    context = {
        'services': services_with_prices,
        'variant' : variant,
        'cat':category,
        'vehicle' : vehicle
    }
    return render(request, 'client/partials/servicecard.html', context)


def get_car_models(request, make_id):
    car_models = CarModel.objects.filter(make_company__pk=make_id)
    data = serializers.serialize('json', car_models)
    return JsonResponse(data, safe=False)

def get_model_variants(request):
    model_id = request.GET.get('model_id')
    if model_id:
        variants = ModelVariant.objects.filter(model_id=model_id)
        data = [{'id': variant.id, 'name': variant.variant_name} for variant in variants]
    else:
        data = []
    return JsonResponse({'variants': data})

def get_models(request):
    make_id = request.GET.get('make_id')
    if make_id:
        models = CarModel.objects.filter(make_company_id=make_id)
        data = [{'id': model.id, 'name': model.model_name} for model in models]
    else:
        data = []
    return JsonResponse({'models': data})


def step1_view(request):
    if request.method == 'POST':
        user =  request.user
        user_info = UserInfo()
        form = ProfilesetupForm(request.POST)
        if form.is_valid():
            user_info.contact_no =  form.cleaned_data['contact_no']
            user_info.address = form.cleaned_data['address']
            user_info.place = form.cleaned_data['place']
            user_info.city = form.cleaned_data['city']
            user_info.district = form.cleaned_data['district']
            user_info.pincode = form.cleaned_data['pincode']
            user_info.client=user   
            user_info.save()
            return redirect('step2_view')
    else:
        form = ProfilesetupForm()
    return render(request, 'account/step1.html', {'form': form})

def step2_view(request):
    if request.method == 'POST':
        form = VehicleaddForm(request.POST)
        if form.is_valid():
            reg_no = form.cleaned_data['vehicle_Regno']
            variant_id = form.cleaned_data['model_variant']
            
            # Assuming request.user is the current user
            vehicle_info = Vehicleinfo(
                client=request.user,
                model_variant=variant_id,  # Assign variant_id directly
                vehicle_Regno=reg_no
            )
            vehicle_info.save()
            sweetify.toast(request, 'Completed', icon='error', timer=3000)
            return redirect('index')

    else:
        form = VehicleaddForm()
    return render(request, 'account/step2.html', {'form': form})

def servicecost_estimation(request):
    variant = None
    if request.method == "POST":
        model_variant_id = request.POST.get('model_variant')
        variant = ModelVariant.objects.get(id =  model_variant_id)
    services = ServiceList.objects.all()
    service_prices = ServicePrice.objects.none()
    if variant:
        service_prices = ServicePrice.objects.filter(variant=variant)
    services_with_prices = []
    for service in services:
        price = next((price for price in service_prices if price.service == service), None)
        if price:
            services_with_prices.append((service, price))
        else:
            services_with_prices.append((service,  0.0))
    make_companys = CarMake.objects.all()
    model_names= CarModel.objects.all()
    model_variants = ModelVariant.objects.all()
    context = {
        'services_with_prices': services_with_prices,
        'make_companys': make_companys,
        'model_names' : model_names,
        'model_variants' : model_variants 
    }
    return render(request, 'client/servicecost_estimation.html', context)


@receiver(user_logged_in)
def set_default_vehicle(sender, user, request, **kwargs):
    try:
        default_vehicle = Vehicleinfo.objects.filter(client=user).first()
        if default_vehicle:
            request.session['selected_vehicle'] = default_vehicle.id
    except Vehicleinfo.DoesNotExist:
        pass

from geopy.distance import geodesic

def rsa (request):
    user =request.user
    vehicles = Vehicleinfo.objects.filter(client = user)
    service_centers = ServiceCenter.objects.all()
    if request.method == "POST":
        vehicle_info_id = request.POST.get('vehicle_info')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        description = request.POST.get('description')
        print(latitude)
        print(longitude)
        # Calculate the distance for each service center and store it in a dictionary
        distances = {}
        user_location = (latitude, longitude)
        for center in service_centers:
            center_location = (float(center.latitude), float(center.longitude))
            dist = geodesic(user_location, center_location).kilometers
            distances[center.id] = dist

            # Find the nearest service center
        nearest_center_id = min(distances, key=distances.get)
        
        nearest_service_center = ServiceCenter.objects.get(id=nearest_center_id)
        rsa_request = RoadsideAssistance.objects.create(
            vehicle_info_id=vehicle_info_id,
            service_center=nearest_service_center,
            latitude=latitude,
            longitude=longitude,
            status='requested',  # You can set the default status or adjust as needed
            description=description,
        )
        print("Nearest Service Center:", nearest_service_center.place)

    return render (request,'client/rsa.html',{'service_centers': service_centers,'vehicles':vehicles})

from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def custom_logout(request):
    logout(request)
    return render(request, 'client/logout.html')