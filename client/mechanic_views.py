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
    rec_details = Servicerecommendation.objects.filter(service_order =  order)
    context = {
        'order': order,
        'order_items' : order_items,
        'completed_percentage' : completed_percentage ,
        'rec_details' : rec_details,
        'form' : ServicerecommendationForm(),
        'addForm' : ServiceMechAddForm()
        }
    return render(request, 'mechanic/service_details.html',context)


def start_order(request, order_slug):
    order = ServiceOrderItem.objects.get(slug=order_slug)
    if order.status == 'created':
        order.status = 'pending'
        order.save()
        if order.service_order.service_type == 'rsa' :
            sp = ServiceOrder.objects.get(id=order.service_order.id)
            service_price = ServicePrice.objects.get(variant=order.vehicle_info.model_variant, service=order.service_list)
            if sp.price is None:
                sp.price = service_price.price
            else:
                sp.price = sp.price + service_price.price
            sp.save()
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
     

def ServiceRec(request,order_slug):
    order = ServiceOrder.objects.get(slug=order_slug)
    form = ServicerecommendationForm(request.POST)
    sevrec = Servicerecommendation()
    if form.is_valid():
        sevrec.service_list = form.cleaned_data['service_list']
        sevrec.service_order = form.cleaned_data['service_order']
        sevrec.save()
        sweetify.toast(request, 'Service Recommended', timer=3000)
        return redirect('ServiceRec', order_slug=order_slug)
    else:
        form = ServicerecommendationForm()
    rec_details = Servicerecommendation.objects.filter(service_order =  order)
    context ={
        'form' : form,
        'od':order,
        'rec_details' : rec_details ,
    }
    return render ( request,'mechanic/service_rec.html',context)

def RsaserviceAdd(request,order_slug):
    order = ServiceOrder.objects.get( slug = order_slug )
    order_item = ServiceOrderItem()
    addForm = ServiceMechAddForm(request.POST)
    if addForm.is_valid():
        service_list = addForm.cleaned_data['service_list']
        order_item.service_order = order
        order_item.vehicle_info = order.vehicle
        order_item.service_list = service_list
        order_item.save()
        print (service_list)
        sweetify.toast(request, 'Service  Added', timer=3000)
        return redirect('service_details', service_slug=order_slug)
    else:
        addForm = ServiceMechAddForm()
    context = {
        'addForm' : addForm, 
    }
    return render ( request,'mechanic/Rsa_ServiceAdd.html',context)

def ServiceRecDel(request,rec_slug):
    del_item = Servicerecommendation.objects.get(recslug = rec_slug)
    order_slug = del_item.service_order.slug
    del_item.delete()
    sweetify.toast(request, 'Service Recommendation is Removed!', timer=3000)
    return redirect('service_details', service_slug=order_slug)


def Roadsideassist (request) :
    mech = request.user
    center_details = mechanicList.objects.get(mechanic =mech)
    rsa_detials =  RoadsideAssistance.objects.filter(service_center =  center_details.service_center)
    context ={
        'rsa_detials' : rsa_detials,
    }
    return render (request,'mechanic/roadsideassist.html',context)

def Roadsidedetails (request,slug) :
    rsa = RoadsideAssistance.objects.get( slug = slug )
    context = {
        'rsa' : rsa,
    }
    return render (request,'mechanic/rsadetials.html',context)

#for showing dynamically the service orders
def service_order_items_view(request, service_order_slug):
    service_order = get_object_or_404(ServiceOrder, slug=service_order_slug)
    order_items = ServiceOrderItem.objects.filter(service_order=service_order)
    return render(request, 'mechanic/service_order_items.html', {'order_items': order_items, 'service_order_slug': service_order.slug})



def get_orderitems(request, service_slug):
    order = ServiceOrder.objects.get(slug=service_slug)
    order_items = ServiceOrderItem.objects.filter(service_order=order)
    order_items_json = [
        {
            'service_Image': item.service_list.service_Image.url,
            'service_list_name': item.service_list.service_name,
            'status': item.status,
            'service_category': item.service_list.service_category.category_name,
            'slug': item.slug
        }
        for item in order_items
    ]
    return JsonResponse(order_items_json, safe=False)