import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_project.settings")
django.setup()

from bookings.models import Service

# Add some hotel services with Unsplash image URLs
hotel_services = [
    {
        "name": "Grand Palace Hotel",
        "description": "A luxury 5-star hotel in the heart of the city with great amenities and a pool.",
        "price_per_unit": 250.00,
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Seaside Resort & Spa",
        "description": "Relaxing beachfront resort with premium amenities and spa services.",
        "price_per_unit": 180.00,
        "image_url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Mountain View Lodge",
        "description": "Cozy lodge with scenic mountain views and hiking trails nearby.",
        "price_per_unit": 120.00,
        "image_url": "https://images.unsplash.com/photo-1517840901100-8179e982acb7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    }
]

# Random transport images
transport_images = [
    "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1541899481282-d53bffe3c3e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1558981806-ec527fa84c39?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1502877338535-766e1452684a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
]

print("Adding hotels and images...")
for h in hotel_services:
    # First, get or create the service
    qs = Service.objects.filter(type='HOTEL', name=h['name'])
    if not qs.exists():
        service = Service.objects.create(
            type='HOTEL',
            name=h['name'],
            description=h['description'],
            price_per_unit=h['price_per_unit'],
            rating=4.5
        )
    else:
        service = qs.first()
        
    if not service.image:
        print(f"Downloading image for {service.name}...")
        try:
            req = urllib.request.Request(h['image_url'], headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            if response.status == 200:
                img_data = response.read()
                service.image.save(f"hotel_{service.id}.jpg", ContentFile(img_data), save=True)
                print(f"Saved image for {service.name}")
        except Exception as e:
            print(f"Failed to download image for {service.name}: {e}")

print("Updating transports...")
transports = Service.objects.filter(type='TRANSPORT')
for i, t in enumerate(transports):
    if not t.image:
        img_url = transport_images[i % len(transport_images)]
        print(f"Downloading image for {t.name} from {img_url}...")
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            if response.status == 200:
                img_data = response.read()
                t.image.save(f"transport_{t.id}.jpg", ContentFile(img_data), save=True)
                print(f"Saved image for {t.name}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

print("Done.")
