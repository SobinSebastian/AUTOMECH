from .import views 
from django.urls import  path
from .views import (
    CarModelListView,
    FueltypeListView,
    ModelVariantListView,
    VehicleinfoListView,
)
urlpatterns = [
path('home/',views.admin_dashboard,name="admin_home"),
#path('vehicle/',views.vehicle_add,name="vehicle_add"),
path('car_make/', views.CarMake.as_view(), name='car_make'),
path('car_model/create/', views.CarModelCreateView.as_view(), name='car_model_create'),
path('fuel_type/create/', views.FueltypeCreateView.as_view(), name='fuel_type_create'),
path('model_variant/create/', views.ModelVariantCreateView.as_view(), name='model_variant_create'),
path('car_model/', CarModelListView.as_view(), name='car_model_list'),
path('fueltype/', FueltypeListView.as_view(), name='fueltype_list'),
path('model_variant/', ModelVariantListView.as_view(), name='model_variant_list'),
path('vehicleinfo/', VehicleinfoListView.as_view(), name='vehicleinfo_list'),
]