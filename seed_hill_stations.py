import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_project.settings")
django.setup()

from explorer.models import HillStation

hill_stations_data = [
    {
        "name": "Shimla",
        "city": "Shimla",
        "district": "Shimla",
        "state": "Himachal Pradesh",
        "country": "India",
        "description": "Shimla, the capital of Himachal Pradesh, is a picturesque hill station nestled in the Himalayan foothills. Known as the 'Queen of Hills', Shimla attracts thousands of tourists every year with its scenic beauty, pleasant climate, and colonial architecture. The town is famous for its ridge walks, toy train rides, temples, and adventure sports.",
        "best_time_to_visit": "March-June, September-October",
        "temperature_range": "5°C - 25°C",
        "latitude": 31.7683,
        "longitude": 77.1092,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Shimla_Vista.jpg/1280px-Shimla_Vista.jpg"
    },
    {
        "name": "Manali",
        "city": "Manali",
        "district": "Kullu",
        "state": "Himachal Pradesh",
        "country": "India",
        "description": "Manali is a popular hill station in the Kullu Valley, renowned for its stunning natural beauty and adventure tourism. Surrounded by majestic mountains, lush forests, and pristine rivers, Manali is a haven for trekkers, mountaineers, and nature lovers. The town offers activities like paragliding, river rafting, skiing, and hiking.",
        "best_time_to_visit": "March-June, September-October",
        "temperature_range": "10°C - 20°C",
        "latitude": 32.2396,
        "longitude": 77.1887,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Manali_Mountains.jpg/1280px-Manali_Mountains.jpg"
    },
    {
        "name": "Darjeeling",
        "city": "Darjeeling",
        "district": "Darjeeling",
        "state": "West Bengal",
        "country": "India",
        "description": "Darjeeling is a stunning hill station in the Himalayas, famous for its tea gardens, stunning views of Kanchenjunga, and its unique toy train. The town blends colonial charm with natural beauty, offering cool weather, emerald tea plantations, and a vibrant local culture.",
        "best_time_to_visit": "April-May, September-November",
        "temperature_range": "8°C - 18°C",
        "latitude": 27.0410,
        "longitude": 88.2663,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Darjeeling_Tea_Gardens.jpg/1280px-Darjeeling_Tea_Gardens.jpg"
    },
    {
        "name": "Ooty (Ootacamund)",
        "city": "Ooty",
        "district": "Nilgiris",
        "state": "Tamil Nadu",
        "country": "India",
        "description": "Ooty, nestled in the Nilgiri Mountains, is one of South India's most popular hill stations. Known as the 'Queen of the Nilgiris', Ooty captivates visitors with its cool climate, beautiful gardens, tea gardens, and scenic landscapes. The town offers boating, horse riding, and scenic toy train rides.",
        "best_time_to_visit": "May-June, October-November",
        "temperature_range": "15°C - 25°C",
        "latitude": 11.4102,
        "longitude": 76.7133,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Ooty_Lake.jpg/1280px-Ooty_Lake.jpg"
    },
    {
        "name": "Munnar",
        "city": "Munnar",
        "district": "Idukki",
        "state": "Kerala",
        "country": "India",
        "description": "Munnar is a scenic hill station in Kerala's Western Ghats, famous for its expansive tea gardens, cardamom hills, and misty landscapes. At 1,600 meters above sea level, Munnar offers a perfect escape with breathtaking views, cool climate, and rich biodiversity. The region is known for tea tourism and trekking.",
        "best_time_to_visit": "September-November, January-March",
        "temperature_range": "12°C - 25°C",
        "latitude": 10.5867,
        "longitude": 77.0595,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Munnar_Tea_Gardens.jpg/1280px-Munnar_Tea_Gardens.jpg"
    },
    {
        "name": "Nainital",
        "city": "Nainital",
        "district": "Nainital",
        "state": "Uttarakhand",
        "country": "India",
        "description": "Nainital, the 'City of Lakes', is a beautiful hill station nestled around the crescent-shaped Naini Lake. The town offers picturesque views of snow-capped Himalayas, pleasant climate, and numerous outdoor activities. Nainital is ideal for honeymooners, families, and adventure enthusiasts.",
        "best_time_to_visit": "March-June, September-October",
        "temperature_range": "8°C - 20°C",
        "latitude": 29.3919,
        "longitude": 79.4504,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Naini_Lake.jpg/1280px-Naini_Lake.jpg"
    },
    {
        "name": "Mussoorie",
        "city": "Mussoorie",
        "district": "Dehradun",
        "state": "Uttarakhand",
        "country": "India",
        "description": "Mussoorie, the 'Queen of Hills', is a charming hill station perched on the Himalayan foothills overlooking the Doon Valley. With its pleasant climate, scenic beauty, colonial architecture, and vibrant mall road, Mussoorie is a favorite destination for tourists and honeymooners.",
        "best_time_to_visit": "March-May, September-November",
        "temperature_range": "10°C - 25°C",
        "latitude": 30.4633,
        "longitude": 78.0686,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Mussoorie_Mall_Road.jpg/1280px-Mussoorie_Mall_Road.jpg"
    },
    {
        "name": "Coorg (Kodagu)",
        "city": "Madikeri",
        "district": "Kodagu",
        "state": "Karnataka",
        "country": "India",
        "description": "Coorg is a scenic hill station in the Western Ghats known for its lush green landscapes, coffee plantations, and pleasant climate. Nestled in mist-covered mountains, Coorg offers a perfect blend of nature, adventure, and leisure. The region is famous for coffee tourism, pepper plantations, and trekking.",
        "best_time_to_visit": "September-November, January-March",
        "temperature_range": "15°C - 25°C",
        "latitude": 12.3381,
        "longitude": 75.7304,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Coorg_Coffee_Plantations.jpg/1280px-Coorg_Coffee_Plantations.jpg"
    },
    {
        "name": "Coonoor",
        "city": "Coonoor",
        "district": "Nilgiris",
        "state": "Tamil Nadu",
        "country": "India",
        "description": "Coonoor, nestled in the Nilgiri Mountains, is a charming hill station offering stunning views of valleys and tea gardens. Known as the 'Gateway to Nilgiris', Coonoor is less crowded than Ooty and offers a peaceful escape with adventure activities like trekking and toy train rides.",
        "best_time_to_visit": "April-June, September-November",
        "temperature_range": "16°C - 26°C",
        "latitude": 11.6033,
        "longitude": 76.8097,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Coonoor_Tea_Gardens.jpg/1280px-Coonoor_Tea_Gardens.jpg"
    },
    {
        "name": "Kasauli",
        "city": "Kasauli",
        "district": "Solan",
        "state": "Himachal Pradesh",
        "country": "India",
        "description": "Kasauli is a serene hill station perched on a ridge overlooking the Sutlej River valley. This quiet retreat is perfect for those seeking peace and tranquility away from crowds. Known for adventure sports, nature walks, and colonial architecture, Kasauli offers a perfect blend of adventure and relaxation.",
        "best_time_to_visit": "March-June, September-October",
        "temperature_range": "8°C - 22°C",
        "latitude": 30.8078,
        "longitude": 76.6359,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Kasauli_Nature.jpg/1280px-Kasauli_Nature.jpg"
    },
]

