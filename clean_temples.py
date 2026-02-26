import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_project.settings")
django.setup()

from explorer.models import Place

# Delete all temples from explorer
temples = Place.objects.filter(category='TEMPLE')
count = temples.count()

if count > 0:
    temples.delete()
    print(f"✅ Deleted {count} temples from explorer.")
else:
    print("ℹ️  No temples found to delete.")

print(f"Total places remaining in explorer: {Place.objects.count()}")
