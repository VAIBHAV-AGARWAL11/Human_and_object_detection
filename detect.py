from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    results = model.track(frame, persist=True, classes=[0])

    annotated_frame = results[0].plot()

    cv2.imshow("Human Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()