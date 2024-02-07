from .import views 
from django.urls import  path
from .views import  * 
urlpatterns = [
    path('home/',views.manager_dashboard,name="manager_home"),
    path('service_slots/',views.manager_slots,name="service_slots"),
    path('mechanic/',views.manager_mechanic,name="manager_mechanic"),
    path('service/booking/',views.manager_bookings,name="manager_booking"),
    path('rsa/',views.manager_rsa,name="rsa_request"),
]