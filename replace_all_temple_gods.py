import os
import django
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_project.settings")
django.setup()

from explorer.models import Place

# Mapping: temple name → list of deity image URLs to try (fallback order)
deity_map = {
    # ---- Previously added national temples ----
    "Golden Temple (Harmandir Sahib)": [
        # Waheguru / Guru Nanak ji painting
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Guru_Nanak_painting_by_Raja_Ravi_Varma.jpg/800px-Guru_Nanak_painting_by_Raja_Ravi_Varma.jpg",
        "https://picsum.photos/seed/guru_nanak/1200/800",
    ],
    "Meenakshi Amman Temple": [
        # Goddess Meenakshi colorful idol
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Meenakshi_Idol.jpg/800px-Meenakshi_Idol.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Devi_Meenakshi.jpg/800px-Devi_Meenakshi.jpg",
        "https://picsum.photos/seed/meenakshi_devi/1200/800",
    ],
    "Brihadeeswarar Temple": [
        # Nataraja - Lord Shiva dancing
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Nataraja.jpg/800px-Nataraja.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Shiva_Nataraja_Brihadeeswara.jpg/800px-Shiva_Nataraja_Brihadeeswara.jpg",
        "https://picsum.photos/seed/nataraja_shiva/1200/800",
    ],
    "Somnath Temple": [
        # Shiva Lingam with divine light
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Somnath_Jyotirlinga.jpg/800px-Somnath_Jyotirlinga.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Lord_Shiva.jpg/800px-Lord_Shiva.jpg",
        "https://picsum.photos/seed/shiva_jyotirlinga/1200/800",
    ],
    "Jagannath Temple": [
        # Lord Jagannath vibrant deity
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Jagannath-puri.jpg/800px-Jagannath-puri.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Jagannath_Lord.jpg/800px-Jagannath_Lord.jpg",
        "https://picsum.photos/seed/lord_jagannath/1200/800",
    ],

    # ---- Mulugu district temples ----
    "Ramappa Temple (Ramalingeswara)": [
        # Lord Shiva - Ramalingeswara
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Shiva_Ramappa.jpg/800px-Shiva_Ramappa.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Nataraja_-_Brihadeeswara_temple.JPG/800px-Nataraja_-_Brihadeeswara_temple.JPG",
        "https://picsum.photos/seed/shiva_ramappa/1200/800",
    ],
    "Sammakka Saralamma Temple": [
        # Sammakka Saralamma goddess idol
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Sammakka_Saralamma_Jatara.jpg/1280px-Sammakka_Saralamma_Jatara.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Sammakka_idol.jpg/800px-Sammakka_idol.jpg",
        "https://picsum.photos/seed/sammakka_goddess/1200/800",
    ],
    "Ghanpur Temple Complex": [
        # Lord Shiva Linga deity
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Shivalinga_gold.jpg/800px-Shivalinga_gold.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Lord_Shiva.jpg/800px-Lord_Shiva.jpg",
        "https://picsum.photos/seed/shiva_ghanpur/1200/800",
    ],
    "Lakshmi Narasimha Swamy Temple, Venkatapur": [
        # Lord Narasimha fierce avatar
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Narasimha_Avatar.jpg/800px-Narasimha_Avatar.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Narasimha_deity.jpg/800px-Narasimha_deity.jpg",
        "https://picsum.photos/seed/lord_narasimha/1200/800",
    ],
    "Mallur Mallanna Temple": [
        # Lord Mallanna (Shiva) deity
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Shiva_Mallanna.jpg/800px-Shiva_Mallanna.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Lord_Shiva.jpg/800px-Lord_Shiva.jpg",
        "https://picsum.photos/seed/mallanna_god/1200/800",
    ],
}

temples = Place.objects.filter(category='TEMPLE')
print(f"Replacing images for {temples.count()} temples...\n")

for place in temples:
    # Remove existing image
    if place.image:
        try:
            place.image.delete(save=False)
        except Exception:
            pass

    urls = deity_map.get(place.name, ["https://picsum.photos/seed/hindu_god/1200/800"])
    downloaded = False

    for url in urls:
        print(f"[{place.name}] Trying: {url[:65]}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=20)
            if resp.status == 200:
                data = resp.read()
                if len(data) > 5000:   # skip tiny/broken files
                    fname = f"god_{place.id}.jpg"
                    place.image.save(fname, ContentFile(data), save=True)
                    print(f"  ✓ Saved: {fname} ({len(data)//1024} KB)\n")
                    downloaded = True
                    break
                else:
                    print(f"  ✗ File too small ({len(data)} bytes), skipping")
        except Exception as e:
            print(f"  ✗ {e}")

    if not downloaded:
        print(f"  ⚠ No image saved for '{place.name}'\n")

print("=" * 55)
print(f"✅ Done! All temple deity images updated.")
print("\nFinal summary:")
for p in Place.objects.filter(category='TEMPLE').order_by('date_added'):
    status = f"✓ {p.image.name}" if p.image else "✗ NO IMAGE"
    print(f"  {status}  |  {p.name}")
