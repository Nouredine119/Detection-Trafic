import cv2
from ultralytics import YOLO
import time
import base64
import asyncio
import os
import tempfile

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# ============================
# 🔊 VOICE SYSTEM (FIX FINAL)
# ============================
import pyttsx3
import threading



def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('volume', 1.0)
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    threading.Thread(target=run, daemon=True).start()

def speak_label(label):
    label = label.lower()
    if "stop" in label:
        speak("Attention stop")
    elif "speed" in label:
        speak("Réduisez la vitesse")
    elif "no entry" in label:
        speak("Sens interdit")
    else:
        speak(label)

# ============================
# 🤖 MODEL
# ============================
model = YOLO("models/yolov8_signs.pt")


# ============================
# 🧠 ADVICE
# ============================
SIGN_ADVICE = {

    "Speed limit (20km/h)": ("⚡ 20 km/h", "Ralentissez fortement, zone très lente."),
    "Speed limit (30km/h)": ("⚡ 30 km/h", "Maintenez une vitesse réduite."),
    "Speed limit (50km/h)": ("⚡ 50 km/h", "Respectez la limite urbaine."),
    "Speed limit (60km/h)": ("⚡ 60 km/h", "Adaptez votre vitesse à la route."),
    "Speed limit (70km/h)": ("⚡ 70 km/h", "Restez sous la limite autorisée."),
    "Speed limit (80km/h)": ("⚡ 80 km/h", "Conduisez prudemment à vitesse moyenne."),
    "End of speed limit (80km/h)": ("🔓 Fin 80", "Fin de limitation, restez vigilant."),
    "Speed limit (100km/h)": ("⚡ 100 km/h", "Route rapide, gardez le contrôle."),
    "Speed limit (120km/h)": ("⚡ 120 km/h", "Autoroute, attention à la sécurité."),

    "No passing": ("🚫 Interdiction doubler", "Ne dépassez pas."),
    "No passing veh over 3.5t": ("🚫 Camions", "Dépassement interdit aux poids lourds."),

    "Right-of-way at intersection": ("⚠️ Priorité", "Vous avez la priorité."),
    "Priority road": ("🛣️ Route prioritaire", "Continuez avec priorité."),

    "Yield": ("⚠️ Cédez", "Ralentissez et cédez le passage."),
    "Stop": ("🛑 STOP", "Arrêtez-vous complètement."),

    "No vehicles": ("🚫 Véhicules", "Accès interdit aux véhicules."),
    "Veh > 3.5t prohibited": ("🚫 +3.5t", "Poids lourds interdits."),
    "No entry": ("⛔ Sens interdit", "N'entrez pas dans cette voie."),

    "General caution": ("⚠️ Danger", "Soyez très vigilant."),
    "Dangerous curve left": ("↩️ Virage gauche", "Ralentissez avant le virage."),
    "Dangerous curve right": ("↪️ Virage droite", "Ralentissez avant le virage."),
    "Double curve": ("🔀 Double virage", "Attention aux virages successifs."),

    "Bumpy road": ("🛤️ Route dégradée", "Réduisez la vitesse."),
    "Slippery road": ("💧 Glissant", "Attention au manque d'adhérence."),
    "Road narrows on the right": ("📉 Rétrécissement", "Route étroite, prudence."),
    "Road work": ("🚧 Travaux", "Ralentissez et suivez la signalisation."),

    "Traffic signals": ("🚦 Feux", "Respectez les feux de signalisation."),
    "Pedestrians": ("🚶 Piétons", "Attention aux passages piétons."),
    "Children crossing": ("👶 Enfants", "Zone scolaire, soyez prudent."),
    "Bicycles crossing": ("🚴 Vélo", "Attention aux cyclistes."),

    "Beware of ice/snow": ("❄️ Verglas", "Risque de glissement."),
    "Wild animals crossing": ("🦌 Animaux", "Attention aux animaux sauvages."),

    "End speed + passing limits": ("🔓 Fin restrictions", "Fin des limitations."),
    
    "Turn right ahead": ("➡️ Tourner droite", "Préparez-vous à tourner."),
    "Turn left ahead": ("⬅️ Tourner gauche", "Préparez-vous à tourner."),
    "Ahead only": ("⬆️ Tout droit", "Continuez tout droit."),
    "Go straight or right": ("↗️ Tout droit/droite", "Choisissez direction."),
    "Go straight or left": ("↖️ Tout droit/gauche", "Choisissez direction."),

    "Keep right": ("➡️ Garder droite", "Restez à droite."),
    "Keep left": ("⬅️ Garder gauche", "Restez à gauche."),

    "Roundabout mandatory": ("🔄 Rond-point", "Entrez dans le rond-point."),

    "End of no passing": ("🔓 Fin interdiction", "Dépassement autorisé."),
    "End no passing veh > 3.5t": ("🔓 Fin camions", "Dépassement autorisé aux camions.")
}

def get_advice(label):
    return SIGN_ADVICE.get(label, ("🔍 " + label, "Respectez le panneau."))

