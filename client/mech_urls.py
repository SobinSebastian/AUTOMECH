from .import views 
from django.urls import  path
from .views import  * 
urlpatterns = [
    path('home/',views.mechanic_dashboard,name="mechanic_home"),
    path('Slot/',views.mechanic_slot,name="mechanic_slot"),
    path('service/orders/',views.service_orders,name="service_orders"),
    path('service/details/<slug:service_slug>',views.service_details,name="service_details"),
    path('service/start/<slug:order_slug>',views.start_order,name="order_start"),
    path('service-order-json/', ServiceOrderJsonView.as_view(), name='service-order-json'),
    path('service-slot-json/', ServiceSlotJsonView.as_view(), name='service-slot-json'),
    path('serviceRec/<slug:order_slug>',views.ServiceRec,name='ServiceRec'),
    # path('rsa/',views.manager_rsa,name="rsa_request_view"),
]