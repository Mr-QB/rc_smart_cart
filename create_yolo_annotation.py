import cv2
import os
import yaml
import requests
from pathlib import Path

drawing = False
ix, iy = -1, -1
bboxes = []
current_class = 0

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, bboxes
    img = param["img"].copy() 

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img_temp = img.copy()
        cv2.rectangle(img_temp, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.putText(img_temp, f"Class: {param['class_names'][current_class]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("frame", img_temp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bboxes.append((current_class, ix, iy, x, y))
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.putText(img, f"Class: {param['class_names'][current_class]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("frame", img)
        param["img"] = img  

# Hàm chuyển đổi tọa độ bounding box sang định dạng YOLO
def convert_to_yolo_format(bboxes, img_width, img_height):
    yolo_annotations = []
    for class_id, x1, y1, x2, y2 in bboxes:
        x_center = (x1 + x2) / 2 / img_width
        y_center = (y1 + y2) / 2 / img_height
        width = abs(x2 - x1) / img_width
        height = abs(y2 - y1) / img_height
        yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    return yolo_annotations

# Hàm gửi file qua HTTP API
def upload_file_to_server(image_path, label_path, yaml_path, server_url="http://localhost:5000/upload"):
    try:
        files = {}
        if image_path:
            files['image'] = open(image_path, 'rb')
        if label_path:
            files['label'] = open(label_path, 'rb')
        if yaml_path:
            files['data_yaml'] = open(yaml_path, 'rb')

        response = requests.post(server_url, files=files)
        for f in files.values():
            f.close()

        if response.status_code == 200:
            print(f"Đã gửi thành công: {image_path if image_path else ''}, {label_path if label_path else ''}, {yaml_path if yaml_path else ''}")
        else:
            print(f"Lỗi khi gửi: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Lỗi khi gửi file: {e}")

def create_yolo_annotations_and_upload(video_dir, output_dir, server_url, frame_step=30, target_size=(640, 640)):
    global bboxes, current_class

    if not os.path.exists(video_dir):
        raise FileNotFoundError(f"Thư mục {video_dir} không tồn tại. Vui lòng tạo thư mục và thêm video.")

    # Tạo thư mục đầu ra
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
    if not video_files:
        raise FileNotFoundError(f"video not found {video_dir}.")
    class_names = [os.path.splitext(f)[0] for f in video_files]  # Lấy tên file video làm tên lớp

    for video_idx, video_file in enumerate(video_files):
        video_path = os.path.join(video_dir, video_file)
        class_name = os.path.splitext(video_file)[0]
        current_class = video_idx  # Gán class_id dựa trên chỉ số video

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"don't open video: {video_file}")
            continue

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Chỉ xử lý frame theo frame_step
            if frame_count % frame_step == 0:
                # Resize frame về kích thước target_size
                frame = cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)
                bboxes = []  # Reset bounding box cho mỗi frame
                frame_name = f"{class_name}_frame_{frame_count:04d}.jpg"
                frame_copy = frame.copy()

                cv2.namedWindow("frame")
                cv2.setMouseCallback("frame", draw_rectangle, {"img": frame_copy, "class_names": class_names})

                print(f"Đang xử lý: {video_file}, frame {frame_count} (kích thước: {target_size})")
                print(" 's' save, 'q' forget, 'n' next frame.")

                while True:
                    cv2.imshow("frame", frame_copy)
                    key = cv2.waitKey(0) & 0xFF

                    if key == ord('s'):
                        if bboxes:
                            output_image_path = os.path.join(images_dir, frame_name)
                            cv2.imwrite(output_image_path, frame)

                            img_height, img_width = frame.shape[:2]
                            yolo_annotations = convert_to_yolo_format(bboxes, img_width, img_height)
                            label_file = os.path.join(labels_dir, frame_name.replace('.jpg', '.txt'))
                            with open(label_file, 'w') as f:
                                f.write('\n'.join(yolo_annotations))
                            print(f"Đã lưu frame {frame_name} và annotation vào {label_file}")

                            upload_file_to_server(output_image_path, label_file, None, server_url)
                            break
                        else:
                            print("Chưa vẽ bounding box nào!")

                    # forget frame
                    elif key == ord('q'):
                        print(f"forget frame {frame_count}")
                        break

                    elif key == ord('n'):
                        break

                cv2.destroyWindow("frame")

            frame_count += 1

        cap.release()

    # creat data.yaml
    data_yaml = {
        'train': os.path.join(output_dir, 'images').replace('\\', '/'),
        'val': os.path.join(output_dir, 'images').replace('\\', '/'),
        'nc': len(class_names),
        'names': class_names
    }
    yaml_path = os.path.join(output_dir, 'data.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(data_yaml, f)
    print(f"Đã tạo file data.yaml tại {yaml_path}")

    # push file data.yaml throught API
    upload_file_to_server(None, None, yaml_path, server_url)

# used API
if __name__ == "__main__":
    video_dir = r"C:\Users\hoang\Desktop\retail_product_detection\products"  
    output_dir = r"C:\Users\hoang\Desktop\retail_product_detection\data"  
    server_url = "http://localhost:5000/upload"  
    frame_step = 30  
    target_size = (640, 640)  
    create_yolo_annotations_and_upload(video_dir, output_dir, server_url, frame_step, target_size)