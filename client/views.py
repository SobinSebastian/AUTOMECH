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

def index(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
           return redirect('admin_home')
        elif request.user.role == 'MECHANIC':
           return redirect('/mechanic_index')
    categories = ServiceCategory.objects.all()
    make = CarMake.objects.all()
    context={'categories':categories,'makes':make}
    return render(request,'client/index.html',context)
     
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
       form = VehicleinfoForm(request.POST)
       form.instance.client = request.user
       if form.is_valid():
            form.save()
   else:
        form = VehicleinfoForm()
   return render(request, 'client/add_vehicle.html', {'form': form})

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
    return render (request,'client/map_view.html')



def ajax_load_services(request, category_slug):
    try:
        category = get_object_or_404(ServiceCategory, slug=category_slug)
        services = ServiceList.objects.filter(service_category=category)

        data = {'services': []}
        for service in services:
            service_data = {
                'name': service.service_name,
                'description': service.description,
                'image_url': service.service_Image.url if service.service_Image else None
            }
            data['services'].append(service_data)

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def get_car_models(request, make_id):
    car_models = CarModel.objects.filter(make_company__pk=make_id)
    data = serializers.serialize('json', car_models)
    return JsonResponse(data, safe=False)

def get_car_variants(request, model_id):
    car_variants = ModelVariant.objects.filter(model__pk=model_id)
    data = serializers.serialize('json', car_variants)
    return JsonResponse(data, safe=False)

