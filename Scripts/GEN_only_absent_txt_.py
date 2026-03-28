''' THIS SCRIPT TAKES a folder (expecting jpgs with their txts inside that folder) as an input in CLI, and scan all jpgs in folder searching for its corresponding (exactly same named) txts. if somewhere it founds negative jpg ( caused either by absence of object in image or by absence of bounding box labels ) then this script GENERATES & SAVES EMPTY TXT FILE for its corresponding jpg (exactly same named) ''' 
import os

# Take folder path input from the terminal
folder_path = input("Enter the folder path: ").strip()

# Check if the folder exists
if not os.path.isdir(folder_path):
    print("Invalid folder path. Please check and try again.")
    exit()

# Get lists of JPG and TXT files (without extensions)
jpg_files = {f[:-4] for f in os.listdir(folder_path) if f.endswith(".jpg")}
txt_files = {f[:-4] for f in os.listdir(folder_path) if f.endswith(".txt")}

# Find JPG files that don't have a corresponding TXT file
missing_txts = jpg_files - txt_files

# Create empty TXT files with the same name as missing ones
for file in missing_txts:
    txt_path = os.path.join(folder_path, f"{file}.txt")
    open(txt_path, 'w').close()  # Creates an empty TXT file

print(f"Created {len(missing_txts)} empty TXT files.")

