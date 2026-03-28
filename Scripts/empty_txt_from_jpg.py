''' THIS SCRIPT takes a folder (expecting only jpgs inside it) as an input from CLI, reads all jpgs one by one, extracts the base file name (without .jpg extension), creates empty txt file with that exact same name and SAVES IT, if pre-existing txt file found in between while creating a empty txt file, than it will be OverWritten ( it will be emptyed , erasing all written texts) '''

import os

def create_empty_txt_files(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please provide a valid directory.")
        return
    
    # List all .jpg files in the folder
    jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
    
    if not jpg_files:
        print("No JPG files found in the folder.")
        return

    for jpg in jpg_files:
        txt_file = os.path.splitext(jpg)[0] + ".txt"  # Change extension to .txt
        txt_path = os.path.join(folder_path, txt_file)
        
        # Create an empty text file
        open(txt_path, 'w').close()
    
    print(f"Created {len(jpg_files)} empty .txt files in '{folder_path}'.")

# Example usage
folder = input("Enter the folder path: ")
create_empty_txt_files(folder)
