from .import views
from django.urls import  path
from django.contrib.auth import views as auth_views
urlpatterns = [
path('',views.index,name="index"),
path('login',views.login,name="login"),
path ('signup',views.register,name="signup"),
]