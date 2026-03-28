import os
import cv2
import numpy as np
from pathlib import Path

# Define input and output directories
INPUT_FOLDER = "input_images"
LABELS_FOLDER = "input_labels"  # Folder containing YOLO label (.txt) files
OUTPUT_FOLDER = "augmented_images"
OUTPUT_LABELS = "augmented_labels"

# Create output folders if they don’t exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_LABELS, exist_ok=True)

def add_gaussian_noise(image):
    """Adds light Gaussian noise to an image (correctly and visibly)."""
    row, col, ch = image.shape
    mean = 0
    sigma = 20  # Reduced standard deviation for light noise
    gauss = np.random.normal(mean, sigma, (row, col, ch)).astype('float32')
    noisy_image = image.astype('float32') + gauss
    noisy_image = np.clip(noisy_image, 0, 255).astype('uint8')
    return noisy_image


def adjust_brightness(image, factor):
    """Adjusts brightness by a given factor (factor > 1 = brighter, factor < 1 = darker)."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * factor, 0, 255)  # Adjust V channel
    brightened_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return brightened_image

def flip_labels_horizontally(label_path, output_label_path):
    """Flips the bounding box x-coordinates in the YOLO label file for a horizontally flipped image."""
    if not os.path.exists(label_path):
        return  # No label file for this image
    
    with open(label_path, "r") as f:
        lines = f.readlines()
    
    flipped_lines = []
    for line in lines:
        parts = line.strip().split()
        class_id = parts[0]
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])
        
        # Flip x-coordinate (1 - old_x)
        x_center_new = 1.0 - x_center  
        
        flipped_lines.append(f"{class_id} {x_center_new:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    
    # Save new label file
    with open(output_label_path, "w") as f:
        f.writelines(flipped_lines)

def augment_image(image_path, label_path):
    """Applies augmentation, updates labels where needed, and saves the new images and labels."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Skipping {image_path}, cannot read file.")
        return
    
    filename = Path(image_path).stem  # Get file name without extension
    ext = Path(image_path).suffix  # Get file extension (.jpg, .png`, etc.)

    # Horizontal Flip (Image + Label)
    flipped = cv2.flip(img, 1)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{filename}_flipped{ext}"), flipped)
    flip_labels_horizontally(label_path, os.path.join(OUTPUT_LABELS, f"{filename}_flipped.txt"))

    # Add Noise
    noisy = add_gaussian_noise(img)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{filename}_noisy{ext}"), noisy)
    # Copy labels (No changes needed)
    if os.path.exists(label_path):
        os.system(f"cp {label_path} {os.path.join(OUTPUT_LABELS, f'{filename}_noisy.txt')}")

    # Increase Brightness
    brighter = adjust_brightness(img, 1.5)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{filename}_brighter{ext}"), brighter)
    # Copy labels
    if os.path.exists(label_path):
        os.system(f"cp {label_path} {os.path.join(OUTPUT_LABELS, f'{filename}_brighter.txt')}")

    # Decrease Brightness
    darker = adjust_brightness(img, 0.5)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{filename}_darker{ext}"), darker)
    # Copy labels
    if os.path.exists(label_path):
        os.system(f"cp {label_path} {os.path.join(OUTPUT_LABELS, f'{filename}_darker.txt')}")

def process_folder(input_folder, label_folder):
    """Processes all images and their corresponding labels in the input folder."""
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        label_path = os.path.join(label_folder, Path(image_file).stem + ".txt")  # Match label with image
        augment_image(image_path, label_path)

# Run augmentation on the dataset
process_folder(INPUT_FOLDER, LABELS_FOLDER)

print("Data augmentation complete. Augmented images and updated labels saved in:")
print("Images →", OUTPUT_FOLDER)
print("Labels →", OUTPUT_LABELS)

