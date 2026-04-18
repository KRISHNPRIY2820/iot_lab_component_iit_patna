# 🌍 TinyML Environmental Monitoring System

## 📌 Overview

This project implements a real-time environmental monitoring system using TinyML on Arduino Nano BLE Sense.

It processes environmental parameters:

* Temperature
* Humidity
* Pressure
* Gas

and performs intelligent prediction using an optimized machine learning model deployed via Edge Impulse.

---

## ⚙️ Features

* Real-time data streaming from cloud server
* TinyML inference on Arduino Nano BLE Sense
* Optimized INT8 TFLite Micro model
* Edge Impulse deployment pipeline
* Serial communication for live prediction

---

## 🧠 System Pipeline

```
Azure Server → Python Script → Data Processing → ML Model → Edge Impulse → Arduino → Prediction Output
```

---

## 📦 Installation

### 1. Install Python Dependencies

```bash
pip install numpy pandas matplotlib scikit-learn tensorflow requests pyserial
```

---

### 2. Install Arduino IDE

Download from: https://www.arduino.cc/en/software

---

### 3. Install Board (Arduino Nano BLE Sense)

* Open Arduino IDE
* Go to: Tools → Board → Boards Manager
* Search: **Arduino Nano 33 BLE**
* Click Install

---

### 4. Add Edge Impulse Library

* Download deployment ZIP from Edge Impulse
* Open Arduino IDE
* Go to: Sketch → Include Library → Add .ZIP Library
* Select the downloaded ZIP

---

## 🚀 How to Run

### Step 1: Train Model

Run your training script:

```bash
python Software_1.ipynb
```

---

### Step 2: Upload Model to Arduino

* Open `.ino` file in Arduino IDE
* Select correct COM port
* Upload the code

---

### Step 3: Start Data Streaming

```bash
python transfer.py
```

---

### Step 4: View Predictions

Open Serial Monitor (115200 baud):

```
Prediction → polluted
Prediction → comfortable
```

---

## 📊 Data Source

```
https://azure.abhi.dedyn.io/iot/
```

---

## 🧪 Model Details

* Input features: 4
* Model type: Dense Neural Network
* Quantization: INT8 (TFLite Micro)
* Deployment: Edge Impulse

---

## ⚠️ Important Notes

* Ensure correct COM port is selected
* Data format must be:

```
temperature,humidity,pressure,gas
```

* Model expects **scaled inputs (handled internally or before deployment)**




---

## 🔗 GitHub Repository


```
(https://github.com/KRISHNPRIY2820/iot_lab_component_iit_patna)
```

---

## 📈 Future Improvements

* Improve class balance in dataset
* Add temporal (time-series) modeling
* Integrate anomaly detection
* Deploy dashboard for visualization

---

## 👨‍💻 Author

GROUP 5
