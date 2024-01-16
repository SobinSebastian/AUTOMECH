from . forms import *
from . models import *
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views import main as default_admin_index


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


def vehicle_add (request):
    search_query = request.GET.get('q') 

    if search_query:
        models =CarModel.objects.filter(Model_Name__icontains=search_query).order_by('make_company', 'model_name')
    else:
        models = CarModel.objects.all().order_by('make_company', 'model_name')
    form = ModelForm()
    form1 = MakeForm()

    if request.method == 'POST':
        if 'form' in request.POST:
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'New Vehicle is added')
                return redirect('vehicle_add')
        elif 'form1' in request.POST:
            form1 = MakeForm(request.POST)
            if form1.is_valid():
                form1.save()
                messages.success(request, 'New Make is added')
                return redirect('vehicle_add')

    return render(request, 'admin/vehicle_add.html', {'form': form, 'form1': form1, 'models': models})