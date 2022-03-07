from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LoggedUser)
admin.site.register(purposeData)
admin.site.register(SponsorsData)
admin.site.register(ZipCode)
admin.site.register(County)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(needTofocusData)
# admin.site.register()