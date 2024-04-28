#Testing the trained model .pt using opencv

import os
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

# Create a directory to save the cropped images
os.makedirs('cropped_books', exist_ok=True)

# Load the pretrained model
model = YOLO('yolov8n.pt')  # replace 'yolov5.pt' with the path to your YOLOv8 model file

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Perform object detection on the frame
    results = model.predict(frame)
    #add some delay

    # Draw the detection results on the frame
    for r in results:
        
        annotator = Annotator(frame)
        
        boxes = r.boxes
        for i, box in enumerate(boxes):
            
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            class_name = model.names[int(c)]
            annotator.box_label(b, model.names[int(c)])
            
			# Check if the class name is 'book'
            if class_name == 'book':
            # Crop the detected object from the frame
                left, top, right, bottom = map(int, b)
                cropped = frame[top:bottom, left:right]
            
                # Save the cropped image to a file
                cv2.imwrite(f'cropped_books/book_{i}.jpg', cropped)

    # Display the frame
    cv2.imshow('Object Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()