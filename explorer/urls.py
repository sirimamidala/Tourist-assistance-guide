from django.urls import path
from . import views

urlpatterns = [
    path('', views.explorer_list, name='explorer-list'),
    path('search/geolocation/', views.geolocation_search, name='geolocation-search'),
    path('<int:pk>/', views.explorer_detail, name='explorer-detail'),
    path('add/', views.place_add, name='explorer-add'),
    path('<int:pk>/edit/', views.place_edit, name='explorer-edit'),
    path('<int:pk>/delete/', views.place_delete, name='explorer-delete'),
    
    # Hill Stations URLs
    path('hill-stations/', views.hill_stations_list, name='hill-stations-list'),
    path('hill-stations/<int:pk>/', views.hill_station_detail, name='hill-station-detail'),
    path('hill-stations/add/', views.hill_station_add, name='hill-station-add'),
    path('hill-stations/<int:pk>/edit/', views.hill_station_edit, name='hill-station-edit'),
    path('hill-stations/<int:pk>/delete/', views.hill_station_delete, name='hill-station-delete'),

    # Real-time GPS Search
    path('real-time/', views.real_time_explorer, name='real-time-explorer'),
    path('api/nearby-places/', views.api_nearby_places, name='api-nearby-places'),
]
