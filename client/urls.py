from .import views
from django.urls import  path
from django.contrib.auth import views as auth_views
from .views import CustomSignupView

urlpatterns = [
path('',views.index,name="index"),
path('account/profile/',views.profileview,name="account_profile"),
]