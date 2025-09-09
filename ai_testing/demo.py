import cv2
import numpy as np
from ultralytics import FastSAM


model = FastSAM("FastSAM-s.pt")  # hoặc FastSAM-x.pt


drawing = False  # đang vẽ
ix, iy = -1, -1
img = None

def crop_object_from_mask(img, bbox, mask=None, padding=0):
    img_proc = img.copy()
    mask_3ch = None
    if mask is not None:
        mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
        mask_3ch = np.stack([mask_resized]*3, axis=-1)
        img_proc = img_proc * (mask_3ch > 0)
    x_min, y_min, x_max, y_max = map(int, bbox)
    x_min_pad = max(x_min - padding, 0)
    y_min_pad = max(y_min - padding, 0)
    x_max_pad = min(x_max + padding, img.shape[1]-1)
    y_max_pad = min(y_max + padding, img.shape[0]-1)
    crop = img_proc[y_min_pad:y_max_pad+1, x_min_pad:x_max_pad+1].copy()
    if mask_3ch is not None:
        mask_crop = mask_3ch[y_min_pad:y_max_pad+1, x_min_pad:x_max_pad+1].copy()
        return mask_crop
    return crop


def draw_bbox(event, x, y, flags, param):
    global ix, iy, drawing, img
    image = img.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Image", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x_min, y_min = min(ix, x), min(iy, y)
        x_max, y_max = max(ix, x), max(iy, y)
        bbox = [x_min, y_min, x_max, y_max]

        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.imshow("Image", img)
        print(f"BBox: {bbox}")

        results = model(img, bboxes=bbox, device="cuda", conf=0.7, iou=0.9)
        if results[0].boxes is not None and len(results[0].boxes) > 0:
            # Lấy contour từ mask (nếu có)
            if results[0].masks is not None:
                b_mask = np.zeros(img.shape[:2], np.uint8)
                contour = results[0].masks.xy[0].astype(np.int32).reshape(-1, 1, 2)
                cv2.drawContours(b_mask, [contour], -1, (255, 255, 255), cv2.FILLED)

                # Mask 3 kênh và AND với ảnh gốc
                mask3ch = cv2.cvtColor(b_mask, cv2.COLOR_GRAY2BGR)
                isolated = cv2.bitwise_and(img, mask3ch)
                cv2.imshow("Isolated Object (Mask)", isolated)
                cv2.imwrite("isolated_object.png", isolated)

            # Lấy bbox và crop ảnh gốc
            x1, y1, x2, y2 = results[0].boxes.xyxy[0].cpu().numpy().astype(int)
            cropped = isolated[y1:y2, x1:x2]
            cv2.imshow("Cropped Object (BBox)", cropped)


        # masks = results[0].masks.data.cpu().numpy() if results[0].masks is not None else None
        # cv2.imshow("Masks",masks[0])

        # if masks is not None and len(masks) > 0:
        #     object_crop = crop_object_from_mask(image, bbox, masks[0], padding=10)
        #     cv2.imwrite("object_crop.png", object_crop)

        # results[0].show()  # hoặc plot() nếu muốn lấy numpy array


if __name__ == "__main__":
    img = cv2.imread("test.jpg")
    
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", draw_bbox)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
