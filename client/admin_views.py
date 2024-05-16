from . forms import *
from . models import *
from django.views import View
from django.utils import timezone
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views import main as default_admin_index
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import CarMake
from .forms import CarMakeForm
from .email_content import *
import sweetify


def is_admin(user):
    return user.is_staff

from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
@staff_member_required
def admin_dashboard(request):
    #user count
    u_count = User.objects.filter(role=User.Role.CLIENT).count()
    mcount = User.objects.filter(role=User.Role.MECHANIC).count()
    man_count = User.objects.filter(role=User.Role.MANAGER).count()
    #order
    order_no = ServiceOrder.objects.count()
    rsa_no = ServiceOrder.objects.filter(service_type='rsa').count()
    nor_oder_num = ServiceOrder.objects.filter(service_type='normal').count()
    #profit
    total_price = 0
    rsa_price = 0
    nor_price = 0
    closed_orders = ServiceOrder.objects.filter(status='closed')
    for i in closed_orders:
        total_price = total_price + i.price
    recent_actions = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
    today = timezone.now().date()
    bookings_today =10 
    # ServiceBooking.objects.filter(booking_date=today).count()
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
    bookings_30_days =7
    # ServiceBooking.objects.filter(booking_date__gte=thirty_days_ago).count()
    total=34 
    # ServiceBooking.objects.count()
    percentage= (bookings_30_days / total) * 100
    #bookings=ServiceBooking.objects.all().order_by('booking_date')
    no_centers = ServiceCenter.objects.count()
    context ={
        'bookings':'',
        'ucount': u_count, 
        'mcount': mcount,
        'man_count' : man_count,
        'order_no'  : order_no,
        'rsa_no'    : rsa_no,
        'nor_oder_num'  : nor_oder_num,
        'actions': recent_actions,
        'tbooking':bookings_today,
        'total':total,
        'per':percentage
    }
    return render(request, 'admin/admin_dashboard.html', context)


@staff_member_required
class CarModelCreateView(CreateView):
    model = CarModel
    form_class = CarModelForm
    template_name = 'admin/car_model_form.html'
    success_url = reverse_lazy('admin:car_model_create')

class FueltypeCreateView(CreateView):
    model = Fueltype
    form_class = FueltypeForm
    template_name = 'admin/fueltype_form.html'
    success_url = reverse_lazy('admin_home')

class ModelVariantCreateView(CreateView):
    model = ModelVariant
    form_class = ModelVariantForm
    template_name = 'admin/model_variant_form.html'
    success_url = reverse_lazy('admin:model_variant_create')


class CarModelListView(ListView):
    model = CarModel
    template_name = 'admin/car_model_list.html'
    context_object_name = 'car_models'

class FueltypeListView(ListView):
    model = Fueltype
    template_name = 'admin/fueltype_list.html'
    context_object_name = 'fueltypes'

class ModelVariantListView(ListView):
    model = ModelVariant
    template_name = 'admin/model_variant_list.html'
    context_object_name = 'model_variants'

class VehicleinfoListView(ListView):
    model = Vehicleinfo
    template_name = 'admin/vehicleinfo_list.html'
    context_object_name = 'vehicleinfos'

class CarMakes(CreateView, ListView):
    model = CarMake
    form_class = CarMakeForm
    template_name = 'admin/car_make_form.html'
    success_url = reverse_lazy('car_make')
    context_object_name = 'car_makes'

    @method_decorator(staff_member_required, cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0))
    def dispatch(self, *args, **kwargs):
       return super().dispatch(*args, **kwargs)
    
class CarMakeUpdateView(UpdateView,ListView):
    model = CarMake
    form_class = CarMakeForm
    template_name = 'admin/car_make_editform.html'
    success_url = reverse_lazy('car_make')
    slug_field = 'make_slug'  # Adjust this to your actual slug field name
    slug_url_kwarg = 'make_slug' 
    context_object_name = 'car_make'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class CarModels(CreateView, ListView):
    model = CarModel
    form_class = CarModelForm
    template_name = 'admin/car_model.html'
    success_url = reverse_lazy('car_model')
    context_object_name = 'car_models'
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
       return super().dispatch(*args, **kwargs)
    

