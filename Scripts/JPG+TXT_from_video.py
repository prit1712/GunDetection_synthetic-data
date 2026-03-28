''' THIS SCRIPT TAKES video folder as input in CLI , seperates each frames (.jpg) file and also generates empty (.txt) file, saves both files ( jpg as well as txt ) in an output folder or creates if does not exists ! '''


import cv2
import os
from datetime import datetime

def extract_frames(video_folder, output_folder, custom_source=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_files = sorted([f for f in os.listdir(video_folder) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))])

    if not video_files:
        print("No video files found in the folder.")
        return

    video_counter = 1  # To ensure unique timestamps for similar video timestamps

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Failed to open video: {video_file}")
            continue

        frame_count = 0

        # Use filename (without extension) as source name if custom_source is not provided
        source_name = custom_source if custom_source else os.path.splitext(video_file)[0]

        # Use the file's modification time for timestamp
        timestamp = datetime.fromtimestamp(os.path.getmtime(video_path))
        date_str = timestamp.strftime("%Y%m%d")
        time_str = timestamp.strftime("%H%M%S")

        # Append video_counter to ensure uniqueness
        time_str += f"_{video_counter:02d}"
        video_counter += 1

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Stop when video ends

            frame_name = f"{source_name}_Clipped_image_{date_str}_{time_str}_frame_{frame_count:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_name)
            cv2.imwrite(frame_path, frame)

            # Create corresponding empty .txt file
            txt_path = os.path.splitext(frame_path)[0] + ".txt"
            open(txt_path, 'w').close()

            frame_count += 1

        cap.release()

    print(f"Frames and text files saved in '{output_folder}'.")

# Example usage
video_folder = input("Enter the video folder path: ")
output_folder = input("Enter the output folder path: ")
custom_source = input("Enter a custom source name (leave empty to use video filename): ").strip()

custom_source = custom_source if custom_source else None  # Set None if empty
extract_frames(video_folder, output_folder, custom_source)

