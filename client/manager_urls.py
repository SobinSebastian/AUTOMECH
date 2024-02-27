from .import views 
from django.urls import  path
from .views import  * 
urlpatterns = [
    path('home/',views.manager_dashboard,name="manager_home"),
    path('service_slots/',views.manager_slots,name="service_slots"),
    path('mechanic/',views.manager_mechanic,name="manager_mechanic"),
    path('service/booking/',views.manager_bookings,name="manager_booking"),
    path('rsa/',views.manager_rsa,name="rsa_request"),
    path('check_unique_slotname/', check_unique_slotname, name='check_unique_slotname'),
    path('remove_alloc_mech/<slug:solt_slug>', remove_alloc_mech, name='remove_alloc_mech'),
     path('manager/bookings/json/', manager_bookings_json, name='manager_bookings_json'),
]