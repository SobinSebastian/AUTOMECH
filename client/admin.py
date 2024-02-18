from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(CarModel)
admin.site.register(Fueltype)
admin.site.register(ModelVariant)
admin.site.register(Vehicleinfo)
admin.site.register(transmissionType)
admin.site.register(ServiceCategory)
admin.site.register(ServiceCenter)
admin.site.register(CarMake)
admin.site.register(ServicePrice)