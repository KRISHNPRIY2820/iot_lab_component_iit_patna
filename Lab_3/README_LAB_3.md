# 🧠 Smart Indoor Movement Detection System

## 🚀 Overview

This project implements a **real-time indoor movement detection system** using multi-sensor fusion and deep learning.

The system collects data from **ESP32 devices equipped with Ultrasonic and PIR sensors**, estimates the position of a person, and then predicts movement patterns using an LSTM-based model.

---

## 📍 System Architecture

```
ESP32 Sensors (Ultrasonic + PIR)
            ↓
     Feature Engineering
            ↓
   Position Model (XGBoost)
            ↓
        (x, y Coordinates)
            ↓
   Sequence Buffer (20 timesteps)
            ↓
        LSTM Model
            ↓
   Movement Prediction
```

---

## ⚙️ Hardware Setup

* 4 × ESP32 boards
* 4 × Ultrasonic sensors
* 4 × PIR sensors

### 📌 Sensor Placement (Room Corners)

```
C0 (0,0) ---- C1 (5,0)
   |              |
   |              |
C3 (0,5) ---- C2 (5,5)
```

---

## 🧠 Models Used

### 🔹 1. Position Model

* Algorithm: **XGBoost Regressor**
* Input: Sensor readings
* Output: **(x, y) coordinates**

---

### 🔹 2. Movement Model

* Algorithm: **LSTM (Long Short-Term Memory)**
* Input: Sequence of (x, y) positions (last 20 timesteps)
* Output: Movement class

  * horizontal
  * vertical
  * stationary

---

## 📊 Performance

| Metric             | Value  |
| ------------------ | ------ |
| 📍 Position Error  | ~0.024 |
| 🔥 Motion Accuracy | ~99%   |
| Precision          | ~0.99  |
| Recall             | ~0.99  |
| F1-score           | ~0.99  |

---


---

## ▶️ How to Run

### 🔹 Step 1: Train Models (Google Colab)

1. Upload dataset
2. Run all cells
3. Save models:

   * `pos_model.pkl`
   * `lstm_model.h5`
   * `lstm_labels.pkl`

---

## 🔄 Real-Time Workflow

1. ESP32 sends sensor data via Serial
2. Python script forwards data to Flask API
3. Position model predicts (x, y)
4. LSTM processes sequence of positions
5. Movement is predicted in real time

---

## 🔥 Key Features

* ✅ Multi-sensor fusion
* ✅ Real-time movement detection
* ✅ High accuracy (~99%)
* ✅ Temporal modeling using LSTM
* ✅ Noise smoothing with buffer
* ✅ Scalable architecture

---

## 📈 Why This Approach Works

Instead of directly predicting movement:

```
Sensors → Movement ❌
```

We use a smarter pipeline:

```
Sensors → Position → Sequence → Movement ✅
```

This improves:

* Accuracy
* Stability
* Real-world performance

---

## 🧪 Example Output

```
📍 Position: (2.03, 2.79)
🚶 Movement: stationary
Confidence: 0.98
```

---

## 📌 Future Improvements

* 🔥 Multi-person tracking
* 🔥 2D/3D visualization dashboard
* 🔥 Cloud deployment (AWS / Render)
* 🔥 ESP32 direct WiFi streaming
* 🔥 TinyML deployment

---

## 🔗 GitHub Repository


`https://github.com/KRISHNPRIY2820/iot_lab_component_iit_patna`

---

## 👩‍💻 Author

GROUP 5

---

## 📄 License

This project is for academic and research purposes.
