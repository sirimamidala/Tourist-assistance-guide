from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from math import radians, cos, sin, asin, sqrt
from .models import Place, HillStation
from .forms import PlaceForm, HillStationForm, GeoLocationSearchForm
from tourist_project.services.gemini_service import GeminiService
from tourist_project.services.places_service import PlacesService
from django.http import JsonResponse


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers
    return c * r


def geolocation_search(request):
    """Search for places using geolocation and filters, with map display."""
    form = GeoLocationSearchForm(request.GET or None)
    places = []
    total_places = 0
    search_performed = False
    search_lat = None
    search_lng = None
    
    # Indian city coordinates for geocoding typed location names
    CITY_GPS = {
        'warangal': (17.9784, 79.5941), 'hyderabad': (17.3850, 78.4867),
        'bangalore': (12.9716, 77.5946), 'bengaluru': (12.9716, 77.5946),
        'chennai': (13.0827, 80.2707), 'mumbai': (19.0760, 72.8777),
        'delhi': (28.6139, 77.2090), 'new delhi': (28.6139, 77.2090),
        'kolkata': (22.5726, 88.3639), 'pune': (18.5204, 73.8567),
        'jaipur': (26.9124, 75.7873), 'goa': (15.2993, 74.1240),
        'kochi': (9.9312, 76.2673), 'cochin': (9.9312, 76.2673),
        'thiruvananthapuram': (8.5241, 76.9366), 'trivandrum': (8.5241, 76.9366),
        'mysore': (12.3051, 76.6551), 'mysuru': (12.3051, 76.6551),
        'vizag': (17.6868, 83.2185), 'visakhapatnam': (17.6868, 83.2185),
        'vijayawada': (16.5062, 80.6480), 'tirupati': (13.6288, 79.4192),
        'madurai': (9.9252, 78.1198), 'coimbatore': (11.0168, 76.9558),
        'trichy': (10.7905, 78.7047), 'thanjavur': (10.7870, 79.1378),
        'pondicherry': (11.9416, 79.8083), 'puducherry': (11.9416, 79.8083),
        'shimla': (31.1048, 77.1734), 'manali': (32.2396, 77.1887),
        'ooty': (11.4102, 76.6950), 'munnar': (10.0889, 77.0595),
        'darjeeling': (27.0410, 88.2663), 'gangtok': (27.3389, 88.6065),
        'udaipur': (24.5854, 73.7125), 'jodhpur': (26.2389, 73.0243),
        'varanasi': (25.3176, 83.0036), 'agra': (27.1767, 78.0081),
        'amritsar': (31.6200, 74.8765), 'rishikesh': (30.0869, 78.2676),
        'dehradun': (30.3165, 78.0322), 'mussoorie': (30.4598, 78.0644),
        'nainital': (29.3919, 79.4542), 'kodaikanal': (10.2381, 77.4892),
        'leh': (34.1526, 77.5771), 'srinagar': (34.0837, 74.7973),
        'chandigarh': (30.7333, 76.7794), 'lucknow': (26.8467, 80.9462),
        'ahmedabad': (23.0225, 72.5714), 'bhopal': (23.2599, 77.4126),
        'indore': (22.7196, 75.8577), 'nagpur': (21.1458, 79.0882),
        'patna': (25.6093, 85.1376), 'bhubaneswar': (20.2961, 85.8245),
        'guwahati': (26.1445, 91.7362), 'coorg': (12.3375, 75.8069),
        'hampi': (15.3350, 76.4600), 'puri': (19.8135, 85.8312),
        'mahabalipuram': (12.6172, 80.1927), 'rameshwaram': (9.2876, 79.3129),
        'alleppey': (9.4981, 76.3388), 'kovalam': (8.3988, 76.9780),
        'varkala': (8.7379, 76.7163), 'lonavala': (18.7546, 73.4062),
        'mount abu': (24.5926, 72.7156), 'wayanad': (11.6854, 76.1320),
        'araku': (18.3273, 82.8759), 'srisailam': (15.8512, 78.8680),
        'guntur': (16.3067, 80.4365), 'nellore': (14.4426, 79.9865),
        'khammam': (17.2473, 80.1514), 'nizamabad': (18.6725, 78.0940),
        'karimnagar': (18.4386, 79.1288), 'salem': (11.6643, 78.1460),
    }
    
    if request.GET and form.is_valid():
        search_performed = True
        latitude = form.cleaned_data.get('latitude')
        longitude = form.cleaned_data.get('longitude')
        location_name = form.cleaned_data.get('location_name', '') or ''
        location_name = location_name.strip()
        place_type = form.cleaned_data.get('place_type')
        search_radius = int(form.cleaned_data.get('search_radius', 50))
        
        # Geocode: if no GPS coords but location name typed, look up the city
        if (latitude is None or longitude is None) and location_name:
            city_key = location_name.lower().strip()
            if city_key in CITY_GPS:
                latitude, longitude = CITY_GPS[city_key]
        
        if latitude is not None and longitude is not None:
            search_lat = latitude
            search_lng = longitude
            
            # Search Places by distance
            all_places = Place.objects.filter(latitude__isnull=False, longitude__isnull=False)
            for place in all_places:
                dist = haversine(longitude, latitude, place.longitude, place.latitude)
                if dist <= search_radius:
                    place.distance_km = round(dist, 2)
                    place.result_type = 'place'
                    places.append(place)
            
            # Also search HillStations by distance
            all_hills = HillStation.objects.filter(latitude__isnull=False, longitude__isnull=False)
            for hs in all_hills:
                dist = haversine(longitude, latitude, hs.longitude, hs.latitude)
                if dist <= search_radius:
                    hs.distance_km = round(dist, 2)
                    hs.result_type = 'hill_station'
                    hs.category = 'HILL_STATION'
                    places.append(hs)
        
        elif location_name:
            # Fall back to text search across both models
            text_places = list(Place.objects.filter(
                Q(location__icontains=location_name) | Q(name__icontains=location_name)
            ))
            for p in text_places:
                p.result_type = 'place'
            places.extend(text_places)
            
            text_hills = list(HillStation.objects.filter(
                Q(city__icontains=location_name) | Q(name__icontains=location_name) |
                Q(state__icontains=location_name)
            ))
            for hs in text_hills:
                hs.result_type = 'hill_station'
                hs.category = 'HILL_STATION'
            places.extend(text_hills)
        else:
            # Show all places if empty search
            for p in Place.objects.all():
                p.result_type = 'place'
                places.append(p)
            for hs in HillStation.objects.all():
                hs.result_type = 'hill_station'
                hs.category = 'HILL_STATION'
                places.append(hs)
        
        # Filter by place type
        if place_type:
            if place_type == 'HILL_STATION':
                places = [p for p in places if getattr(p, 'category', '') == 'HILL_STATION']
            elif place_type == 'TEMPLE':
                places = [p for p in places if 
                    'historical' in getattr(p, 'category', '').lower() or 
                    'temple' in getattr(p, 'name', '').lower() or
                    'temple' in getattr(p, 'location', getattr(p, 'city', '')).lower()]
            elif place_type in ['BEACH', 'HISTORICAL', 'NATURE', 'ADVENTURE', 'CITY']:
                places = [p for p in places if getattr(p, 'category', '') == place_type]
        
        total_places = len(places)
        places = sorted(places, key=lambda x: getattr(x, 'distance_km', float('inf')))
    
    return render(request, 'explorer/geolocation_search.html', {
        'form': form,
        'places': places,
        'total_places': total_places,
        'search_performed': search_performed,
        'search_lat': search_lat,
        'search_lng': search_lng,
    })


