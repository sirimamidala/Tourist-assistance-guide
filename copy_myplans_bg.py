import shutil
import os

source = r"C:\Users\Neha sri\.gemini\antigravity\brain\9aa03268-c5af-49d9-a398-756ef11c9d9e\my_plans_bg_1772048750080.png"
dest = r"c:\Users\Neha sri\Downloads\project\static\images\my-plans-bg.png"

os.makedirs(os.path.dirname(dest), exist_ok=True)
shutil.copy2(source, dest)
print(f"Copied {source} to {dest}")
