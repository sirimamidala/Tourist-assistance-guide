import urllib.request
import os

images_dir = r"c:\Users\Neha sri\Downloads\project\static\images"
os.makedirs(images_dir, exist_ok=True)

# A highly thematic "travel planning" image (map, passport, camera on a table)
plan_url = "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1600&q=80"
plan_dest = os.path.join(images_dir, "my-plans-bg.png")

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
urllib.request.install_opener(opener)

print("Downloading new My Plans background...")
urllib.request.urlretrieve(plan_url, plan_dest)
print("New image downloaded successfully!")
