import cv2
import numpy as np
from bson.decimal128 import Decimal128
import torch
from pymongo import MongoClient
import logging
import threading
import requests
import time
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
        self.threshold = 0.42

        self.connect_db()

        self.product_embeddings = []
        self._stop_thread = False
        self._thread = threading.Thread(target=self._update_embeddings_periodically, daemon=True)
        self._thread.start()

        self.label_sended = []
    
    def get_embedding_db(self):
        product_embeddings = []
        products = list(self.collection.find({}))
        for prod in products:
            name = prod['name']
            embeddings = list(prod['embeddings'][0]) if 'embeddings' in prod and len(prod['embeddings']) > 0 else []
            price = prod.get('price', 0)
            id = prod.get('custom_id', 0)
            product_embeddings.append({
            "name": name,
            "embeddings": embeddings,
            "price": price,
            "id": id,
            "image": prod.get('org_images', "")[0]
        })
        return product_embeddings

    def _update_embeddings_periodically(self):
        while not self._stop_thread:
            try:
                self.product_embeddings = self.get_embedding_db()
            except Exception as e:
                logging.info(f"[ERROR] Updating embeddings failed: {e}")
            time.sleep(10) 

    def connect_db(self, uri="mongodb://superAdmin:Matkhau123%40@localhost:27017/", db_name="smartcartdb", collection_name="products_product"):
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
    
    def check_label(self, crop):
        products = list(self.collection.find({}))
        emb_crop = self.get_embedding(crop)

        for prod in self.product_embeddings:
            for emb_vec in prod['embeddings']:
                emb_db = torch.tensor(emb_vec, dtype=torch.float32).to('cuda')
                sim, is_same = self.verify_embedding(emb_crop, emb_db)
                if is_same:
                    return prod, sim
            # emb_db = torch.tensor(prod['embedding'], dtype=torch.float32).to('cuda')
            # sim, is_same = self.verify_embedding(emb_crop, emb_db)
            # if is_same:
            #     return prod['label'], sim
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
        results = self.fastsam_model.predict(frame,retina_masks=True, device="cuda",conf=0.8,iou=0.9)
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

    def get_object_from_fast_sam(self,frame, results):
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
            prod, sim = self.check_label(obj)
            if prod is not None:
                self.sent_to_cart_monitor(prod['image'], prod['name'], price=  float(prod['price'].to_decimal()), id=(prod['id']), quantity=1)
                x1, y1, x2, y2 = bboxs[i].astype(int)
                cv2.putText(image, f"{prod['name']} {sim:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                return 
            
    
    def sent_to_cart_monitor(self, image, label, price, id, quantity, api_endpoint="http://192.168.5.151:8000/carts/api/add_to_cart/"):
        if id in self.label_sended:
            return
        self.label_sended.append(id)
        product_data = {
            "id": id,
            "name": label,
            "price": price,
            "image":image,
            "quantity": quantity
        }
        response = requests.post(api_endpoint, json=product_data)



if __name__ == "__main__":
    camera = CartObjectRecognizer(camera_index=2)  # /dev/video2
    try:
        camera.start_camera()
        while True:
            # print(len(camera.product_embeddings))
            frame = camera.get_frame()
            annotated_frame, results = camera.run_fastsam_on_frame(frame)
            objects, bboxes, masks = camera.get_object_from_fast_sam(frame, results)
            camera.check_project_name(objects, bboxes, frame)

            cv2.imshow("USB Camera", frame)
            # cv2.imshow("Annotated", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.stop_camera()
        cv2.destroyAllWindows()
