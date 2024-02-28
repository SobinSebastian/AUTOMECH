from . forms import *
from . models import *
import sweetify
from django.views import View
from django.http import JsonResponse
from .decorators import manager_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect, get_object_or_404

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
    context = {
        'order': order,
        'order_items' : order_items
        }
    return render(request, 'mechanic/service_details.html',context)
