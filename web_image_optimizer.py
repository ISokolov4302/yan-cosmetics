import os
import sys
from PIL import Image
import string

def clean_name(name):
    # Transliteration or simple removal of non-ascii
    # For now, let's just remove non-ascii and clean up symbols
    name = name.lower()
    name = name.replace(' ', '-')
    valid_chars = "-_.%s%s" % (string.ascii_lowercase, string.digits)
    cleaned = ''.join(c for c in name if c in valid_chars)
    while '--' in cleaned:
        cleaned = cleaned.replace('--', '-')
    return cleaned.strip('-')

def optimize_images(source_dir, target_dir, max_width=800):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    processed_count = 0
    for filename in os.listdir(source_dir):
        # Skip targeted directory and script files
        if filename in ["images", "web_image_optimizer.py", "web_image_optimizer.exe"]:
            continue
            
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            try:
                img_path = os.path.join(source_dir, filename)
                with Image.open(img_path) as img:
                    # Rename
                    base_name = os.path.splitext(filename)[0]
                    new_name = clean_name(base_name) + ".webp"
                    
                    # Resize if too large
                    if img.width > max_width:
                        w_percent = (max_width / float(img.width))
                        h_size = int((float(img.height) * float(w_percent)))
                        img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
                    
                    # Save as WebP
                    target_path = os.path.join(target_dir, new_name)
                    img.save(target_path, "WEBP", quality=80)
                    print(f"Optimized: {filename} -> {new_name}")
                    processed_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return processed_count

if __name__ == "__main__":
    # Get directory of the script or exe
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("================================")
    print("YAN Cosmetics Image Optimizer v2")
    print("================================\n")
    
    # 1. Define possible source folders
    possible_sources = ["Ян прайс", "upload", "original_images", "."]
    source = None
    
    for ps in possible_sources:
        path = os.path.join(base_dir, ps)
        if os.path.exists(path):
            # If it's the current dir, we'll iterate files later
            # but we need to make sure we don't pick up 'images' folder
            source = path
            if ps != ".": # Found a specific folder, use it
                break

    target = os.path.join(base_dir, "images")
    
    print(f"Directory: {base_dir}")
    print(f"Source folder: {os.path.basename(source) if source else 'None'}")
    print(f"Target folder: images/\n")
    
    if source:
        processed = optimize_images(source, target)
        print(f"\nГотово! Обработано изображений: {processed}")
    else:
        print("Ошибка: Не найдена папка с исходными изображениями.")
    
    print("\nТеперь вы можете загрузить папку 'taplink_site' на Netlify.")
    input("\nНажмите Enter, чтобы выйти...")
