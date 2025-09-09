from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import torch
import cv2
from pymongo import MongoClient

device = "cuda"

processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
model = AutoModel.from_pretrained("facebook/dinov2-base").to(device)
model.eval()

def get_embedding(img):
    inputs = processor(images=img, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    emb = outputs.last_hidden_state[:, 0, :]  # CLS token
    emb = emb / emb.norm(dim=-1, keepdim=True)
    return emb.cpu()  # để chắc chắn có thể convert sang list

# ---- MongoDB setup ----
client = MongoClient("mongodb://superAdmin:Matkhau123%40@localhost:27017/")
db = client["cart_db"]
collection = db["embeddings"]

# ---- Tạo embedding và lưu vào Mongo ----
img_path = "test/object_5.png"
img = cv2.imread(img_path)
emb = get_embedding(img)

doc = {
    "label": "object_4",
    "embedding": emb.numpy().tolist(),  # chuyển sang list
    "path": img_path
}
collection.insert_one(doc)
print("Saved to MongoDB:", doc["label"])

# ---- Load embedding từ Mongo và convert về tensor ----
saved_doc = collection.find_one({"label": "object_4"})
emb_loaded = torch.tensor(saved_doc["embedding"], dtype=torch.float32)

print("Loaded embedding shape:", emb_loaded.shape)