# ============================
# 🌐 APP
# ============================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# 🖥 HTML
# ============================
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# ============================
# 📤 UPLOAD
# ============================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tmp.write(await file.read())
    tmp.close()
    return {"path": tmp.name}

# ============================
# 📷 CAMERA
# ============================
@app.websocket("/ws/camera")
async def ws_camera(websocket: WebSocket, url: str):
    await websocket.accept()

    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        await websocket.send_json({"type": "error", "message": "Camera error"})
        return

    # 🔥 FIX : cooldown par label
    last_spoken_time = {}
    COOLDOWN = 3

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, imgsz=640, conf=0.35)

            detections = []

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    conf = float(box.conf[0])

                    if conf < 0.7:
                        continue

                    now = time.time()

                    # 🔊 SPEAK FIX FINAL
                    if label not in last_spoken_time or (time.time() - last_spoken_time[label] > COOLDOWN):
                        print("🔊 Speak:", label)
                        speak(label)
                        last_spoken_time[label] = time.time()

                    icon, advice = get_advice(label)

                    detections.append({
                        "label": label,
                        "conf": round(conf * 100, 1),
                        "icon_text": icon,
                        "advice": advice,
                        "is_new": True
                    })

            annotated = results[0].plot()
            _, buffer = cv2.imencode('.jpg', annotated)
            frame_b64 = base64.b64encode(buffer).decode()

            await websocket.send_json({
                "type": "frame",
                "frame": frame_b64,
                "detections": detections
            })

            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        pass
    finally:
        cap.release()

# ============================
# 🎬 VIDEO
# ============================
@app.websocket("/ws/video")
async def ws_video(websocket: WebSocket, path: str):
    await websocket.accept()

    cap = cv2.VideoCapture(path)

    last_spoken_time = {}
    detection_buffer = {}

    COOLDOWN = 4

    # 🔥 IMPORTANT : seulement panneaux (adapter selon ton modèle)
    ALLOWED = [
        'Speed limit (20km/h)', 'Speed limit (30km/h)', 'Speed limit (50km/h)', 'Speed limit (60km/h)', 
    'Speed limit (70km/h)', 'Speed limit (80km/h)', 'End of speed limit (80km/h)', 'Speed limit (100km/h)', 
    'Speed limit (120km/h)', 'No passing', 'No passing veh over 3.5t', 'Right-of-way at intersection', 
    'Priority road', 'Yield', 'Stop', 'No vehicles', 'Veh > 3.5t prohibited', 'No entry', 
    'General caution', 'Dangerous curve left', 'Dangerous curve right', 'Double curve', 
    'Bumpy road', 'Slippery road', 'Road narrows on the right', 'Road work', 'Traffic signals', 
    'Pedestrians', 'Children crossing', 'Bicycles crossing', 'Beware of ice/snow', 
    'Wild animals crossing', 'End speed + passing limits', 'Turn right ahead', 'Turn left ahead', 
    'Ahead only', 'Go straight or right', 'Go straight or left', 'Keep right', 'Keep left', 
    'Roundabout mandatory', 'End of no passing', 'End no passing veh > 3.5t'
    ]

    try:
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # 🔥 SPEED BOOST (1 frame sur 2)
            if frame_count % 2 != 0:
                continue

            # 🔥 resize = + rapide + + précis
            frame = cv2.resize(frame, (640, 360))

            results = model(frame, imgsz=416, conf=0.4)

            detections = []

            for r in results:
                for box in r.boxes:

                    cls = int(box.cls[0])
                    label = model.names[cls].strip()
                    conf = float(box.conf[0])

                    # 🔥 filtre confiance
                    if conf < 0.6:
                        continue

                    # 🔥 filtre classes
                    if label not in ALLOWED:
                        continue

                    # 🔥 filtre taille (évite faux positifs)
                    x1, y1, x2, y2 = box.xyxy[0]
                    area = (x2 - x1) * (y2 - y1)

                    if area < 2500:
                        continue

                    # 🔥 validation multi-frame (TRÈS IMPORTANT)
                    if label not in detection_buffer:
                        detection_buffer[label] = 0

                    detection_buffer[label] += 1

                    if detection_buffer[label] < 3:
                        continue

                    # 🔊 speak (cooldown)
                    now = time.time()
                    if label not in last_spoken_time or (now - last_spoken_time[label] > COOLDOWN):
                        speak_label(label)
                        last_spoken_time[label] = now

                    icon, advice = get_advice(label)

                    detections.append({
                        "label": label,
                        "conf": round(conf * 100, 1),
                        "icon_text": icon,
                        "advice": advice,
                        "is_new": True
                    })

            annotated = results[0].plot()
            _, buffer = cv2.imencode('.jpg', annotated)
            frame_b64 = base64.b64encode(buffer).decode()

            await websocket.send_json({
                "type": "frame",
                "frame": frame_b64,
                "detections": detections
            })

            await asyncio.sleep(0.03)

    except WebSocketDisconnect:
        pass
    finally:
        cap.release()
        try:
            os.unlink(path)
        except:
            pass
# ============================
# ▶ RUN
# ============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)