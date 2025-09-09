import sys
from mobile_sam import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import torch
import cv2
import numpy as np

image = cv2.imread("test.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

sam_checkpoint = "./ai_testing/MobileSAM/weights/mobile_sam.pt"
model_type = "vit_t"

device = "cuda" if torch.cuda.is_available() else "cpu"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
sam.eval()

mask_generator = SamAutomaticMaskGenerator(sam)

masks = mask_generator.generate(image)
for i, m in enumerate(masks):
    mask = m["segmentation"].astype(np.uint8) * 255  
    cv2.imwrite(f"mask_{i}.png", mask)
