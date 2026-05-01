# 🚦 Real-Time Traffic Sign Detection and Driver Assistance System

An intelligent **real-time traffic sign detection and driver assistance web application** built using **YOLOv8, FastAPI, OpenCV, WebSocket, HTML/CSS/JavaScript**, and **Text-to-Speech alerts**.

The system detects road traffic signs from:

* 📱 **Live smartphone camera stream**
* 🎬 **Uploaded video files**

and instantly provides:

* ✅ Bounding box detection
* ✅ Traffic sign classification
* ✅ Driver advice message
* ✅ Visual alert notification
* ✅ Voice warning assistance

---

## 📌 Project Overview

Road traffic sign recognition is an important component of modern **Advanced Driver Assistance Systems (ADAS)**.

This project proposes a lightweight yet powerful solution capable of:

* detecting **43 German traffic sign classes**
* processing camera/video streams in near real-time
* reducing false positives using smart validation
* helping the driver with contextual instructions and speech warnings

The detection model is trained on the **GTSRB (German Traffic Sign Recognition Benchmark)** dataset and deployed inside a **FastAPI WebSocket streaming server**.

---

## ✨ Features

### 🚀 Dual Detection Modes

* **Live Camera Mode** using smartphone IP camera stream
* **Video Upload Mode** for offline analysis

### 🧠 AI Detection Engine

* YOLOv8 custom trained model
* 43 traffic sign classes
* confidence filtering
* false positive reduction
* multi-frame validation

### 🔊 Driver Assistance System

* automatic voice warnings
* visual danger alerts
* contextual driving recommendations

### 🌐 Modern Web Interface

* live annotated frames
* detection history console
* dynamic detection cards
* upload drag & drop support
* responsive dashboard

---

## 🛠 Technologies Used

| Technology           | Purpose             |
| -------------------- | ------------------- |
| Python               | Backend logic       |
| FastAPI              | Web server          |
| OpenCV               | Video frame capture |
| YOLOv8 (Ultralytics) | Object detection    |
| WebSocket            | Real-time streaming |
| HTML/CSS/JavaScript  | Frontend UI         |
| pyttsx3              | Voice synthesis     |
| GTSRB Dataset        | Model training      |

---

## 📂 Project Structure

```bash
traffic-sign-detection-yolov8/
│
├── app.py
├── index.html
├── prepare_data.py
├── Article.js
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   └── put_model_here.txt
│
├── sounds/
│
└── scripts/
```

---

## 🧠 Supported Traffic Sign Classes

The model supports detection of **43 road sign categories**, including:

* Stop
* No Entry
* Yield
* Priority Road
* Speed Limits
* Slippery Road
* Road Work
* Pedestrians
* Children Crossing
* Wild Animals Crossing
* Turn Right / Left
* Roundabout
* Traffic Signals
* and many more...

---

## ⚙ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/traffic-sign-detection-yolov8.git
cd traffic-sign-detection-yolov8
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Place Trained Model

Put your trained YOLO model inside:

```bash
models/yolov8_signs.pt
```

### 4. Run Application

```bash
python app.py
```

Open browser:

```bash
http://localhost:8000
```

---

## 📸 Detection Workflow

### Camera Mode

1. Connect smartphone camera using DroidCam/IP Webcam
2. Paste camera URL
3. Start live detection

### Video Mode

1. Upload road video
2. System analyzes frames automatically
3. Driver receives sign warnings

---

## 🔊 Driver Assistance Logic

Each detected traffic sign triggers:

* sign classification
* confidence score
* contextual driver recommendation
* vocal warning alert

Examples:

| Sign        | Voice Warning    | Advice                            |
| ----------- | ---------------- | --------------------------------- |
| STOP        | "Attention Stop" | Stop completely before proceeding |
| No Entry    | "Sens interdit"  | Access prohibited                 |
| Speed Limit | "Reduce speed"   | Respect the speed limitation      |

---

## 📈 Performance

* Average Detection Confidence: **70% – 95%**
* Camera Mode Speed: **15–20 FPS**
* Video Mode Optimized Processing
* Low Latency WebSocket Streaming
* CPU Friendly Deployment

---

## 🎯 Future Improvements

* GPS integration
* ONNX edge deployment
* lane detection
* pedestrian detection
* mobile application version
* multilingual voice assistant

---

## 👨‍💻 Author

Developed as an academic deep learning and intelligent transportation project.

---

## 📄 License

This project is open-source for educational and research purposes.