def get_nearby_places(lat, lon, exclude_pk=None, exclude_type=None):
    """Helper to find nearby records from both models."""
    nearby = []
    if lat is None or lon is None:
        return []
        
    # Check Places
    all_p = Place.objects.filter(latitude__isnull=False, longitude__isnull=False)
    for p in all_p:
        if exclude_type == 'place' and p.pk == exclude_pk:
            continue
        dist = haversine(lon, lat, p.longitude, p.latitude)
        if dist <= 25:
            p.distance_km = round(dist, 2)
            p.result_type = 'place'
            nearby.append(p)
            
    # Check HillStations
    all_h = HillStation.objects.filter(latitude__isnull=False, longitude__isnull=False)
    for h in all_h:
        if exclude_type == 'hill_station' and h.pk == exclude_pk:
            continue
        dist = haversine(lon, lat, h.longitude, h.latitude)
        if dist <= 25:
            h.distance_km = round(dist, 2)
            h.result_type = 'hill_station'
            h.category = 'HILL_STATION'
            nearby.append(h)
            
    nearby.sort(key=lambda x: x.distance_km)
    return nearby[:6]


def explorer_list(request):
    """Public: view all tourist places with optional search and category filter."""
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')
    
    places = Place.objects.all()
    ai_suggestions = []

    if query:
        # Search local database
        places = places.filter(
            Q(name__icontains=query) | 
            Q(location__icontains=query) | 
            Q(description__icontains=query)
        )
        
        # Call Gemini for global suggestions if query is more than just a short string
        if len(query) > 2:
            ai_suggestions = GeminiService.find_global_places(query)

    if category:
        places = places.filter(category=category)

    categories = Place.CATEGORY_CHOICES
    return render(request, 'explorer/list.html', {
        'places': places,
        'categories': categories,
        'selected_category': category,
        'search_query': query,
        'ai_suggestions': ai_suggestions,
    })


def explorer_detail(request, pk):
    """Public: detailed view of a single place with map and nearby places."""
    place = get_object_or_404(Place, pk=pk)
    nearby_places = get_nearby_places(place.latitude, place.longitude, exclude_pk=place.pk, exclude_type='place')
    
    return render(request, 'explorer/detail.html', {
        'place': place,
        'nearby_places': nearby_places,
    })


