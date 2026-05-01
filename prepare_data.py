import os
import shutil
import random

# --- CONFIGURATION ---
# Path to your existing folders
source_img_dir = 'dataset/archive/Train' 
source_lbl_dir = 'dataset/yolo_labels'
target_base = 'GTSRB_FINAL'
split_ratio = 0.8  # 80% Train, 20% Val

# 1. Create the new directory structure
for split in ['train', 'val']:
    os.makedirs(f'{target_base}/images/{split}', exist_ok=True)
    os.makedirs(f'{target_base}/labels/{split}', exist_ok=True)

# 2. Get all the labels you generated
all_labels = [f for f in os.listdir(source_lbl_dir) if f.endswith('.txt')]
random.shuffle(all_labels)

# 3. Split the list
split_idx = int(len(all_labels) * split_ratio)
train_list = all_labels[:split_idx]
val_list = all_labels[split_idx:]

def process_files(file_list, split_name):
    print(f"Processing {split_name} set...")
    for lbl_name in file_list:
        # Move Label
        shutil.copy(os.path.join(source_lbl_dir, lbl_name), 
                    os.path.join(target_base, 'labels', split_name, lbl_name))
        
        # Find and Move Image
        # We assume the image name matches the label name (e.g. 00001.txt -> 00001.png)
        img_name = lbl_name.replace('.txt', '.png') 
        
        # Search for the image in the 0-42 subfolders
        found = False
        for root, dirs, files in os.walk(source_img_dir):
            if img_name in files:
                shutil.copy(os.path.join(root, img_name), 
                            os.path.join(target_base, 'images', split_name, img_name))
                found = True
                break
        
        if not found:
            print(f"⚠️ Could not find image for {lbl_name}")

# Run the moving process
process_files(train_list, 'train')
process_files(val_list, 'val')

print("\n✅ Done! Your YOLO dataset is ready in 'GTSRB_FINAL'")