from .import views
from django.urls import  path
urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.orders, name='orders'),
]