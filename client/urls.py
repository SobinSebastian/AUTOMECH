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
path('get_car_models/<int:make_id>/', views.get_car_models, name='get_car_models'),
path('get_car_variants/<int:model_id>/', views.get_car_variants, name='get_car_variants'),
path('map/', views.map_view, name='map_view'),
path('ajax/load-services/<slug:category_slug>/', views.ajax_load_services, name='ajax_load_services'),
]