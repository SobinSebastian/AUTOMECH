from . forms import *
from . models import *
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views import main as default_admin_index
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import CarMake
from .forms import CarMakeForm


def is_admin(user):
    return user.is_staff

@staff_member_required
def admin_dashboard(request):
    u_count = User.objects.filter(is_active=True).count()
    mcount = User.objects.filter(role=User.Role.MECHANIC).count()
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
    return render(request, 'admin/admin_dashboard.html', {'bookings':'','ucount': u_count, 'mcount': mcount, 'actions': recent_actions,'tbooking':bookings_today,'total':total,'per':percentage})


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


def service_category(request, slug=None):
    cat = ServiceCategory.objects.all()
    
    if slug:
        instance = get_object_or_404(ServiceCategory, slug=slug)
        button_text = 'Update'
    else:
        instance = ServiceCategory()
        button_text = 'Add'
        
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('service_category')
    else:
        form = ServiceCategoryForm(instance=instance)
    
    context = {'form': form, 'Categories': cat,'buttontext':button_text}
    return render(request, 'admin/servicecategory.html', context)

def service_category_list(request, slug=None):
    cat= get_object_or_404(ServiceCategory, slug=slug)
    serviceList = ServiceList.objects.filter(service_category=cat.id)
    if request.method == 'POST':
        form = ServiceListForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ServiceListForm()
    context={'ServiceLists':serviceList,'service_category':cat,'form':form}
    return render(request, 'admin/servicecategorylist.html', context)

def service_category_view(request, slug=None):
    service = get_object_or_404(ServiceList, slug=slug)
    context = {'service':service}
    return render(request, 'admin/serviceview.html', context)

@staff_member_required
def client_list_view(request):
    users = User.objects.filter(role=User.Role.CLIENT)
    userinfo=UserInfo
    return render(request,'admin/clientlist.html',{'users': users,'userinfo':userinfo})