from . forms import *
from . models import *
import sweetify
from django.views import View
from django.http import JsonResponse
from .decorators import manager_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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
@manager_required
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
    user =request.user
    mcount = available_mechanics(request.user)
    service_slots = ServicesSlots.objects.filter(service_center=user.servicecenter)

    context = {
        'form': form,
        'mcount': mcount,
        'service_slots': service_slots,
        'form1': form1,
    }

    return render(request, 'manager/manager_slots.html', context)

@manager_required
def remove_alloc_mech(request, solt_slug):
    services_slot = get_object_or_404(ServicesSlots, slug = solt_slug)
    services_slot.allocated_mech = None
    services_slot.save()
    return redirect('service_slots')
@manager_required
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

@manager_required
def manager_bookings(request):
    user = request.user
    center = ServiceCenter.objects.get(manager = user)
    service_orders = ServiceOrder.objects.filter(service_center=center)
    order_items =ServiceOrderItem.objects.all()
    active_service_slots = ServicesSlots.objects.filter(service_center=center,allocated_mech__isnull=False)
    print(active_service_slots)
    context = {
        'service_orders': service_orders,
        'orderitems' : order_items,
        'active_service_slots':active_service_slots
    }
    return render(request, 'manager/manager_booking.html',context)

@manager_required
def manager_bookings_json(request):
    user = request.user
    center = ServiceCenter.objects.get(manager=user)

    # Fetch service orders related to the service center
    service_orders = ServiceOrder.objects.filter(service_center=center)

    # Convert service order data to a format suitable for FullCalendar
    events = []
    for order in service_orders:
        events.append({
            'title': f"{order.vehicle.vehicle_Regno} - {order.service_center.place}",
            'start': str(order.date) + 'T' + str(order.time),
        })

    return JsonResponse(events, safe=False)



@manager_required
def manager_rsa(request):
    return render(request, 'manager/manager_rsa.html')





@require_POST
def allocate_service_slot(request):
    slug = request.POST.get('slug')
    selected_slot = request.POST.get('slot')
    service_order = ServiceOrder.objects.get(slug=slug)
    slot = ServicesSlots.objects.get(id =selected_slot)
    service_order.service_slot = slot
    service_order.status = 'pending'
    service_order.save()
    sweetify.success(request, 'Slot allocated ', text= f'successfully.',timer=5000, persistent=False,)
    # Redirect to a success page or back to the same page
    return redirect('manager_booking')