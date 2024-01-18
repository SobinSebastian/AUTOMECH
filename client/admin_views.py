from . forms import *
from . models import *
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views import main as default_admin_index
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import CarMake
from .forms import CarMakeForm


def is_admin(user):
    return user.is_staff

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


class CarMake(CreateView, ListView):
    model = CarMake
    form_class = CarMakeForm
    template_name = 'admin/car_make_form.html'
    success_url = reverse_lazy('car_make')
    context_object_name = 'car_makes'

class CarModel(CreateView, ListView):
    model = CarModel
    form_class = CarModelForm
    template_name = 'admin/car_model.html'
    success_url = reverse_lazy('car_model')
    context_object_name = 'car_models'