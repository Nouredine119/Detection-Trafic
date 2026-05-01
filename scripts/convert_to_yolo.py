from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # small YOLO model
model.train(
    data="GTSRB_FINAL/data.yaml", 
    epochs=10,        # 50 is too many for now; start with 10
    imgsz=128,        # Huge speed boost! GTSRB images are small anyway
    batch=4,          # Uses less RAM, helps the CPU breathe
    workers=2         # High worker counts can actually slow down older CPUs
)

# Save final weights
model.save("models/yolov8_signs.pt")