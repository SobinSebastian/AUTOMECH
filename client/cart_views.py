from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import sweetify
from django.views.decorators.cache import cache_control
import razorpay
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
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
            price = total_price,
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
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def orders (request):
    id = request.session.get('selected_vehicle')
    vehicle = Vehicleinfo.objects.get(id=id)
    service_prices = ServicePrice.objects.filter(variant = vehicle.model_variant)
    serviceorders = ServiceOrder.objects.filter(vehicle_id=id).order_by('date')
    order_items =ServiceOrderItem.objects.all()

    serviceorder_prices = []

    for serviceorder in serviceorders:
        total_price = 0

        for order_item in order_items:
            if order_item.service_order == serviceorder:
                for service_p in service_prices:
                    if service_p.service == order_item.service_list:
                        total_price += service_p.price
                        # order_item_with_price = {
                        #     'order_item': order_item,
                        #     'price': service_p.price
                        # }
                        # serviceorder_prices.append(order_item_with_price)

        # Append the total price along with the service order
                payruppe = total_price *100
        serviceorder_prices.append({
            'service_order': serviceorder,
            'total_price': total_price,
            'payruppe':payruppe        
            })

    order_items_with_prices = []
    for order_item in order_items: 
        total_price  = 0
        for service_p in service_prices:
            if service_p.service == order_item.service_list:
                total_price = (total_price+service_p.price)
                order_items_with_prices.append({
                    'order_item': order_item,
                    'price': service_p.price
                })
    context = {
        'serviceorder_prices':serviceorder_prices,
        'serviceorders': serviceorders,
        'order_items' : order_items_with_prices,
        }
    return  render(request,'client/orders.html',context)


def remove_from_cart(request, slug):
    cart_item = Cart.objects.get(slug=slug)
    cart_item.delete()
    sweetify.toast(request, 'Item Removed From the cart', icon='error', timer=3000)
    return redirect('view_cart')


def book(request):
    return redirect('view_cart')

#basic setup for payment it will handle with pay id in database
def pay(request,slug):
    det = ServiceOrder.objects.get(slug=slug)
    price = det.price
    amount_in_paise = int(price * 100)
    client = razorpay.Client(auth=('rzp_test_fUAj9vRg2OywN4', '1edKB7jxm6c56kSl4tzg0z0E'))
    payment = client.order.create(data={ 'amount':amount_in_paise, 'currency': 'INR', 'payment_capture': 1 })
    det.razorpay_order_id=payment['id']
    det.save() 
    context ={
        'det':det,
        'payment': payment
    }
    return render(request,'client/pay_bill.html',context)

# code to generate pdf 
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generate_estimate_pdf(request,slug):

    orders = ServiceOrder.objects.get(slug =slug)
    car = orders.vehicle.model_variant
    service_prices = ServicePrice.objects.filter(variant = car)
    items = ServiceOrderItem.objects.filter(service_order = orders)
    table_data = [
    ["Service Name", "Price"]
    ]
    totalprice= 0
    for i in items:
        for j in service_prices:
            if j.service == i.service_list:
                totalprice =  totalprice + j.price
                table_data.append([i.service_list.service_name,str(j.price) ])
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    
    # Set the content-disposition header to force download
    response['Content-Disposition'] = 'attachment; filename="estimate.pdf"'

    # Create a PDF object
    pdf = canvas.Canvas(response)
    logo_path = "D:\PROJECT 2024\Automech\client\logo.png"  # Modify this path to your logo image
    logo_width = 50  # Adjust logo width as needed
    logo_height = 50  # Adjust logo height as needed
    if logo_path:
      pdf.drawImage(logo_path, 50, 770, width=logo_width, height=logo_height)

  # Add company name
    pdf.setFont("Helvetica-Bold", 20)
    company_name = "Auto Mech"
    pdf.drawString(logo_width + 60, 790, company_name)  # Adjust position based on logo size

    # Enter your company and customer information

    customer_name = "Customer Name"
    customer_phone = "Customer Phone"
    customer_date = "MM/DD/YYYY"
    customer_address = "Customer Address"
    car_make = f"{orders.vehicle.model_variant.model.make_company}"
    car_model = f"{orders.vehicle.model_variant}"
    car_registration = f"{orders.vehicle.vehicle_Regno}"
    car_serial = "Car Serial"
    car_odometer = "Odometer"
    insurance_company = "Insurance Company"
    adjuster = "Adjuster"

    pdf.setFont("Helvetica", 10)
    pdf.drawString(400, 800, f"Auto Mech,Pala Road")
    pdf.drawString(400, 785, f"Pallickathode,Kottayam ,686503")
    pdf.drawString(400, 770, f"auto.mech.rsa@gmail.com")
    pdf.drawString(400, 755, f"907457 4393")

    start_x = 50
    start_y = 750
    end_x = 500
    end_y = 750

    # Set line width and color (optional)
    line_width = 1  # Adjust thickness
    line_color = "black"  # Adjust color

    # Draw the line
    pdf.setStrokeColor(line_color)  # Set color before drawing (optional)
    pdf.setLineWidth(line_width)  # Set width before drawing (optional)
    pdf.line(start_x, start_y, end_x, end_y)

    pdf.drawString(60, 720, "Estimate For :")
    pdf.drawString(60, 705, "Name:")
    pdf.drawString(100, 705, f"{request.user}")
    pdf.drawString(60, 690, "Phone:")
    pdf.drawString(100, 690, f"9074574393")
    pdf.drawString(60, 675, "Email:")
    pdf.drawString(100, 675, f"sobinolickal1936@gmail.com")
    pdf.drawString(60, 660, "Address:")
    pdf.drawString(100, 660, f"{totalprice}")

    pdf.drawString(350, 720, "Date:")
    pdf.drawString(400, 720, customer_date)

    pdf.drawString(350, 705, "Vehicle Information:")
    car_details_left = 350  # Adjust for spacing
    car_details_top = 690
    pdf.drawString(car_details_left, car_details_top, f"Make: {car_make}")
    pdf.drawString(car_details_left, car_details_top - 15, f"Model: {car_model}")
    pdf.drawString(car_details_left, car_details_top - 30, f"Registration: {car_registration}")

    # Create a table for the estimate items
    # # Helper function to draw the table
    def draw_table(table_data, x, y, col_widths, row_heights):
        for col_index, col_width in enumerate(col_widths):
            for row_index, row_data in enumerate(table_data):
                cell_text = row_data[col_index]
                pdf.drawString(x + (col_index * col_width), y - (row_index * row_heights), cell_text)

    # # Draw the estimate table
    col_widths = [100, 150]
    row_heights = 15
    table_top = 600
    table_left = 50
    draw_table(table_data, table_left, table_top, col_widths, row_heights)

    pdf.showPage()
    pdf.save()

    return response
