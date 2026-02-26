"""
Seed GPS coordinates for all existing Place records in the explorer app.
Run with: python manage.py shell < seed_gps_coordinates.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist_project.settings')
django.setup()

from explorer.models import Place, HillStation
from destinations.models import Destination

# GPS coordinates for known Indian tourist places
# Format: { 'name_fragment': (latitude, longitude) }
GPS_DATA = {
    # Beaches
    'agonda': (15.0449, 73.9878),
    'palolem': (15.0100, 74.0230),
    'radhanagar': (11.9810, 92.9530),
    'varkala': (8.7379, 76.7163),
    'marina': (13.0499, 80.2824),
    'kovalam': (8.3988, 76.9780),
    'calangute': (15.5437, 73.7553),
    'baga': (15.5554, 73.7514),
    'anjuna': (15.5735, 73.7393),
    'juhu': (19.0988, 72.8267),
    
    # Hill Stations
    'ooty': (11.4102, 76.6950),
    'munnar': (10.0889, 77.0595),
    'kodaikanal': (10.2381, 77.4892),
    'manali': (32.2396, 77.1887),
    'shimla': (31.1048, 77.1734),
    'darjeeling': (27.0410, 88.2663),
    'mussoorie': (30.4598, 78.0644),
    'nainital': (29.3919, 79.4542),
    'coorg': (12.3375, 75.8069),
    'lonavala': (18.7546, 73.4062),
    'mount abu': (24.5926, 72.7156),
    'wayanad': (11.6854, 76.1320),
    'yelagiri': (12.5816, 78.6327),
    'yercaud': (11.7750, 78.2083),
    'coonoor': (11.3530, 76.7959),
    'valparai': (10.3270, 76.9530),
    'meghamalai': (9.7170, 77.4420),
    'kotagiri': (11.4213, 76.8597),
    'horsley hills': (13.6597, 78.3950),
    'araku': (18.3273, 82.8759),
    
    # Historical / Cultural
    'taj mahal': (27.1751, 78.0421),
    'agra': (27.1767, 78.0081),
    'hampi': (15.3350, 76.4600),
    'khajuraho': (24.8318, 79.9199),
    'konark': (19.8876, 86.0945),
    'mahabalipuram': (12.6172, 80.1927),
    'ajanta': (20.5519, 75.7033),
    'ellora': (20.0258, 75.1780),
    'meenakshi': (9.9195, 78.1193),
    'madurai': (9.9252, 78.1198),
    'mysore': (12.3051, 76.6551),
    'jaipur': (26.9124, 75.7873),
    'varanasi': (25.3176, 83.0036),
    'amritsar': (31.6200, 74.8765),
    'fatehpur': (27.0945, 77.6679),
    
    # Nature / Wildlife
    'periyar': (9.4680, 77.2350),
    'ranthambore': (26.0173, 76.5026),
    'kaziranga': (26.5775, 93.1711),
    'jim corbett': (29.5300, 78.7747),
    'sundarbans': (21.9497, 88.8987),
    'gir': (21.1243, 70.7944),
    'bandipur': (11.6686, 76.6336),
    'nagarhole': (12.0757, 76.1517),
    'dudhsagar': (15.3144, 74.3143),
    'jog falls': (14.2295, 74.8127),
    'athirappilly': (10.2853, 76.5698),
    
    # Adventure
    'rishikesh': (30.0869, 78.2676),
    'leh': (34.1526, 77.5771),
    'ladakh': (34.1526, 77.5771),
    'spiti': (32.2464, 78.0350),
    'bir billing': (31.9783, 76.7520),
    'coorg adventure': (12.3375, 75.8069),
    
    # Cities
    'delhi': (28.6139, 77.2090),
    'mumbai': (19.0760, 72.8777),
    'bangalore': (12.9716, 77.5946),
    'bengaluru': (12.9716, 77.5946),
    'chennai': (13.0827, 80.2707),
    'kolkata': (22.5726, 88.3639),
    'hyderabad': (17.3850, 78.4867),
    'pune': (18.5204, 73.8567),
    'kochi': (9.9312, 76.2673),
    'goa': (15.2993, 74.1240),
    'udaipur': (24.5854, 73.7125),
    'jodhpur': (26.2389, 73.0243),
    
    # Temples
    'tirupati': (13.6288, 79.4192),
    'tirumala': (13.6833, 79.3474),
    'rameshwaram': (9.2876, 79.3129),
    'kedarnath': (30.7352, 79.0669),
    'badrinath': (30.7433, 79.4938),
    'somnath': (20.8880, 70.4014),
    'puri': (19.8135, 85.8312),
    'dwarka': (22.2394, 68.9678),
    'vaishno devi': (33.0308, 74.9490),
    'sri rangam': (10.8560, 78.6900),
    'brihadeeswarar': (10.7828, 79.1318),
    'thanjavur': (10.7870, 79.1378),
    'kanchi': (12.8342, 79.7036),
    'kanchipuram': (12.8342, 79.7036),
    'chidambaram': (11.3993, 79.6912),
    'srirangapatna': (12.4180, 76.6947),
    'belur': (13.1631, 75.8628),
    'halebidu': (13.2134, 75.9916),
}

updated = 0
skipped = 0

for place in Place.objects.all():
    name_lower = place.name.lower()
    loc_lower = place.location.lower()
    matched = False
    
    for key, (lat, lng) in GPS_DATA.items():
        if key in name_lower or key in loc_lower:
            place.latitude = lat
            place.longitude = lng
            place.save(update_fields=['latitude', 'longitude'])
            print(f"  ✓ {place.name} → ({lat}, {lng})")
            updated += 1
            matched = True
            break
    
    if not matched:
        skipped += 1
        print(f"  ✗ {place.name} | {place.location} — no GPS match")

print(f"\nPlaces: {updated} updated, {skipped} no match")

# Also seed some destinations with coordinates if they exist
dest_updated = 0
for dest in Destination.objects.all():
    name_lower = dest.name.lower()
    loc_lower = dest.location.lower()
    for key, (lat, lng) in GPS_DATA.items():
        if key in name_lower or key in loc_lower:
            dest.latitude = lat
            dest.longitude = lng
            dest.save(update_fields=['latitude', 'longitude'])
            print(f"  ✓ Dest: {dest.name} → ({lat}, {lng})")
            dest_updated += 1
            break

print(f"Destinations: {dest_updated} updated")
print("\nDone! GPS coordinates seeded.")
