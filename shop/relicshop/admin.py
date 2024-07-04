from django.contrib import admin

from . import models


@admin.register(models.CityModel)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(models.StreetModel)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(models.ShopModel)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']