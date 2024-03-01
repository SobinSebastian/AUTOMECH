from . forms import *
from . models import *
import sweetify
from django.views import View
from django.http import JsonResponse
from .decorators import manager_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect, get_object_or_404
from django.core.serializers import serialize
def mechanic_dashboard (request):
    mech = request.user
    center_details = mechanicList.objects.get(mechanic =mech)
    context ={
        'center_details':center_details
    }
    return render (request,'mechanic/dashboard.html',context)


def mechanic_slot(request):
    slot= ServicesSlots.objects.get(allocated_mech=request.user)
    orders=ServiceOrder.objects.filter(service_slot=slot)
    context ={
        'slot' : slot,
        'orders': orders 
    }
    return render(request,'mechanic/mech_slot.html',context)


def service_orders(request):
    service_orders = ServiceOrder.objects.all()
    context ={
        ' service_orders': service_orders
    }
    return render(request,'mechanic/service_orders.html',context)

def service_details(request, service_slug):
    order = ServiceOrder.objects.get(slug=service_slug)
    order_items = ServiceOrderItem.objects.filter(service_order=order)
    completed_count = order_items.filter(status='completed').count()
    total_items = order_items.count()
    completed_percentage = (completed_count / total_items) * 100
    if order.status == 'pending':
        order.status = 'processing'
        order.save()
    context = {
        'order': order,
        'order_items' : order_items,
        'completed_percentage' : completed_percentage
        }
    return render(request, 'mechanic/service_details.html',context)


def start_order(request, order_slug):
    order = ServiceOrderItem.objects.get(slug=order_slug)
    if order.status == 'created':
        order.status = 'pending'
        order.save()
        sweetify.toast(request, 'Service order has started processing', timer=3000)
    elif order.status == 'pending':
        order.status = 'completed'
        order.save()
        sweetify.toast(request, 'Service order has Completed', timer=3000)
    service_slug_value=order.service_order.slug
    return redirect('service_details', service_slug=service_slug_value)


class ServiceOrderJsonView(View):
    def get(self, request, *args, **kwargs):
        service_orders = ServiceOrder.objects.all()
        events = []
        for order in service_orders:
            events.append({
                'id': order.id,
                'resourceId': order.service_slot.id if order.service_slot else None,
                'start': f"{order.date}T{order.time}",
                'title': f"{order.vehicle.vehicle_Regno} - {order.service_center.place}",
                'status': order.status,
                'url': f"/path/to/detail/view/{order.id}/"  # Add the actual URL to view details
            })

        return JsonResponse(events, safe=False)


class ServiceSlotJsonView(View):
     def get(self, request, *args, **kwargs):
        # Modify this based on your ServicesSlots model structure
        service_slots = ServicesSlots.objects.all()
        resources = [{'id': slot.id, 'title': str(slot.slotname)} for slot in service_slots]
        return JsonResponse(resources, safe=False)