from . forms import *
from . models import *
import sweetify
from django.views import View
from django.http import JsonResponse
from .decorators import manager_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect, get_object_or_404

@manager_required
def manager_dashboard(request):
    user = request.user
    center = ServiceCenter.objects.get(manager = user)
    context ={'center':center}
    return render(request, 'manager/manager_dashboard.html',context)


def available_mechanics(user):
    service_center_instance = user.servicecenter
    mechanic_list = mechanicList.objects.filter(service_center=service_center_instance).values_list('mechanic', flat=True)
    existing_slot = ServicesSlots.objects.values_list('allocated_mech', flat=True)
    
    allocated_mechanics = Client.objects.filter(pk__in=existing_slot)
    available_mechanics = Client.objects.filter(pk__in=mechanic_list).exclude(pk__in=allocated_mechanics)
    return available_mechanics.count()

# def manager_slots(request):
#     if request.method == 'POST':
#         form = ServicesSlotsForm(request.POST,user=request.user)
#         if form.is_valid():
#             form.instance.service_center = request.user.servicecenter
#             form.save()
#             return redirect('service_slots') 
#     else:
#         form = ServicesSlotsForm(user=request.user)
#     mcount = available_mechanics(request.user)
#     service_slots =  ServicesSlots.objects.filter(service_center=request.user.servicecenter)
#     form1 = SlotsMechAddForm(user=request.user)        
#     context = {
#         'form': form , 
#         'mcount': mcount,
#         'service_slots' : service_slots,
#         'form1' : form1
#         }
#     return render(request, 'manager/manager_slots.html',context)

def manager_slots(request):
    if request.method == 'POST':
        # Handling ServicesSlotsForm
        form = ServicesSlotsForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.service_center = request.user.servicecenter
            form.save()
            return redirect('service_slots')

        # Handling SlotsMechAddForm
        form1 = SlotsMechAddForm(request.POST, user=request.user)
        if form1.is_valid():
            slug = request.POST.get('slotslug')
            man_id = request.POST.get('Mechanic')
            mech = User.objects.get(id = man_id)
            services_slot = get_object_or_404(ServicesSlots, slug=slug)
            services_slot.allocated_mech = mech
            services_slot.save()
        return redirect('service_slots')
    
    else:
        form = ServicesSlotsForm(user=request.user)
        form1 = SlotsMechAddForm(user=request.user)

    mcount = available_mechanics(request.user)
    service_slots = ServicesSlots.objects.filter(service_center=request.user.servicecenter)

    context = {
        'form': form,
        'mcount': mcount,
        'service_slots': service_slots,
        'form1': form1,
    }

    return render(request, 'manager/manager_slots.html', context)


def remove_alloc_mech(request, solt_slug):
    services_slot = get_object_or_404(ServicesSlots, slug = solt_slug)
    services_slot.allocated_mech = None
    services_slot.save()
    return redirect('service_slots')

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


@csrf_exempt
def check_unique_slotname(request):
    if request.method == 'POST':
        service_center_id = ServiceCenter.objects.get(manager = request.user)
        slotname = request.POST.get('slotname')
        existing_slot = ServicesSlots.objects.filter(service_center_id=service_center_id, slotname=slotname).exists()

        return JsonResponse({'unique': not existing_slot})

    return JsonResponse({'error': 'Invalid request method'})


def manager_bookings(request):
    return render(request, 'manager/manager_booking.html')

def manager_rsa(request):
    return render(request, 'manager/manager_rsa.html')
