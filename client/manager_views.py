from . forms import *
from . models import *
import sweetify
from django.views import View
from django.shortcuts import render,redirect, get_object_or_404
from .decorators import manager_required

@manager_required
def manager_dashboard(request):
    user = request.user
    center = ServiceCenter.objects.get(manager = user)
    print (center)
    context ={'center':center}
    return render(request, 'manager/manager_dashboard.html',context)

def manager_slots(request):
    return render(request, 'manager/manager_slots.html')

def manager_mechanic(request):
    user = request.user
    service_center_instance = ServiceCenter.objects.get(manager = user)
    if request.method == 'POST':
        form = MechanicAddFrom(request.POST)
        if form.is_valid():
            client_instance = form.save()
            mechanic_list_instance = mechanicList.objects.create(
                mechanic=client_instance,
                service_center=service_center_instance,)
            sweetify.success(request, 'New Mechanic', text= f'is successfully Added',timer=5000, persistent=False,)
            return redirect('manager_mechanic')

    else:
        form = MechanicAddFrom()
    mec_list = mechanicList.objects.filter(service_center=service_center_instance)
    context = {
        'form' : form,
        'mechanics' : mec_list,
    }
    return render(request, 'manager/manager_mechanic.html',context)

def manager_bookings(request):
    return render(request, 'manager/manager_booking.html')

def manager_rsa(request):
    return render(request, 'manager/manager_rsa.html')
