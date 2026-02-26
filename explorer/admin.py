from django.contrib import admin
from .models import Place, HillStation


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'category', 'date_added')
    list_filter = ('category',)
    search_fields = ('name', 'location')
    readonly_fields = ('date_added',)


@admin.register(HillStation)
class HillStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'created_date')
    list_filter = ('state', 'country')
    search_fields = ('name', 'city', 'district', 'state')
    readonly_fields = ('created_date', 'latitude', 'longitude')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Location Details', {
            'fields': ('city', 'district', 'state', 'country')
        }),
        ('Map Coordinates', {
            'fields': ('latitude', 'longitude')
        }),
        ('Visit Information', {
            'fields': ('best_time_to_visit', 'temperature_range')
        }),
        ('Metadata', {
            'fields': ('created_date',)
        }),
    )
