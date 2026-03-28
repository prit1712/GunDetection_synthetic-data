import cv2
import torch
import os
import argparse
import time
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="Overlay guns over detected hands from input.")
    parser.add_argument("--ip_folder", type=str, help="Path to folder of input videos.")
    parser.add_argument("--cam", type=str, help="Use '0' for webcam or provide an RTSP URL.")
    parser.add_argument("--model", type=str, required=True, help="Path to weights file.")
    parser.add_argument("--conf", type=float, default=0.65, help="Confidence threshold.")
    return parser.parse_args()

def main():
    args = parse_args()

    if bool(args.ip_folder) == bool(args.cam):
        print("Error: Provide **either** --ip_folder OR --cam (0 for webcam, RTSP link for stream).")
        exit()

    model = YOLO(args.model)
    C_T = args.conf

    # Create a unique output folder for each run (Indexed manner)
    output_base = "/home/tlab/Desktop/2nd_TRY/outputs"
    run_index = 1
    while os.path.exists(f"{output_base}/run_{run_index:02d}"):
        run_index += 1

    output_folder = f"{output_base}/run_{run_index:02d}"
    os.makedirs(output_folder, exist_ok=True)
    print(f"[INFO] Output frames will be saved in: {output_folder}")

    input_png = "/home/tlab/Desktop/2nd_TRY/PNG_L/Clipped_image_20250122_140614.png"
    sticker = cv2.imread(input_png, cv2.IMREAD_UNCHANGED)
    #if sticker is None:
    #    print("Error: Sticker not found.")
    #    exit()

    fixed_size = 100
    aspect_ratio = sticker.shape[1] / sticker.shape[0]
    new_w = fixed_size if aspect_ratio > 1 else int(fixed_size * aspect_ratio)
    new_h = int(fixed_size / aspect_ratio) if aspect_ratio > 1 else fixed_size
    sticker = cv2.resize(sticker, (new_w, new_h), interpolation=cv2.INTER_AREA)

    if args.ip_folder:
        video_sources = [os.path.join(args.ip_folder, f) for f in sorted(os.listdir(args.ip_folder)) if f.endswith((".mp4", ".avi", ".mov"))]
    else:
        video_sources = [0 if args.cam == "0" else args.cam]

    for idx, video_source in enumerate(video_sources, start=1):
        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            print(f"Error: Unable to open video source: {video_source}")
            continue

        output_path = os.path.join(output_folder, f"annotated_output_{idx:02d}.mp4") if args.ip_folder else os.path.join(output_folder, "annotated_output_live.mp4")

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        print(f"Processing: {video_source} → Saving as {output_path}")

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # Current date and time

            # 🔹 Save frames using timestamp and frame count to prevent overwriting
            base_filename = os.path.join(output_folder, f"frame_{timestamp}_{frame_count:07d}")
            processed_frame_filename = f"{base_filename}.jpg"
            annotation_filename = f"{base_filename}.txt"

            results = model(frame)
            detected = False
            annotations = []

            for result in results:
                for box in result.boxes:
                    conf = float(box.conf[0])
                    if conf >= C_T:
                        detected = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        box_width, box_height = x2 - x1, y2 - y1

                        sticker_aspect_ratio = sticker.shape[1] / sticker.shape[0]
                        new_w = box_width if box_width > box_height else int(box_height * sticker_aspect_ratio)
                        new_h = int(box_width / sticker_aspect_ratio) if box_width > box_height else box_height

                        resized_sticker = cv2.resize(sticker, (new_w, new_h), interpolation=cv2.INTER_AREA)
                        hand_center_x, hand_center_y = (x1 + x2) // 2, (y1 + y2) // 2
                        x1_s, y1_s = max(0, hand_center_x - new_w // 2), max(0, hand_center_y - new_h // 2)
                        x2_s, y2_s = min(frame.shape[1], x1_s + new_w), min(frame.shape[0], y1_s + new_h)

                        sticker_cropped = resized_sticker[0:(y2_s - y1_s), 0:(x2_s - x1_s)]
                        roi = frame[y1_s:y2_s, x1_s:x2_s]

                        if sticker_cropped.shape[2] == 4:
                            sticker_rgb = sticker_cropped[:, :, :3]
                            alpha_mask = sticker_cropped[:, :, 3] / 255.0
                            frame[y1_s:y2_s, x1_s:x2_s] = (1 - alpha_mask[:, :, None]) * roi + alpha_mask[:, :, None] * sticker_rgb
                        else:
                            frame[y1_s:y2_s, x1_s:x2_s] = sticker_cropped

                        img_h, img_w = frame.shape[:2]
                        x_center = (x1_s + x2_s) / 2 / img_w
                        y_center = (y1_s + y2_s) / 2 / img_h
                        w_norm = (x2_s - x1_s) / img_w
                        h_norm = (y2_s - y1_s) / img_h

                        annotations.append(f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}")
                        
                        # Draw bounding box around gun sticker
                        #cv2.rectangle(frame, (x1_s, y1_s), (x2_s, y2_s), (0, 0, 255), 2)

            cv2.imwrite(processed_frame_filename, frame)

            if detected:
                with open(annotation_filename, "w") as f:
                    f.write("\n".join(annotations))

            out.write(frame)
            cv2.imshow("Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        out.release()
        print(f"✅ Saved: {output_path}")

    cv2.destroyAllWindows()
    print("All videos processed successfully!")

if __name__ == "__main__":
    main()

