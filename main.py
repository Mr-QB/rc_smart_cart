from ultralytics import YOLO
import cv2

video_path = 'test.mp4'
model_path = r'C:\Users\hoang\Desktop\retail_product_detection\models\bob_yolov8\best.pt'

model = YOLO(model_path)

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, task='segment', conf=0.75, show=False, verbose=False)
    annotated_frame = results[0].plot()

    # Hiển thị
    cv2.imshow("Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
