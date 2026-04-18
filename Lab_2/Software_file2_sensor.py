import serial
import time
import csv
import os
import requests
from datetime import datetime
import RPi.GPIO as GPIO

# ================= CONFIG =================
SERIAL_PORT = "/dev/ttyAMA0"
BAUDRATE = 4800
DE_RE_PIN = 18
READ_INTERVAL = 15
THINGSPEAK_WRITE_KEY = "FMGUCC517WMLJF4R"
DATA_DIR = "data"
ROWS_PER_FILE = 2000

SERVER_URL = "http://azure.abhi.dedyn.io/iot/api/"
# ==========================================

# ---------- GPIO ----------
GPIO.setmode(GPIO.BCM)
GPIO.setup(DE_RE_PIN, GPIO.OUT)
GPIO.output(DE_RE_PIN, GPIO.LOW)

# ---------- SERIAL ----------
ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUDRATE,
    bytesize=8,
    parity=serial.PARITY_NONE,
    stopbits=1,
    timeout=1
)

print("✅ RS485 serial port opened")

QUERY = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x07, 0x04, 0x08])

# ---------- FILE HELPERS ----------
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_next_csv():
    files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".csv"))
    if not files:
        return os.path.join(DATA_DIR, "soil_001.csv")
    num = int(files[-1].split("_")[1].split(".")[0])
    return os.path.join(DATA_DIR, f"soil_{num+1:03d}.csv")

# ---------- SENSOR ----------
def read_sensor():
    GPIO.output(DE_RE_PIN, GPIO.HIGH)
    time.sleep(0.01)

    ser.write(QUERY)
    ser.flush()

    GPIO.output(DE_RE_PIN, GPIO.LOW)
    time.sleep(0.2)

    r = ser.read(19)
    if len(r) != 19:
        return None

    return {
        "time": datetime.now().isoformat(),
        "moisture": ((r[3] << 8) | r[4]) / 10,
        "temperature": ((r[5] << 8) | r[6]) / 10,
        "conductivity": (r[7] << 8) | r[8],
        "ph": ((r[9] << 8) | r[10]) / 10,
        "nitrogen": (r[11] << 8) | r[12],
        "phosphorus": (r[13] << 8) | r[14],
        "potassium": (r[15] << 8) | r[16],
    }

# ---------- SERVER ----------
def send_to_thingspeak(data):
    url = "https://api.thingspeak.com/update"
    payload = {
        "api_key": THINGSPEAK_WRITE_KEY,
        "field1": data["moisture"],
        "field2": data["temperature"],
        "field3": data["conductivity"],
        "field4": data["ph"],
        "field5": data["nitrogen"],
        "field6": data["phosphorus"],
        "field7": data["potassium"],
    }

    try:
        r = requests.post(url, data=payload, timeout=5)
        if r.text != "0":
            print("🌐 ThingSpeak OK → Entry ID:", r.text)
        else:
            print("⚠️ ThingSpeak rejected update (rate limit?)")
    except Exception as e:
        print("⚠️ ThingSpeak error:", e)



# ---------- MAIN ----------
ensure_data_dir()
csv_file = get_next_csv()
rows_written = 0

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "time", "moisture", "temperature",
        "conductivity", "ph",
        "nitrogen", "phosphorus", "potassium"
    ])

print("📈 Logging started")

try:
    while True:
        data = read_sensor()
        if data:
            # ---- LOCAL CSV SAVE (SAFE) ----
            with open(csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(data.values())

            rows_written += 1
            print("✅ Logged:", data)

            # ---- SERVER UPLOAD (CSV BODY) ----
            send_to_thingspeak(data)


            # ---- ROTATE FILE ----
            if rows_written >= ROWS_PER_FILE:
                csv_file = get_next_csv()
                rows_written = 0
                with open(csv_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "time", "moisture", "temperature",
                        "conductivity", "ph",
                        "nitrogen", "phosphorus", "potassium"
                    ])
        else:
            print("❌ No sensor response")

        time.sleep(READ_INTERVAL)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    GPIO.cleanup()
    ser.close()
