from .import views 
from django.urls import  path
from .views import  * 
urlpatterns = [
    path('home/',views.mechanic_dashboard,name="mechanic_home"),
    # path('service/booking/',views.mechanic_bookings,name="mechanic_booking"),
    # path('rsa/',views.manager_rsa,name="rsa_request_view"),
]