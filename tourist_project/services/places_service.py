import requests
import json
from django.conf import settings

class PlacesService:
    """
    Service helper to fetch real-time places data using external APIs.
    Supports OpenStreetMap (Overpass API) and Google Places API.
    """
    
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Mapping of our categories to OSM tags
    OSM_MAPPING = {
        'HOTEL': '["tourism"~"hotel|hostel|guest_house|motel|resort|apartment"]',
        'TRANSPORT': '["amenity"~"bus_station|bus_stop|taxi|ferry_terminal|train_station"]',
        'ATTRACTION': '["tourism"~"attraction|museum|viewpoint|zoo|theme_park|artwork"]',
        'RESTAURANT': '["amenity"~"restaurant|cafe|fast_food|food_court"]',
        'HOSPITAL': '["amenity"~"hospital|clinic|doctors"]',
        'TEMPLE': '["amenity"~"place_of_worship|shrine"]'
    }

    # Mapping of our categories to Google Place Types
    GOOGLE_MAPPING = {
        'HOTEL': 'lodging',
        'TRANSPORT': 'bus_station',
        'ATTRACTION': 'tourist_attraction',
        'RESTAURANT': 'restaurant',
        'HOSPITAL': 'hospital',
        'TEMPLE': 'place_of_worship'
    }

    @staticmethod
    def get_nearby_places(lat, lng, radius_km=2, category='ATTRACTION'):
        """
        Main method to fetch nearby places.
        Tries Google Places if API key is present, otherwise falls back to OSM.
        """
        google_api_key = getattr(settings, "GOOGLE_PLACES_API_KEY", None)
        
        # Fallback to general settings or placeholder if not specifically set
        if not google_api_key or google_api_key == 'your-google-api-key-here':
            return PlacesService._fetch_from_osm(lat, lng, radius_km, category)
        
        return PlacesService._fetch_from_google(lat, lng, radius_km, category, google_api_key)

    @staticmethod
    def _fetch_from_osm(lat, lng, radius_km, category):
        """Fetch data from OpenStreetMap Overpass API."""
        # Ensure radius is an integer and cap it at 50km for safety
        radius_meters = int(min(float(radius_km), 50) * 1000)
        tag = PlacesService.OSM_MAPPING.get(category, '["tourism"~"attraction"]')
        
        # Adding [timeout:60] to the query itself and increasing requests timeout
        query = f"""
        [out:json][timeout:60];
        (
          node(around:{radius_meters},{lat},{lng}){tag};
          way(around:{radius_meters},{lat},{lng}){tag};
          relation(around:{radius_meters},{lat},{lng}){tag};
        );
        out center body;
        """
        
        try:
            response = requests.post(PlacesService.OVERPASS_URL, data={'data': query}, timeout=65)
            data = response.json()
            
            results = []
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                # Use 'center' if available (for ways/relations), otherwise lat/lon
                lat_val = element.get('lat') or element.get('center', {}).get('lat')
                lng_val = element.get('lon') or element.get('center', {}).get('lon')
                
                if lat_val and lng_val:
                    results.append({
                        'name': tags.get('name', 'Unnamed Place'),
                        'lat': lat_val,
                        'lng': lng_val,
                        'category': category,
                        'address': tags.get('addr:full', tags.get('addr:street', 'Nearby Area')),
                        'rating': None,
                        'source': 'OpenStreetMap'
                    })
            return results
        except Exception as e:
            return {"error": f"OSM API Error: {str(e)}"}

    @staticmethod
    def _fetch_from_google(lat, lng, radius_km, category, api_key):
        """Fetch data from Google Places API."""
        radius_meters = radius_km * 1000
        place_type = PlacesService.GOOGLE_MAPPING.get(category, 'tourist_attraction')
        
        params = {
            'location': f"{lat},{lng}",
            'radius': radius_meters,
            'type': place_type,
            'key': api_key
        }
        
        try:
            response = requests.get(PlacesService.GOOGLE_PLACES_URL, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') != 'OK' and data.get('status') != 'ZERO_RESULTS':
                return {"error": f"Google API Error: {data.get('status')} - {data.get('error_message', '')}"}
                
            results = []
            for item in data.get('results', []):
                results.append({
                    'name': item.get('name'),
                    'lat': item['geometry']['location']['lat'],
                    'lng': item['geometry']['location']['lng'],
                    'category': category,
                    'address': item.get('vicinity', 'Nearby Area'),
                    'rating': item.get('rating'),
                    'source': 'Google Places'
                })
            return results
        except Exception as e:
            return {"error": f"Google API Error: {str(e)}"}
