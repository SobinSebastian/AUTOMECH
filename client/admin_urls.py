from .import views 
from django.urls import  path
from .views import  * 
# (
#     CarModelListView,
#     FueltypeListView,
#     ModelVariantListView,
#     VehicleinfoListView,
# )
urlpatterns = [
path('home/',views.admin_dashboard,name="admin_home"),
#path('vehicle/',views.vehicle_add,name="vehicle_add"),
path('car_make/', views.CarMakes.as_view(), name='car_make'),
path('car_make/model',views.ModelsMake, name='car_make_model'),
path('car_model/', views.CarModels.as_view(), name='car_model'),
path('car_model/variant',views.Car_variant_view,name='car_variant'),
path('car_model/variant/service/<slug:slug>/',views.variant_serviceprice_view,name='car_variant_service'),
path('service/category/',views.service_category,name='service_category'),
path('service/category/<slug:slug>/',views.service_category,name='service_category'),
path('service/category/list/<slug:slug>/',views.service_category_list,name='service_category_list'),
path('service/category/list/view/<slug:slug>/',views.service_category_view,name='service_edit'),
path('fuel_type/create/', views.FueltypeCreateView.as_view(), name='fuel_type_create'),
path('model_variant/create/', views.ModelVariantCreateView.as_view(), name='model_variant_create'),
path('car_model/', views.CarModels.as_view(), name='car_model'),
path('fueltype/', FueltypeListView.as_view(), name='fueltype_list'),
path('model_variant/', ModelVariantListView.as_view(), name='model_variant_list'),
path('vehicleinfo/', VehicleinfoListView.as_view(), name='vehicleinfo_list'),
path('clients/list', views.client_list_view, name='client_list'),
path('service_center/add', views.service_center_add, name='service_center'),
path('service_center/', views.service_center_view, name='service_center_view'),
path('service_center/manager/', views.service_center_manager, name='service_center_manager'),
path('service_center/<slug:slug>/', views.service_center_details, name='service_center_details'),
path('model_variant/service',variant_service,name='variant_service'),
path('create_service_price/',create_service_form,name='create_service_price'),
path('post/<slug:slug>/', create_or_edit_post, name='edit_post'),#FOR BLOG EDIT
path('post/', create_or_edit_post, name='create_post'),#FOR BLOG CREATION
path('blog/',view_blog,name='admin_blog'),#blog
path('blog/<slug:blog_slug>/',blog_details,name='blog_details'),
path('tasks/', TaskListViewAndCreateView, name='task_list_create_update'),
path('tasks/<slug:slug>/', TaskListUpdateView, name='edit_task'),
#URLS FOR Bluk upload
path('download-excel-with-headers/',download_excel_with_headers, name='download_excel_with_headers'),
path('insert_data',insert_excel,name="excelin"),
path('car_make/<slug:make_slug>/edit/', CarMakeUpdateView.as_view(), name='car_make_edit'),
]