@staff_member_required
def place_add(request):
    """Admin only: add a new tourist place."""
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save()
            messages.success(request, f'"{place.name}" has been added successfully!')
            return redirect('explorer-list')
    else:
        form = PlaceForm()
    return render(request, 'explorer/form.html', {'form': form, 'action': 'Add'})


@staff_member_required
def place_edit(request, pk):
    """Admin only: edit an existing tourist place."""
    place = get_object_or_404(Place, pk=pk)
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{place.name}" updated successfully!')
            return redirect('explorer-detail', pk=place.pk)
    else:
        form = PlaceForm(instance=place)
    return render(request, 'explorer/form.html', {'form': form, 'action': 'Edit', 'place': place})


@staff_member_required
def place_delete(request, pk):
    """Admin only: delete a tourist place."""
    place = get_object_or_404(Place, pk=pk)
    if request.method == 'POST':
        name = place.name
        place.delete()
        messages.success(request, f'"{name}" deleted successfully.')
        return redirect('explorer-list')
    return render(request, 'explorer/confirm_delete.html', {'place': place})


# Hill Station Views
def hill_stations_list(request):
    """Public: view all hill stations with search and filter by state and city."""
    state = request.GET.get('state', '')
    city = request.GET.get('city', '')
    
    hill_stations = HillStation.objects.all()
    
    if state:
        hill_stations = hill_stations.filter(state__icontains=state)
    
    if city:
        hill_stations = hill_stations.filter(city__icontains=city)
    
    # Get unique states and cities for filter dropdowns
    states = HillStation.objects.values_list('state', flat=True).distinct().order_by('state')
    cities = HillStation.objects.values_list('city', flat=True).distinct().order_by('city')
    
    return render(request, 'explorer/hill_stations_list.html', {
        'hill_stations': hill_stations,
        'states': states,
        'cities': cities,
        'selected_state': state,
        'selected_city': city,
    })


def hill_station_detail(request, pk):
    """Public: detailed view of a single hill station with map and nearby places."""
    hill_station = get_object_or_404(HillStation, pk=pk)
    nearby_places = get_nearby_places(hill_station.latitude, hill_station.longitude, exclude_pk=hill_station.pk, exclude_type='hill_station')
    
    return render(request, 'explorer/hill_station_detail.html', {
        'hill_station': hill_station,
        'nearby_places': nearby_places,
    })


@staff_member_required
def hill_station_add(request):
    """Admin only: add a new hill station."""
    if request.method == 'POST':
        form = HillStationForm(request.POST, request.FILES)
        if form.is_valid():
            hill_station = form.save()
            messages.success(request, f'"{hill_station.name}" has been added successfully!')
            return redirect('hill-stations-list')
    else:
        form = HillStationForm()
    return render(request, 'explorer/hill_station_form.html', {'form': form, 'action': 'Add'})


@staff_member_required
def hill_station_edit(request, pk):
    """Admin only: edit an existing hill station."""
    hill_station = get_object_or_404(HillStation, pk=pk)
    if request.method == 'POST':
        form = HillStationForm(request.POST, request.FILES, instance=hill_station)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{hill_station.name}" updated successfully!')
            return redirect('hill-station-detail', pk=hill_station.pk)
    else:
        form = HillStationForm(instance=hill_station)
    return render(request, 'explorer/hill_station_form.html', {'form': form, 'action': 'Edit', 'hill_station': hill_station})


@staff_member_required
def hill_station_delete(request, pk):
    """Admin only: delete a hill station."""
    hill_station = get_object_or_404(HillStation, pk=pk)
    if request.method == 'POST':
        name = hill_station.name
        hill_station.delete()
        messages.success(request, f'"{name}" deleted successfully.')
        return redirect('hill-stations-list')
    return render(request, 'explorer/hill_station_confirm_delete.html', {'hill_station': hill_station})


def api_nearby_places(request):
    """
    AJAX endpoint to receive GPS coordinates and return nearby places from external APIs.
    """
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius', 2)
    category = request.GET.get('category', 'ATTRACTION')

    if not lat or not lng:
        return JsonResponse({"error": "Latitude and Longitude are required"}, status=400)

    try:
        radius_float = float(radius)
        print(f"--- GPS Search Debug ---")
        print(f"Lat: {lat}, Lng: {lng}, Radius: {radius_float}km, Category: {category}")
        
        data = PlacesService.get_nearby_places(lat, lng, radius_float, category)
        print(f"Results Count: {len(data) if isinstance(data, list) else 'Error'}")
        print(f"-------------------------")
        
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=500)
            
        return JsonResponse({"results": data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def real_time_explorer(request):
    """
    Render the real-time GPS explorer page.
    """
    return render(request, 'explorer/real_time.html')
