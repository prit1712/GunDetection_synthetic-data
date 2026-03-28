from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("/home/tlab/Desktop/2nd_TRY/dataset/runs/detect/train/weights/best.pt")

# Define path to directory containing images and videos for inference
source = "/home/tlab/Desktop/2nd_TRY/dataset/train/images"

# Run inference on the source
results = model(
    source,
    conf=0.4,
    save=True,
    project="/home/tlab/Desktop/2nd_TRY/dataset/runs/detect",
    name="my_output",
)
  # generator of Results objects
