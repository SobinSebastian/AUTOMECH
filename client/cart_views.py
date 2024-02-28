from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import sweetify
@login_required
def view_cart(request):
    id = request.session.get('selected_vehicle')
    vehicle = Vehicleinfo.objects.get(id=id)
    service_prices = ServicePrice.objects.filter(variant = vehicle.model_variant)
    cart_items = Cart.objects.filter(vehicle_info=vehicle)
    cart_items_with_prices = []
    total_price  = 0
    for cart_item in cart_items:
        for service_p in service_prices:
            if service_p.service == cart_item.service_list:
                cart_items_with_prices.append({
                    'cart_item': cart_item,
                    'price': service_p.price
                })
                total_price = (total_price + service_p.price)
    service_centers = ServiceCenter.objects.all()

    #//////////////////////// SERVICE ORDER PLACING  //////////////////////////
    if request.method == 'POST':
        service_center_id = request.POST.get('service_center')
        date = request.POST.get('date')
        time = request.POST.get('time')
        service_center = ServiceCenter.objects.get(id=service_center_id)
        booking_date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        
        # Create a ServiceOrder object and save it
        service_order = ServiceOrder(
            service_center=service_center,
            date=booking_date,
            time=time,
            vehicle=vehicle,
        )
        service_order.save()

        for cart_item in cart_items:
            service_order_item = ServiceOrderItem(
                service_order=service_order,
                vehicle_info=cart_item.vehicle_info,
                service_list=cart_item.service_list,
            )
            service_order_item.save()

            # Remove the item from the cart
            cart_item.delete()
            sweetify.toast(request, 'Order Placed', icon='success', timer=3000)
        # Redirect to a success page or do other actions
        return redirect('orders')  

    #//////////////////////// SERVICE ORDER PLACING END  //////////////////////
    context = {
        'cart_items': cart_items_with_prices,
        'total_price':  total_price,
        'service_centers': service_centers
    }
    return render(request, 'client/cart.html',context)

 
def add_to_cart(request, slug):
    client = request.user
    service = ServiceList.objects.get(slug = slug)
    id = request.session.get('selected_vehicle')
    vehicle = Vehicleinfo.objects.get(id=id)
    cart_item, created = Cart.objects.get_or_create(client=request.user,vehicle_info=vehicle,service_list=service)
    if created:
        sweetify.toast(request, 'Item added to the cart', icon='success', timer=3000)
    else:
        sweetify.toast(request, 'Item already exists in the cart', icon='warning', timer=3000)


    return redirect('index')
 
def orders (request):
    id = request.session.get('selected_vehicle')
    vehicle = Vehicleinfo.objects.get(id=id)
    service_prices = ServicePrice.objects.filter(variant = vehicle.model_variant)
    serviceorders = ServiceOrder.objects.filter(vehicle_id=id).order_by('date')
    order_items =ServiceOrderItem.objects.all()

    order_items_with_prices = []
    total_price  = 0
    for order_item in order_items:
        matched = False
        for service_p in service_prices:
            if service_p.service == order_item.service_list and not matched:
                total_price = (total_price+service_p.price)
                order_items_with_prices.append({
                    'order_item': order_item,
                    'price': service_p.price
                })
                print(service_p.price)
                matched = True 
                payruppe = total_price *100
    context = {
        'serviceorders': serviceorders,
        'order_items' : order_items_with_prices,
        'total_price':  total_price,
        'payruppe':payruppe
        }
    return  render(request,'client/orders.html',context)


def remove_from_cart(request, slug):
    cart_item = Cart.objects.get(slug=slug)
    cart_item.delete()
    sweetify.toast(request, 'Item Removed From the cart', icon='error', timer=3000)
    return redirect('view_cart')


def book(request):
    return redirect('view_cart')




# code to generate pdf 
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generate_estimate_pdf(request):
    # Your estimate data (replace this with your actual data)
    estimate_data = {
        'customer_name': 'John Doe',
        'item': 'Web Development',
        'quantity': 5,
        'unit_price': 100,
        'total_amount': 500,
    }

    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    
    # Set the content-disposition header to force download
    response['Content-Disposition'] = 'attachment; filename="estimate.pdf"'

    # Create a PDF object
    pdf = canvas.Canvas(response)

    # Add content to the PDF
    pdf.drawString(100, 800, f'Estimate for: {estimate_data["customer_name"]}')
    pdf.drawString(100, 780, f'Item: {estimate_data["item"]}')
    pdf.drawString(100, 760, f'Quantity: {estimate_data["quantity"]}')
    pdf.drawString(100, 740, f'Unit Price: ${estimate_data["unit_price"]}')
    pdf.drawString(100, 720, f'Total Amount: ${estimate_data["total_amount"]}')

    # Save the PDF
    pdf.showPage()
    pdf.save()

    return response
