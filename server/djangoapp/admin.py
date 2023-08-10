from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarMakeInline(admin.TabularInline):  
    model = CarModel.carmakes.through


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    inlines = [CarMakeInline]
# CarMakeAdmin class with CarModelInline


# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel,CarModelAdmin)