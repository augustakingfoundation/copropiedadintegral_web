from django.contrib import admin

from place.models import City
from place.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'state',
    )

    list_filter = (
        'state',
    )
