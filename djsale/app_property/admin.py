from django.contrib import admin

from .models import HousingType, RoomsNumber, Housing


@admin.register(HousingType)
class AdminHousingType(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(RoomsNumber)
class AdminRoomsNumber(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Housing)
class AdminHousing(admin.ModelAdmin):
    list_display = ['id', 'cost', 'address', 'housing_type', 'rooms_number', 'created_date', 'is_sold', 'description']
