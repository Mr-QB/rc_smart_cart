from ultralytics import FastSAM

# Create a FastSAM model
model = FastSAM("FastSAM-s.pt")  # or FastSAM-x.pt

# Track with a FastSAM model on a video
results = model.track(
    source=0, imgsz=480, show=True, save=True, conf=0.5, device="cuda"
)  # webcam
