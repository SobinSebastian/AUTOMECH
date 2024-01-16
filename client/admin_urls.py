from .import views
from django.urls import  path
urlpatterns = [
path('home/',views.admin_dashboard,name="admin_home"),
path('vehicle/',views.vehicle_add,name="vehicle_add"),
]