fallback_urls = [
    "https://picsum.photos/seed/hillstation1/1200/800",
    "https://picsum.photos/seed/hillstation2/1200/800",
    "https://picsum.photos/seed/hillstation3/1200/800",
    "https://picsum.photos/seed/hillstation4/1200/800",
    "https://picsum.photos/seed/hillstation5/1200/800",
    "https://picsum.photos/seed/hillstation6/1200/800",
    "https://picsum.photos/seed/hillstation7/1200/800",
    "https://picsum.photos/seed/hillstation8/1200/800",
    "https://picsum.photos/seed/hillstation9/1200/800",
    "https://picsum.photos/seed/hillstation10/1200/800",
]

print("Seeding Hill Stations into Explorer...")
for i, hs_data in enumerate(hill_stations_data):
    qs = HillStation.objects.filter(name=hs_data['name'])
    if qs.exists():
        hill_station = qs.first()
        print(f"Already exists: {hill_station.name}")
    else:
        hill_station = HillStation.objects.create(
            name=hs_data['name'],
            city=hs_data['city'],
            district=hs_data['district'],
            state=hs_data['state'],
            country=hs_data['country'],
            description=hs_data['description'],
            best_time_to_visit=hs_data['best_time_to_visit'],
            temperature_range=hs_data['temperature_range'],
            latitude=hs_data['latitude'],
            longitude=hs_data['longitude'],
        )
        print(f"Created: {hill_station.name}")

    # Download and save image if not already present
    if not hill_station.image:
        urls_to_try = [hs_data['image_url'], fallback_urls[i % len(fallback_urls)]]
        for url in urls_to_try:
            print(f"  Downloading image from: {url[:70]}...")
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req, timeout=15)
                if resp.status == 200:
                    img_data = resp.read()
                    # Use a safe filename
                    fname = f"hill_station_{hill_station.id}.jpg"
                    hill_station.image.save(fname, ContentFile(img_data), save=True)
                    print(f"  ✓ Image saved as {fname}")
                    break
            except Exception as e:
                print(f"  ✗ Failed: {str(e)[:60]}")
    else:
        print(f"  ✓ Image already present: {hill_station.image.name}")

print("\n✅ Done! Hill Stations added to Explorer.")
print(f"Total hill stations: {HillStation.objects.count()}")
