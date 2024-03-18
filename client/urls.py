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
path('u_vehicle',views.uservehicle,name='uservehicle'),
path('map/', views.map_view, name='map_view'),
path('get_category_data/<slug:category_slug>/', views.get_category_data, name='get_category_data'),
path('service/cost',views.servicecost_estimation,name='service_cost_finder'),

# RSA URLS
path('rsa/request',views.rsa,name='rsarequest'),
path('rsa/details',views.rsadetails,name='rsadetails'),

path('blog/',views.client_blog,name='client_blog'),
path('blog/<slug:blog_slug>/',views.client_blog_details,name='client_blog_details'),

path('like_post/<slug:post_slug>/',views.like_post, name='like_post'),
path('Terms',views.terms,name='terms'),
path('Privacy',views.privacy,name='privacy'),

path('Vehicles',views.vehicel_details,name='my_vehicles'),
path('logout/', views.custom_logout, name='custom_logout'),
path('cars/',views.car,name='cars'),
path('Vehicles/History/<str:vehicle_Regno>',views.service_history,name='history'),
#for vehicle select
path('load_car_make/', views.load_car_make, name='load_car_make'),
path('load_car_models/<int:make_id>/', views.load_car_models, name='load_car_models'),
path('load_model_variants/<int:model_id>/', views.load_model_variants, name='load_model_variants'),
path('setcar/<slug:var_slug>', views.setcar, name='setcar'),
path('check_vehicle_exists/', views.check_vehicle_exists, name='check_vehicle_exists'),
path('warning-alarm/',views.warning_alarm, name='warning_alarm'),
path('check_email_exists/', views.check_email_exists, name='check_email_exists'),
]