@staff_member_required
def ModelsMake(request):
    make=None
    if request.method == 'POST':
        make_id = request.POST.get('make_id')
        if(make_id):
            make = get_object_or_404(CarMake, id=make_id)
        if request.method == "POST":
            form =ModelVariantForm (request.POST)
            if form.is_valid():
                form.save()    
                model=form.cleaned_data['model']
                car_model = CarModel.objects.get(model_name=model)
                manu = car_model.make_company
                make = manu
            form1 = CarModelForm(request.POST, request.FILES)
            if form1.is_valid():
                form1.save()
                make = form1.cleaned_data['make_company']
        else:
            form = ModelVariantForm()
            form1 = ModelVariantForm()
        models_list=CarModel.objects.filter(make_company = make)
        context = {'car_models':models_list,'make':make,'form':form,'form1':form1}
    return render(request, "admin/car_makes_model.html",context)



@staff_member_required
def Car_variant_view(request):
    model =None
    if request.method == 'POST':
        model_id = request.POST.get('model_id')
        if model_id :
            model = get_object_or_404(CarModel, id=model_id)
        if request.method == "POST":
            form = ModelVariantForm (request.POST)
            if form.is_valid():
                form.save()    
                m=form.cleaned_data['model']
                model = get_object_or_404(CarModel, model_name = m)
        else:
            form = ModelVariantForm()
       
        variants = ModelVariant.objects.filter(model = model)
        context ={'variants': variants,'model':model,'form':form}
        
    return render(request,"admin/car_variant.html",context)

@staff_member_required
def service_category(request, slug=None):
    cat = ServiceCategory.objects.all()
    
    if slug:
        instance = get_object_or_404(ServiceCategory, slug=slug)
        button_text = 'Update'
        msg = "ServiceCategory Is Updated"
    else:
        instance = ServiceCategory()
        button_text = 'Add'
        msg = "New ServiceCategory Is Added"
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            sweetify.toast(request, f'{msg}')
            return redirect('service_category')
        else:
            print(form.errors) 
            sweetify.toast(request, f'Service category with this Category name already exists.', icon='error', timer=3000)
            
    else:
        form = ServiceCategoryForm(instance=instance)
    
    context = {'form': form, 'Categories': cat,'buttontext':button_text}
    return render(request, 'admin/servicecategory.html', context)

@staff_member_required
def service_category_list(request, slug=None):
    cat= get_object_or_404(ServiceCategory, slug=slug)
    serviceList = ServiceList.objects.filter(service_category=cat.id).order_by('service_name')
    if request.method == 'POST':
        form = ServiceListForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ServiceListForm()
    context={'ServiceLists':serviceList,'service_category':cat,'form':form}
    return render(request, 'admin/servicecategorylist.html', context)
@staff_member_required
def service_category_view(request, slug=None):
    s_tasks = Task.objects.all()
    service = get_object_or_404(ServiceList, slug=slug)
    if request.method == 'POST':
        form = ServiceListForm(request.POST,request.FILES,instance = service)
        if form.is_valid():
            form.save()
    else:
        form = ServiceListForm(instance = service )
    context = {'service':service,'form': form,'s_tasks':s_tasks}
    return render(request, 'admin/serviceview.html', context)

@staff_member_required
def client_list_view(request):
    users = User.objects.filter(role=User.Role.CLIENT)
    userinfo=UserInfo
    return render(request,'admin/clientlist.html',{'users': users,'userinfo':userinfo})

@staff_member_required
def service_center_add(request):
    if request.method == 'POST':
        form = ServiceCenterForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'New Service Ceneter Is Added')
    else:
        form = ServiceCenterForm()
    context ={'form':form}
    return render(request,'admin/service_center_add.html',context)

@staff_member_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def service_center_view(request):
    form = ServiceCenterUpdateForm()
    if request.method == 'POST':
        slug = request.POST.get('service_center_slug')
        man_id= request.POST.get('manager')
        manager = Manager.objects.get(id = man_id)
        center = ServiceCenter.objects.get(slug=slug)
        center.manager = manager
        center.save()        
        sweetify.success(request, 'New Manager is Assigned')
        return redirect('service_center_view')

    ServiceCenters = ServiceCenter.objects.all()
    count = ServiceCenters.count()
    context ={'ServiceCenters':ServiceCenters,'form' : form,'count' : count}
    return render(request,'admin/service_center_view.html',context)


