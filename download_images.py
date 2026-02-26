import urllib.request
import os

images_dir = r"c:\Users\Neha sri\Downloads\project\static\images"
os.makedirs(images_dir, exist_ok=True)

urls = [
    ("https://loremflickr.com/1600/900/emergency,ambulance", "emergency-bg.png"),
    ("https://loremflickr.com/1600/900/tropical,vacation", "my-plans-bg.png")
]

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
urllib.request.install_opener(opener)

for url, filename in urls:
    dest = os.path.join(images_dir, filename)
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, dest)

print("Images downloaded successfully!")
