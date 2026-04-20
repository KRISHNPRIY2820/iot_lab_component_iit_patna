import cv2
import pytesseract
import numpy as np
import re
import time
from collections import Counter

# ---------------- CONFIG ----------------
STREAM_URL = "tcp://127.0.0.1:8888"
SAVE_FILE = "plates5.txt"

OCR_INTERVAL = 2.0  # seconds

# Connect to stream
cap = cv2.VideoCapture(STREAM_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ Stream not opened")
    exit()

# ---------------- FUNCTIONS ----------------
def clean_text(text):
    return re.sub(r'[^A-Z0-9]', '', text.upper())

def valid_plate(text):
    return len(text) >= 5 and any(c.isdigit() for c in text)

# 🔥 NEW: multi-frame stable OCR
plate_history = []

def stable_plate(text):
    if len(text) < 5:
        return None

    plate_history.append(text)

    if len(plate_history) > 5:
        plate_history.pop(0)

    return Counter(plate_history).most_common(1)[0][0]

# 🔥 NEW: smart OCR for 1-line + 2-line plates
def smart_ocr(thresh):
    config1 = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    config2 = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    text1 = pytesseract.image_to_string(thresh, config=config1)
    text2 = pytesseract.image_to_string(thresh, config=config2)

    text1 = clean_text(text1)
    text2 = clean_text(text2)

    # Choose better result
    if len(text2) > len(text1):
        return text2
    return text1

last_ocr_time = 0

print("🚀 REAL-TIME ANPR (FINAL + 2-LINE SUPPORT)... Press 'q' to exit")

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()

    if not ret:
        continue

    # Drop buffered frames (low latency)
    for _ in range(2):
        cap.grab()

    # Resize for speed
    small = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detected_boxes = []

    for cnt in contours:
        if cv2.contourArea(cnt) < 1500:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)

        if 2 < aspect_ratio < 6:
            detected_boxes.append((x, y, w, h))

    # -------- DRAW BOXES --------
    for (x, y, w, h) in detected_boxes:

        scale_x = frame.shape[1] / 320
        scale_y = frame.shape[0] / 240

        x1 = int(x * scale_x)
        y1 = int(y * scale_y)
        w1 = int(w * scale_x)
        h1 = int(h * scale_y)

        cv2.rectangle(frame, (x1,y1), (x1+w1,y1+h1), (0,255,0), 2)

    # -------- OCR --------
    current_time = time.time()

    if detected_boxes and (current_time - last_ocr_time > OCR_INTERVAL):

        last_ocr_time = current_time

        x, y, w, h = detected_boxes[0]

        scale_x = frame.shape[1] / 320
        scale_y = frame.shape[0] / 240

        x1 = int(x * scale_x)
        y1 = int(y * scale_y)
        w1 = int(w * scale_x)
        h1 = int(h * scale_y)

        plate = frame[y1:y1+h1, x1:x1+w1]

        if plate.size != 0:

            # -------- IMPROVED PREPROCESSING --------
            plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
            plate_gray = cv2.resize(plate_gray, None, fx=2, fy=2)

            plate_gray = cv2.bilateralFilter(plate_gray, 11, 17, 17)

            _, thresh = cv2.threshold(
                plate_gray, 0, 255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            kernel = np.ones((3,3), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

            # 🔥 NEW OCR (supports 2-line)
            text = smart_ocr(thresh)

            # 🔥 STABILIZE OUTPUT
            stable_text = stable_plate(text)

            if stable_text and valid_plate(stable_text):
                print("PLATE:", stable_text)

                with open(SAVE_FILE, "a") as f:
                    f.write(stable_text + "\n")

                cv2.putText(frame, stable_text, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    # -------- DISPLAY --------
    cv2.imshow("REAL-TIME ANPR (FINAL)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

