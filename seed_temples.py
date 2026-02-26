import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_project.settings")
django.setup()

from explorer.models import Place

temples = [
    {
        "name": "Golden Temple (Harmandir Sahib)",
        "description": "The holiest shrine of Sikhism, the Golden Temple in Amritsar is a breathtaking structure covered in gold leaf, reflected in the serene Amrit Sarovar (Pool of Nectar). It welcomes over 100,000 visitors daily and serves free langar (community meals) to all, regardless of faith.",
        "location": "Amritsar, Punjab, India",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/The_Golden_Temple_of_Amritsar_7.jpg/1280px-The_Golden_Temple_of_Amritsar_7.jpg"
    },
    {
        "name": "Meenakshi Amman Temple",
        "description": "A magnificent Dravidian masterpiece in Madurai, the Meenakshi Amman Temple features 14 towering gopurams (temple towers) adorned with thousands of colorful sculptures. Dedicated to Goddess Meenakshi and Lord Sundareshwar, it is one of the grandest temples in India.",
        "location": "Madurai, Tamil Nadu, India",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Meenakshi_Amman_Temple.jpg/1280px-Meenakshi_Amman_Temple.jpg"
    },
    {
        "name": "Brihadeeswarar Temple",
        "description": "A UNESCO World Heritage Site built by Raja Raja Chola I in 1010 AD, the Brihadeeswarar Temple in Thanjavur is a pinnacle of Chola architecture. Its 216-foot vimana (tower) is made entirely of granite and casts no shadow at noon.",
        "location": "Thanjavur, Tamil Nadu, India",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Brihadeeswarar_temple_2015.jpg/1280px-Brihadeeswarar_temple_2015.jpg"
    },
    {
        "name": "Somnath Temple",
        "description": "One of the 12 Jyotirlinga shrines of Lord Shiva, the Somnath Temple stands at the confluence of three rivers on the Arabian Sea coast. Rebuilt seven times after repeated invasions, this temple symbolises resilience and faith. The shore temple setting at sunset is spectacular.",
        "location": "Veraval, Saurashtra, Gujarat, India",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Somnath_temple.jpg/1280px-Somnath_temple.jpg"
    },
    {
        "name": "Jagannath Temple",
        "description": "One of the Char Dhams and dedicated to Lord Jagannath (form of Vishnu), the Jagannath Temple in Puri is famous for the annual Rath Yatra chariot festival. The 65-metre-tall shikhara dominates the Puri skyline. Non-Hindus are not permitted inside, making it deeply sacred.",
        "location": "Puri, Odisha, India",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Jagannath_Temple_Puri.jpg/1280px-Jagannath_Temple_Puri.jpg"
    },
]

fallback_urls = [
    "https://picsum.photos/seed/temple1/1200/800",
    "https://picsum.photos/seed/temple2/1200/800",
    "https://picsum.photos/seed/temple3/1200/800",
    "https://picsum.photos/seed/temple4/1200/800",
    "https://picsum.photos/seed/temple5/1200/800",
]

print("Seeding temples into Explorer...")
for i, t in enumerate(temples):
    qs = Place.objects.filter(name=t['name'], category='TEMPLE')
    if qs.exists():
        place = qs.first()
        print(f"Already exists: {place.name}")
    else:
        place = Place.objects.create(
            name=t['name'],
            description=t['description'],
            location=t['location'],
            category='TEMPLE',
            image=''
        )
        print(f"Created: {place.name}")

    if not place.image:
        urls_to_try = [t['image_url'], fallback_urls[i % len(fallback_urls)]]
        for url in urls_to_try:
            print(f"  Downloading image from: {url[:70]}...")
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req, timeout=15)
                if resp.status == 200:
                    img_data = resp.read()
                    fname = f"temple_{place.id}.jpg"
                    place.image.save(fname, ContentFile(img_data), save=True)
                    print(f"  ✓ Image saved as {fname}")
                    break
            except Exception as e:
                print(f"  ✗ Failed: {e}")
    else:
        print(f"  ✓ Image already present: {place.image.name}")

print("\n✅ Done! Temples added to Explorer.")
print("Total temples:", Place.objects.filter(category='TEMPLE').count())
