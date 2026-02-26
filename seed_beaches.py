import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_project.settings")
django.setup()

from explorer.models import Place

# Reliable free beach image URLs (direct downloads, no redirect chains)
beach_images = {
    "Radhanagar Beach": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Radhanagar_Beach_Havelock_Island.jpg/1280px-Radhanagar_Beach_Havelock_Island.jpg",
    "Palolem Beach": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Palolem_beach%2C_goa.jpg/1280px-Palolem_beach%2C_goa.jpg",
    "Varkala Beach": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Varkala_cliff_beach.jpg/1280px-Varkala_cliff_beach.jpg",
    "Marina Beach": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Marina_beach_Chennai_at_sunrise.jpg/1280px-Marina_beach_Chennai_at_sunrise.jpg",
    "Agonda Beach": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Agonda_beach_from_north.jpg/1280px-Agonda_beach_from_north.jpg",
}

# Fallback generic beach images (guaranteed to work)
fallback_urls = [
    "https://picsum.photos/seed/beach1/1200/800",
    "https://picsum.photos/seed/beach2/1200/800",
    "https://picsum.photos/seed/beach3/1200/800",
    "https://picsum.photos/seed/beach4/1200/800",
    "https://picsum.photos/seed/beach5/1200/800",
]

beaches = Place.objects.filter(category='BEACH')
print(f"Found {beaches.count()} beach(es) in DB")

for i, place in enumerate(beaches):
    if not place.image:
        urls_to_try = []
        if place.name in beach_images:
            urls_to_try.append(beach_images[place.name])
        urls_to_try.append(fallback_urls[i % len(fallback_urls)])

        downloaded = False
        for url in urls_to_try:
            print(f"Trying image for '{place.name}': {url[:60]}...")
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                })
                resp = urllib.request.urlopen(req, timeout=15)
                if resp.status == 200:
                    img_data = resp.read()
                    filename = f"beach_{place.id}.jpg"
                    place.image.save(filename, ContentFile(img_data), save=True)
                    print(f"  ✓ Saved for '{place.name}'")
                    downloaded = True
                    break
            except Exception as e:
                print(f"  ✗ Failed: {e}")

        if not downloaded:
            print(f"  ⚠ Could not download any image for '{place.name}'")
    else:
        print(f"  ✓ '{place.name}' already has an image: {place.image.name}")

print("\n✅ Done!")
