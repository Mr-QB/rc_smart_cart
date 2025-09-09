import cv2
import numpy as np
import torch
from pymongo import MongoClient
import logging
from transformers import AutoImageProcessor, AutoModel
from ultralytics import FastSAM


class CartObjectRecognizer:
    def __init__(self, camera_index=2, width=1280, height=720, fps=30):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None

        self.fastsam_model = FastSAM("FastSAM-s.pt")
        
        self.dinov2_model_name = "facebook/dinov2-base"
        self.dinov2_processor = AutoImageProcessor.from_pretrained(self.dinov2_model_name)
        self.dinov2_model = AutoModel.from_pretrained(self.dinov2_model_name).to("cuda")
        self.dinov2_model.eval()
        self.threshold = 0.45

        self.connect_db()

    def connect_db(self, uri="mongodb://superAdmin:Matkhau123%40@localhost:27017/", db_name="cart_db", collection_name="embeddings"):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")

    def start_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            raise Exception(f"Could not open camera index {self.camera_index}")

        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

    def get_embedding(self, image):
        inputs = self.dinov2_processor(images=image, return_tensors="pt").to('cuda')
        with torch.no_grad():
            outputs = self.dinov2_model(**inputs)
        emb = outputs.last_hidden_state[:, 0, :]  
        emb = emb / emb.norm(dim=-1, keepdim=True)
        return emb

    def verify_embedding(self, emb1, emb2):
        similarity = (emb1 @ emb2.T).item()
        is_same = similarity >= self.threshold
        return similarity, is_same
    
    def check_label(self, crop, reference_db):
        products = list(self.collection.find({}))
        emb_crop = self.get_embedding(crop)

        for prod in products:
            emb_db = torch.tensor(prod['embedding'], dtype=torch.float32).to('cuda')
            sim, is_same = self.verify_embedding(emb_crop, emb_db)
            if is_same:
                return prod['label'], sim
        return None, None

    def get_frame(self):
        if self.cap is None:
            raise Exception("Camera is not started.")
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Failed to capture frame.")
        return frame

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def run_fastsam_on_frame(self, frame):
        results = self.fastsam_model.predict(frame,retina_masks=True, device="cuda",conf=0.7,iou=0.9)
        annotated_frame = results[0].plot()
        return annotated_frame, results

    def get_bboxes_and_masks(self, results):
        bboxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes is not None else []
        masks = results[0].masks.data.cpu().numpy() if results[0].masks is not None else []
        return bboxes, masks
    
    def crop_object_from_mask(self, image, bbox, mask=None, padding=0):
        mask = (mask * 255).astype("uint8")  
        mask3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        isolated = cv2.bitwise_and(image, mask3ch)  
        x1, y1, x2, y2 = bbox.astype(int)
        cropped = isolated[y1:y2, x1:x2]
        return cropped

    def get_object_from_fast_sam(self, results):
        objects = []
        bboxes, masks = self.get_bboxes_and_masks(results)

        for i in range(len(bboxes)):
            bbox = bboxes[i]
            mask = masks[i]
            obj_crop = self.crop_object_from_mask(frame, bbox, mask, padding=10)
            objects.append(obj_crop)
        return objects, bboxes, masks

    def check_project_name(self, objects, bboxs, image):
        for i, obj in enumerate(objects):
            label, sim = self.check_label(obj, self.collection)
            if label is not None:
                x1, y1, x2, y2 = bboxs[i].astype(int)
                cv2.putText(image, f"{label} {sim:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

if __name__ == "__main__":
    camera = CartObjectRecognizer(camera_index=2)  # /dev/video2
    try:
        camera.start_camera()
        while True:
            frame = camera.get_frame()
            annotated_frame, results = camera.run_fastsam_on_frame(frame)
            objects, bboxes, masks = camera.get_object_from_fast_sam(results)
            camera.check_project_name(objects, bboxes, frame)

            cv2.imshow("USB Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.stop_camera()
        cv2.destroyAllWindows()
