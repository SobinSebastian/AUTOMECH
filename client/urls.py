from .import views
from django.urls import  path
from django.contrib.auth import views as auth_views
from .views import CustomSignupView

urlpatterns = [
path('',views.index,name="index"),
path('account/profile/',views.profileview,name="account_profile"),
path('vehicle/',views.vehicle,name="vehicle"),
path('vehicle/add',views.add_vehicle,name="vehicle_add"),
path('vehicle/edit/<int:id>/', views.edit_vehicle, name='vehicle_edit'),
path('get_car_models/', views.get_car_models, name='get_car_models'),
]