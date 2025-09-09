from ultralytics import FastSAM
import cv2
import numpy as np

model = FastSAM("FastSAM-x.pt")
image = cv2.imread("test.jpg")
everything_results = model.predict(
    image,
    device="cuda",
    retina_masks=True,
    imgsz=1024,
    conf=0.9,  # confidence threshold
    iou=0.9,  # IoU threshold cho NMS
)

bboxes = everything_results[0].boxes.xyxy.cpu().numpy() if everything_results[0].boxes is not None else []
masks = everything_results[0].masks.data.cpu().numpy() if everything_results[0].masks is not None else []
print(len(masks), "objects detected")

for i in range(len(masks)):
    mask = (masks[i] * 255).astype("uint8")  
    print(image.shape,mask.shape,bboxes[i].shape)
    mask3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    isolated = cv2.bitwise_and(image, mask3ch)  
    cv2.imwrite(f"test/isolated_{i}.png", isolated)
    x1, y1, x2, y2 = bboxes[i].astype(int)
    cropped = isolated[y1:y2, x1:x2]
    cv2.imwrite(f"test/object_{i}.png", cropped)