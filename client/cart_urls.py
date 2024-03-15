from .import views
from django.urls import  path
urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.orders, name='orders'),
    path('orders/cancel/<slug:slug>', views.Cancel_Service_order, name='ocancel'),
    path('generate-estimate-pdf/<slug:slug>', views.generate_estimate_pdf, name='generate_estimate_pdf'),
    path('pay/<slug:slug>',views.pay,name='bill_pay'),
    path('razorpay_callback/',views.razorpay_callback,name='razorpay_callback'),
    path('generate-bill-pdf/<slug:slug>', views.generate_bill_pdf, name='generate_bill_pdf'),
]