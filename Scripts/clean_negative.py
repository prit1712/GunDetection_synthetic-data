import os
import shutil

# Source folder with JPGs and TXTs 
source_folder = "/home/tlab/Desktop/2nd_TRY/outputs/run_01"

# Destination folder
destination_folder = "/home/tlab/Desktop/2nd_TRY/outputs/-ve_run_01"
os.makedirs(destination_folder, exist_ok=True)

# Loop through all TXT files
for file in os.listdir(source_folder):
    if file.endswith(".txt"):  
        txt_path = os.path.join(source_folder, file)

        # Check if TXT file size is 0 bytes
        if os.path.getsize(txt_path) == 0:
            jpg_file = file.replace(".txt", ".jpg")  # Matching JPG name
            jpg_path = os.path.join(source_folder, jpg_file)

            # Move TXT file
            shutil.move(txt_path, os.path.join(destination_folder, file))
            print(f"Moved: {file}")

            # Move corresponding JPG (if exists)
            if os.path.exists(jpg_path):
                shutil.move(jpg_path, os.path.join(destination_folder, jpg_file))
                print(f"Moved: {jpg_file}")

print(" Done!")

