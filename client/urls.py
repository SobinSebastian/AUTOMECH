from .import views
from django.urls import  path
from django.contrib.auth import views as auth_views
from .views import CustomSignupView

urlpatterns = [
path('',views.index,name="index"),
path('account/profile/',views.profileview,name="account_profile"),
path('account/profilesetup/',views.profilesetup,name="profile_setup"),
path('step1/',views.step1_view, name='step1_view'),
path('step2/', views.step2_view, name='step2_view'),
path('vehicle/',views.vehicle,name="vehicle"),
path('vehicle/add',views.add_vehicle,name="vehicle_add"),
path('vehicle/edit/<int:id>/', views.edit_vehicle, name='vehicle_edit'),
path('get_car_models/<int:make_id>/', views.get_car_models, name='get_car_models'),
path('get_model_variants/', views.get_model_variants, name='get_model_variants'),
path('get_models/', views.get_models, name='get_models'),
path('map/', views.map_view, name='map_view'),
path('get_category_data/<slug:category_slug>/', views.get_category_data, name='get_category_data'),
path('service/cost',views.servicecost_estimation,name='service_cost_finder'),

]