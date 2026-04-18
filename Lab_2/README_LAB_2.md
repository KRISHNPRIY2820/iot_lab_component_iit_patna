# 🌱 Soil Data Collection using RS485 Sensor and Raspberry Pi

## 🚀 Overview

This project focuses on **real-time soil data collection** using an RS485-based soil sensor connected to a Raspberry Pi.
The system reads multiple soil parameters, stores them locally in CSV format, and uploads them to the cloud (ThingSpeak) for remote monitoring.

---

## 🧩 System Components

* Raspberry Pi 4
* Soil Sensor (RS485-based, e.g., ZTS-3002)
* USB to RS485 Converter
* Jumper Wires
* ThingSpeak Cloud Platform

---

## 🔌 Hardware Connections

### Sensor → RS485 Converter

| Sensor Pin | RS485 Converter |
| ---------- | --------------- |
| A          | A               |
| B          | B               |
| GND        | GND             |

### RS485 Converter → Raspberry Pi

* Connect via USB port

---

## ⚙️ Installation

### 1. Update System

```bash
sudo apt update
```

### 2. Install Required Libraries

```bash
pip3 install pyserial requests
```

---

## 📡 Working Principle

1. Raspberry Pi sends a Modbus query to the soil sensor
2. Sensor responds with raw data
3. Data is parsed into meaningful values
4. Data is:

   * Stored locally in CSV files
   * Sent to ThingSpeak cloud

---

## 📊 Parameters Measured

* Soil Moisture (%)
* Temperature (°C)
* Electrical Conductivity
* pH Level
* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)

---

## 💾 Data Storage

### Local Storage

* Data is saved in CSV format inside the `data/` folder
* Each file contains up to 2000 entries
* New file is created automatically after limit

Example:

```
data/soil_001.csv
data/soil_002.csv
```

---

## ☁️ Cloud Upload (ThingSpeak)

Data is uploaded to ThingSpeak using API.

### Fields Mapping

| Field  | Parameter    |
| ------ | ------------ |
| Field1 | Moisture     |
| Field2 | Temperature  |
| Field3 | Conductivity |
| Field4 | pH           |
| Field5 | Nitrogen     |
| Field6 | Phosphorus   |
| Field7 | Potassium    |

---

## ▶️ How to Run

```bash
python sensor.py
```

---

## 📈 Data Flow

```
Soil Sensor → RS485 → Raspberry Pi → CSV + ThingSpeak
```

---

## ⚠️ Notes

* Ensure correct USB port detection (`/dev/ttyUSB0` or similar)
* Check wiring if "No sensor response" appears
* Maintain minimum 15-second interval for ThingSpeak

---

## 🔗 GitHub Repository
https://github.com/KRISHNPRIY2820/iot_lab_component_iit_patna

---

## 📌 Scope of Work

This project covers:

* Hardware interfacing
* Data acquisition
* Data logging
* Cloud integration

*(Machine Learning and inference are handled separately.)*

---

## 🧑‍💻 Author

Group 5

---
