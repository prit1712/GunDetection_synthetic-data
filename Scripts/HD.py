import cv2
import torch
from ultralytics import YOLO
 
model = YOLO("/home/tlab/Desktop/2nd_TRY/best.pt") 	# LOADING MODEL INTO model VARIABLE

video_path = "/home/tlab/Desktop/2nd_TRY/cctv8.mp4" 	# PROVIDING video.mp4 AS AN INPUT / USE 0 FOR WEBCAM
cap = cv2.VideoCapture(video_path) 	# GET VIDEO INTO cap VARIABLE

while cap.isOpened():
	ret, frame = cap.read() 	# RETURN frame BY READING VIDEO WHILE cap is open   
	if not ret:
		break
		
	results = model(frame) 	# STORING OUTPUT FROM frame BY model IN results
	
	for result in results:
		for box in result.boxes:
			x1, y1, x2, y2 = map(int, box.xyxy[0]) 	# GET COORDINATES OF BOB FROM box.xyxy INTO variables
			conf = float(box.conf[0]) 		# GET CONFIDENCE FROM box.conf[0] INTO conf variables
			label = f"Hand {conf:.2f}"		# DRAW LABELING SHOWING Hand CLASS AND conf UPTO 2 FLOAT
			
			cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)	# DRAW rectangle
			cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)	# SHOWING TEXT
			
	cv2.imshow("hand_detection", frame) 	# SHOWING POPUP WINDOW NAMED hand_detection SHOWING RESULTS FROM frame
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
