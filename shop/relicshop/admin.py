from django.contrib import admin

from . import models


@admin.register(models.CityModel)
class PostFilesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
