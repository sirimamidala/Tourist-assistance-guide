from django.contrib import admin
from .models import Destination, Attraction, Gallery

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'category', 'rating')
    list_filter = ('category', 'destination')
    search_fields = ('name', 'destination__name')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('destination', 'caption')
    list_filter = ('destination',)
