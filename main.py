# import cv2
# import numpy as np
# from ultralytics import YOLO

# # Load YOLOv8 segmentation model
# model = YOLO("yolov8s-seg.pt")  # Dùng model segmentation

# # Đọc ảnh đầu vào
# image_path = "/home/hoangkt/retail_product_detection/Screenshot from 2025-06-13 14-59-51.png"  # Đổi tên file ảnh đầu vào
# image = cv2.imread(image_path)

# # Dự đoán bằng YOLOv8
# results = model(image)[0]

# # Lấy mask và bbox
# masks = results.masks.data  # Tensor [N, H, W]
# boxes = results.boxes.xyxy  # Tensor [N, 4]

# # Xử lý từng object
# for i, mask in enumerate(masks):
#     # Chuyển mask sang ảnh nhị phân uint8
#     binary_mask = (mask.cpu().numpy() * 255).astype(np.uint8)

#     # Bbox
#     x1, y1, x2, y2 = boxes[i].cpu().numpy().astype(int)

#     # Kiểm tra bbox hợp lệ
#     if x2 <= x1 or y2 <= y1:
#         continue

#     # Cắt ảnh và mask
#     sub_image = image[y1:y2, x1:x2]
#     sub_mask = binary_mask[y1:y2, x1:x2]

#     # Bỏ qua nếu rỗng
#     if sub_image.size == 0 or sub_mask.size == 0:
#         continue

#     # Resize mask để khớp với ảnh
#     sub_mask_resized = cv2.resize(
#         sub_mask,
#         (sub_image.shape[1], sub_image.shape[0]),
#         interpolation=cv2.INTER_NEAREST
#     )

#     # Áp dụng mask
#     masked_image = cv2.bitwise_and(sub_image, sub_image, mask=sub_mask_resized)

#     # Hiển thị object đã tách nền
#     cv2.imshow(f"Object {i+1}", masked_image)

# # Hiển thị toàn bộ kết quả gốc có bbox
# annotated = results.plot()
# cv2.imshow("Detection", annotated)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np
from ultralytics import YOLO
import os

# ==== Cấu hình ====
video_path = "/home/hoangkt/retail_product_detection/video.mp4"  # ← Thay bằng đường dẫn file video của bạn
model_path = "yolov8m-seg.pt"
save_masked = False        # True nếu muốn lưu các object đã tách

# ==== Kiểm tra file video ====
if not os.path.exists(video_path):
    print(f"❌ Không tìm thấy video: {video_path}")
    exit()

# ==== Load model YOLOv8 segmentation ====
model = YOLO(model_path)

# ==== Mở video ====
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"❌ Không thể mở video: {video_path}")
    exit()

frame_count = 0
object_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("✅ Đã xử lý hết video.")
        break

    frame_count += 1

    # Phát hiện và phân đoạn bằng YOLOv8
    results = model(frame)[0]

    # Nếu có mask
    if results.masks is not None:
        masks = results.masks.data
        boxes = results.boxes.xyxy

        for i, mask in enumerate(masks):
            binary_mask = (mask.cpu().numpy() * 255).astype(np.uint8)
            x1, y1, x2, y2 = boxes[i].cpu().numpy().astype(int)

            if x2 <= x1 or y2 <= y1:
                continue

            sub_image = frame[y1:y2, x1:x2]
            sub_mask = binary_mask[y1:y2, x1:x2]

            if sub_image.size == 0 or sub_mask.size == 0:
                continue

            sub_mask_resized = cv2.resize(sub_mask, (sub_image.shape[1], sub_image.shape[0]), interpolation=cv2.INTER_NEAREST)
            masked_image = cv2.bitwise_and(sub_image, sub_image, mask=sub_mask_resized)

            # Hiển thị object đã tách
            window_name = f"Object {i}"
            cv2.imshow(window_name, masked_image)

            # Tuỳ chọn lưu ảnh object
            if save_masked:
                os.makedirs("masked", exist_ok=True)
                filename = f"masked/frame{frame_count}_obj{object_id}.png"
                cv2.imwrite(filename, masked_image)
                object_id += 1

    # Hiển thị khung có annotate
    annotated_frame = results.plot()
    cv2.imshow("YOLOv8 Segmentation", annotated_frame)

    # Nhấn Q để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Người dùng đã thoát.")
        break

cap.release()
cv2.destroyAllWindows()
