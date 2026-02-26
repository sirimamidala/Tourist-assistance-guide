import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_project.settings")
django.setup()

from explorer.models import Place

# Attractive deity/god images for each temple (Wikipedia Commons - high quality)
temple_deity_images = {
    "Golden Temple (Harmandir Sahib)": [
        # Golden Temple illuminated at night - most iconic stunning view
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Golden_Temple_Reflection.jpg/1280px-Golden_Temple_Reflection.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/The_Golden_Temple_of_Amritsar_7.jpg/1280px-The_Golden_Temple_of_Amritsar_7.jpg",
        "https://picsum.photos/seed/golden_temple/1200/800",
    ],
    "Meenakshi Amman Temple": [
        # Goddess Meenakshi deity close-up
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Meenakshi_Idol.jpg/800px-Meenakshi_Idol.jpg",
        # Temple gopuram - striking colorful sculpture
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Gopuram_of_Meenakshi_Amman_Temple.jpg/1280px-Gopuram_of_Meenakshi_Amman_Temple.jpg",
        "https://picsum.photos/seed/meenakshi/1200/800",
    ],
    "Brihadeeswarar Temple": [
        # Lord Nataraja (Shiva dancing) - the iconic deity of Chola temples
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Nataraja_-_Brihadeeswara_temple.JPG/800px-Nataraja_-_Brihadeeswara_temple.JPG",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Brihadeeswarar_temple_2015.jpg/1280px-Brihadeeswarar_temple_2015.jpg",
        "https://picsum.photos/seed/shiva_nataraja/1200/800",
    ],
    "Somnath Temple": [
        # Lord Shiva lingam at Somnath
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Somnath_temple.jpg/1280px-Somnath_temple.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Somnath_Jyotirlinga.jpg/800px-Somnath_Jyotirlinga.jpg",
        "https://picsum.photos/seed/somnath_shiva/1200/800",
    ],
    "Jagannath Temple": [
        # Lord Jagannath deity - colorful and vibrant
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Jagannath-puri.jpg/800px-Jagannath-puri.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Jagannath_Temple_Puri.jpg/1280px-Jagannath_Temple_Puri.jpg",
        "https://picsum.photos/seed/jagannath/1200/800",
    ],
}

temples = Place.objects.filter(category='TEMPLE')
print(f"Found {temples.count()} temple(s). Replacing with deity images...\n")

for place in temples:
    urls = temple_deity_images.get(place.name, ["https://picsum.photos/seed/temple_god/1200/800"])

    # Delete old image file if present
    if place.image:
        try:
            old_path = place.image.path
            place.image.delete(save=False)
            print(f"🗑  Removed old image for: {place.name}")
        except Exception:
            pass

    downloaded = False
    for url in urls:
        print(f"  Trying: {url[:75]}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            resp = urllib.request.urlopen(req, timeout=20)
            if resp.status == 200:
                img_data = resp.read()
                fname = f"deity_{place.id}.jpg"
                place.image.save(fname, ContentFile(img_data), save=True)
                print(f"  ✓ Saved deity image '{fname}' for {place.name}\n")
                downloaded = True
                break
        except Exception as e:
            print(f"  ✗ {e}")

    if not downloaded:
        print(f"  ⚠ Could not download any image for '{place.name}'\n")

print("✅ All temple deity images updated!")
print("\nSummary:")
for p in Place.objects.filter(category='TEMPLE'):
    print(f"  {p.name}: {p.image.name if p.image else 'NO IMAGE'}")
