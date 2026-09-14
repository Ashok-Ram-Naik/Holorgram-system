# 🌌 Intelligent Virtual Holographic Interaction System 

[![AI](https://img.shields.io/badge/AI-Custom%20Trained-blue.svg)]()
[![3D](https://img.shields.io/badge/3D-Three.js-black.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

An advanced, touchless interface for 3D holographic projection powered by **custom-trained machine learning models**. This system enables real-time interaction with 3D holograms using **hand gestures and voice commands trained from real-world datasets**, delivering a futuristic, Iron Man-style experience.

---

## 🧠 Core Innovation

Unlike systems that depend on pre-trained models, this project is built using:

- Custom-collected real-world gesture datasets  
- Self-trained machine learning models  
- Voice command models trained on real user speech samples  
- Optimized real-time inference pipeline  

---

## 🧠 Advanced Algorithms & Technology

### 1. Computer Vision (Custom Hand Gesture Recognition)

The gesture system is built entirely from scratch using real-world data:

- **Dataset Collection**
  - Captured multiple gestures (pinch, swipe, thumbs up, point)
  - Includes variations in lighting, backgrounds, and users  

- **Preprocessing**
  - Hand segmentation using OpenCV  
  - Frame normalization and noise reduction  

- **Feature Engineering**
  - Extraction of finger joint relationships  
  - Distance and angle-based feature calculation  

- **Model Training**
  - Custom CNN + keypoint-based classifier  
  - Trained on labeled gesture dataset  

- **Gesture Detection**
  - Real-time classification  
  - Temporal smoothing for stability  
  - Threshold-based filtering  

---

### 2. Natural Language Processing (Custom Voice Recognition)

Voice interaction is powered by a model trained on real speech data:

- **Dataset Collection**
  - Multiple users recording commands (Next, Rotate, Stop, etc.)  
  - Includes noise and accent variations  

- **Feature Extraction**
  - MFCC (Mel Frequency Cepstral Coefficients)  

- **Model Training**
  - RNN / LSTM-based classifier  
  - Maps voice patterns to system actions  

- **Execution Pipeline**
  - Audio → Feature Extraction → Classification → Action  

---

### 3. 3D Graphics & Animation

- Built using Three.js  
- Smooth animations using Linear Interpolation (Lerp)  
- Quaternion-based rotations (no gimbal lock)  
- Real-time scene updates  

---

### 4. Holographic Display System

- Based on Pepper’s Ghost Principle  
- Custom 4-view rendering system:
  - Screen split into four perspectives  
  - Rotated and mirrored for pyramid projection  
  - Enables 360° holographic illusion  

---

## ✨ Key Features

-  Custom-trained gesture recognition system  
-  Voice commands trained on real datasets  
-  360° holographic projection  
-  10+ interactive 3D objects  
-  Low-latency real-time processing  
-  High accuracy classification  
-  Clean glassmorphism UI  

---

## 🛠️ Tech Stack

### AI/ML
- Custom CNN (Gesture Recognition)
- LSTM / RNN (Voice Recognition)
- OpenCV (Preprocessing)

### Frontend
- Three.js
- Web APIs (Camera + Microphone)
- HTML, CSS

### Backend
- Python (Flask)

### Hardware
- Webcam  
- Microphone  
- Hologram pyramid display  

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Webcam
- Microphone
- Modern browser (Chrome/Edge recommended)

---

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NaikNithin2005/Hologram-System.git
   cd Hologram-System
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python server.py
   ```

3. **Run Frontend**:
   - Double-click `start_hologram.bat` in the root folder to start the local web server instantly, or manually run:
     ```bash
     cd frontend
     python -m http.server 8080
     ```
   - Open your browser to `http://localhost:8080/`.
   - Allow camera and microphone access.

---

## 🎮 How to Use

### 🖐️ Hand Gestures

| Gesture | Action |
| :--- | :--- |
| **Pinch** | Zoom In/Out |
| **Swipe** | Rotate Object |
| **Thumb Up** | Next 3D Object |
| **Point** | Previous 3D Object |

### 🎙️ Voice Commands

- **"Next"** / **"Previous"**: Switch between 3D models.
- **"Rotate"** / **"Stop"**: Toggle automatic rotation.
- **"Hologram Mode"**: Toggle between full-screen and 4-way split view.

---

## 📊 Dataset Details

### Hand Gesture Dataset
- **1000+ samples per gesture**
- Recorded across multiple users for diversity
- Includes various lighting conditions and skin tones

### Voice Dataset
- **Multi-speaker recordings**
- Data augmented with background noise for robustness
- Includes accent variations for better generalization

---

## 🗺️ Future Enhancements
- [ ] Dual-hand interaction
- [ ] AR integration (WebXR)
- [ ] Custom 3D model upload
- [ ] Adaptive AI gesture learning
- [ ] Audio/haptic feedback

---

## 📄 License
This project is licensed under the MIT License.

## 🤝 Acknowledgments
- Built using custom datasets and self-trained machine learning models.
- Inspired by futuristic, real-world AI interaction systems.
