#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# SURGICAL COMPRESSION

import os
import csv
from PIL import Image
import sys

# Raise the CSV field limit for long archival paths
csv.field_size_limit(10000000)

# --- CONFIGURATION ---
input_csv = r'./UMF_Database_image_list_1.csv'
demo_folder = r'./Gust_Images'

# We set this high so it runs the whole batch, but skips the heavy stuff
sample_limit = 50000 
# approved_prefixes = ('UMF', 'UMFB', 'B', 'AES', 'UAS' 'FS', 'EC', 'PL')

def create_vendor_demo():
    webp_dir = os.path.join(demo_folder, 'WebP_Compressed')
    os.makedirs(webp_dir, exist_ok=True)
    
    demo_log_path = os.path.join(demo_folder, 'UMF_Image_Migration_Log.csv')
    count = 0
    demo_data = []

    print(f"🚀 Starting Surgical JPEG Migration...")

    with open(input_csv, mode='r', encoding='utf-8-sig') as infile:
        first_line = infile.readline()
        infile.seek(0)
        delimiter = ';' if ';' in first_line else ','
        
        reader = csv.DictReader(infile, delimiter=delimiter)
        reader.fieldnames = [n.strip().replace('\ufeff', '') for n in reader.fieldnames]

        for row in reader:
            if count >= sample_limit:
                break
            
            src = row.get('Full Path')
            fname = row.get('File Name')

            if not src or not fname:
                continue

            # --- THE FILTERS ---
            # 1. Skip if it's not a JPEG (Prevents VPN lag from TIFs)
            if not src.lower().endswith(('.jpg', '.jpeg', '.tif', '.nef')):
                continue

            # 2. Skip if it doesn't match your database prefixes
            if not fname.upper().startswith(approved_prefixes):
                # Optional: print(f"⏩ Skipping non-standard name: {fname}")
                continue

            if os.path.exists(src):
                try:
                    clean_name = os.path.splitext(fname)[0]
                    # We use the clean name so TIFs can "slide in" later with the same name
                    webp_name = f"{clean_name}.webp" 
                    webp_path = os.path.join(webp_dir, webp_name)
                    
                    # Skip if we already converted it in a previous run
                    if os.path.exists(webp_path):
                        count += 1
                        continue

                    with Image.open(src) as img:
                        if img.mode in ("RGBA", "P", "CMYK", "LA"):
                            img = img.convert("RGB")
                        img.save(webp_path, "WEBP", quality=80)
                    
                    row['New_WebP_Name'] = webp_name
                    row['Local_WebP_Path'] = webp_path
                    demo_data.append(row)
                    
                    count += 1
                    if count % 20 == 0:
                        print(f"✅ {count} priority JPEGs compressed...")
                        
                except Exception as e:
                    print(f"❌ Error on {fname}: {e}")
            else:
                continue

    # Write the new Log
    if demo_data:
        keys = demo_data[0].keys()
        with open(demo_log_path, 'w', newline='', encoding='utf-8-sig') as out:
            writer = csv.DictWriter(out, fieldnames=keys)
            writer.writeheader()
            writer.writerows(demo_data)
        
        print(f"\n✨ SUCCESS!")
        print(f"📂 Processed {count} images.")
        print(f"📝 New Mapping CSV: {demo_log_path}")
    else:
        print("\n❌ No matching JPEGs found. Check your prefixes or CSV paths!")

if __name__ == "__main__":
    create_vendor_demo()