@staff_member_required
def service_center_details(request, slug):
    if slug :
        center = ServiceCenter.objects.get(slug=slug)
        slots = ServicesSlots.objects.filter(service_center=center)
    else :
        center = None
    context= { 'center' : center,
              'slots' : slots}
    return render (request,'admin/service_center_details.html',context)





# Example usage:
#employee_mail(['sobinolickal1936@gmail.com'])

@staff_member_required
def service_center_manager(request):
    if request.method == 'POST':
        form = MangaerAddFrom(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email'] 
            form.save()
            employee_mail([email])

            sweetify.success(request, 'New Manager', text= f'is successfully Added',timer=5000, persistent=False,)
    else:
        form = MangaerAddFrom()
    managers = Manager.objects.filter( role = 'MANAGER')
    context = {'form':form,'managers': managers}
    return render(request,'admin/service_center_manager.html',context)



def variant_service(request):        
    context  = {'form' : ServicePriceForm()  }
    return render(request,"admin/car_variant_service.html",context)

def create_service_form(request):
    if request.method == 'POST':
        form =  ServicePriceForm(request.POST or None)
        if form.is_valid():
            form.save()
    return render(request,"admin/partials/addserviceform.html",{'form' : ServicePriceForm()} )




@staff_member_required
def variant_serviceprice_view(request,slug=None):
    model =None
    variant = None
    variant = get_object_or_404(ModelVariant, variant_slug=slug)
    if request.method == "POST":
        form2 = PriceFormchange (request.POST)
        form = ServicePriceForm (request.POST)
       
        if form.is_valid():
            form.save()
            sweetify.toast(request, f'New Service Is Added for  {variant}', icon='success', timer=3000)
        else :
            sweetify.toast(request, 'Already In the list', icon='error', timer=3000)
        if form2.is_valid():
            p = form2.cleaned_data['price']
            val = request.POST.get('slugval')
            ser_price = ServicePrice.objects.get(slug=val)
            ser_price.price =p
            from decimal import Decimal
            if Decimal(p) <= 0 :
                sweetify.toast(request, ' Invalid Price', icon='error', timer=3000)
            else :
                ser_price.save()
                sweetify.toast(request, f' Service Is Updated for  {ser_price}', icon='success', timer=3000)
        return redirect('car_variant_service', slug=variant.variant_slug)
    else:
        form = ServicePriceForm()
        form2 = PriceFormchange()
       
        price_list = ServicePrice.objects.filter(variant = variant)
        context ={
                'variant': variant,
                'price_list':price_list,
                'form':form,
                'form2':form2,
                }
        
        return render(request,"admin/variant_price.html",context)



#/////////////////////////////  VIEWS FOR BLOG  START /////////////////////////////////////////////////
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def view_blog (request):
    posts = Post.objects.all()
    context ={
        'posts':posts
    }
    return render(request,'admin/blog.html',context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def blog_details (request,blog_slug):
    post = Post.objects.get(slug = blog_slug)
    context={
        'post':post
    }
    return render(request,'admin/blog_details.html',context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def create_or_edit_post(request, slug=None):
    post = get_object_or_404(Post, slug=slug) if slug else None

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            sweetify.toast(request, 'Post is Updated', icon='success', timer=3000)
            return redirect('admin_blog')
    else:
        form = PostForm(instance=post)

    template_name ='admin/create_post.html'
    return render(request, template_name, {'form': form, 'post': post})
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\  VIEWS FOR BLOG END    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ TASK \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)   
def TaskListViewAndCreateView(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.toast(request, 'Service Task Is Added', icon='success', timer=3000)
            return redirect('task_list_create_update')
    else:
        form = TaskForm()

    tasks = Task.objects.all()
    context = {
        'form': form,
        'tasks': tasks,
    }
    return render(request, 'admin/task_list_create_update.html', context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def TaskListUpdateView(request, slug=None):
    if slug:
        task = get_object_or_404(Task, slug=slug)
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                sweetify.toast(request, 'Service Task Is Updated', icon='success', timer=3000)
                return redirect('task_list_create_update')
            




#//////////////////////////////// VIEWS FOR EXCEL UPLOAD  ////////////////////////////////////////////////
from django.http import HttpResponse
from django.template.loader import get_template
from xlsxwriter.workbook import Workbook
def download_excel_with_headers(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="model_variants_template.xlsx"'

    workbook = Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Add headers
    headers = ['Model', 'Fuel Type', 'Torque', 'BHP', 'Engine', 'Transmission', 'Tyre Size', 'Variant Name']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    fuel_types = Fueltype.objects.all()
    transmission_types = transmissionType.objects.all()
    car_models = CarModel.objects.all()

    # Add fuel types, transmission types, and car models to lists for dropdowns
    fuel_type_list = [fuel.fuel_name for fuel in fuel_types]
    transmission_type_list = [transmission.transmission_name for transmission in transmission_types]
    car_model_list = [model.model_name for model in car_models]

    # Add dropdowns for Fuel Type, Transmission, and Car Model
    worksheet.data_validation(1, 1, 1000, 1, {'validate': 'list',
                                              'source': fuel_type_list,
                                              'input_message': 'Select a Fuel Type'})

    worksheet.data_validation(1, 5, 1000, 5, {'validate': 'list',
                                              'source': transmission_type_list,
                                              'input_message': 'Select a Transmission Type'})

    worksheet.data_validation(1, 0, 1000, 0, {'validate': 'list',
                                              'source': car_model_list,
                                              'input_message': 'Select a Car Model'})


    workbook.close()
    return response

import pandas as pd
def insert_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Read the uploaded Excel file
                df = pd.read_excel(request.FILES['excel_file'])

                # Get fuel types, transmission types, and car models
                fuel_types = Fueltype.objects.all()
                transmission_types = transmissionType.objects.all()
                car_models = CarModel.objects.all()

                # Create dictionaries for quick lookup
                fuel_type_dict = {fuel.fuel_name: fuel.id for fuel in fuel_types}
                transmission_type_dict = {transmission.transmission_name: transmission.id for transmission in transmission_types}
                car_model_dict = {model.model_name: model.id for model in car_models}

                # Iterate over each row in the DataFrame and save data to ModelVariant
                for index, row in df.iterrows():
                    model_name = row['Model']

                    # Skip the row if the model is missing
                    if not model_name or model_name not in car_model_dict:
                        sweetify.toast(request, f"Skipping row {index + 2}: Missing or invalid model name", icon='error', timer=3000)
                        continue

                    # Get the IDs for fuel type and transmission type, handling possible missing values
                    fuel_type_id = fuel_type_dict.get(row.get('Fuel Type', ''), None)
                    transmission_type_id = transmission_type_dict.get(row.get('Transmission', ''), None)

                    # Create the ModelVariant, skipping if any of the required values are missing
                    try:
                        model_variant = ModelVariant.objects.create(
                            model_id=car_model_dict[model_name],
                            fuel_type_id=fuel_type_id,
                            torque=row.get('Torque', ''),
                            bhp=row.get('BHP', ''),
                            engine=row.get('Engine', ''),
                            transmission_id=transmission_type_id,
                            tyre_size=row.get('Tyre Size', ''),
                            variant_name=row.get('Variant Name', '')
                        )
                        sweetify.toast(request, f"Model Variant {model_variant.variant_name} inserted successfully", icon='success', timer=3000)
                    except Exception as e:
                        messages.warning(request, f"Skipping row {index + 2}: {str(e)}")

                return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successful upload
            except Exception as e:
                sweetify.toast(request, f'Error inserting data: {e}')
        else:
            sweetify.toast(request, 'Invalid form submission. Please check your file and try again.')
    else:
        form = ExcelUploadForm()

    return render(request, 'admin/model_excel_input.html', {'form': form})
    
from django.http import JsonResponse
def service_order_events(request):
    service_orders = ServiceOrder.objects.all()
    events = []
    for order in service_orders:
        event = {
            'title': str(order),
            'start': order.date.strftime('%Y-%m-%d') + 'T' + order.time.strftime('%H:%M:%S'),
            'end': None,  # Add end time if necessary
            'allDay': False,  # Adjust as needed
            'className': order.status.lower(),  # Assign class based on status
            'url': f'/service_order/{order.slug}/detail',  # Add URL to view order detail
        }
        events.append(event)
    return JsonResponse(events, safe=False)

def full_schedule(request):
    return render (request,'admin/full.html')