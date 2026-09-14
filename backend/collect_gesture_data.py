import cv2
import mediapipe as mp
import numpy as np
import time
import os
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

GESTURES = {
    "0": "None",
    "1": "Thumb_Up",
    "2": "Index_Point",
    "3": "Open_Palm",
    "4": "Closed_Fist"
}

SAMPLES_PER_GESTURE = 500
CSV_FILE = "gesture_data.csv"

# Initialize CSV
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = ['label'] + [f'v_{i}' for i in range(63)]
        writer.writerow(header)

cap = cv2.VideoCapture(0)

current_gesture = None
recording = False
frames_recorded = 0

print("Controls:")
for k, v in GESTURES.items():
    print(f"Press '{k}' to start recording {v}")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue
        
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            if recording and current_gesture is not None:
                # Extract 63 features
                features = []
                for lm in hand_landmarks.landmark:
                    features.extend([lm.x, lm.y, lm.z])
                    
                with open(CSV_FILE, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([current_gesture] + features)
                
                frames_recorded += 1
                
                if frames_recorded >= SAMPLES_PER_GESTURE:
                    recording = False
                    print(f"\nFinished recording {SAMPLES_PER_GESTURE} frames for {GESTURES[str(current_gesture)]}!")
                    
    # Display UI
    if recording:
        cv2.putText(frame, f"Recording {GESTURES[str(current_gesture)]}: {frames_recorded}/{SAMPLES_PER_GESTURE}", 
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Press 0-4 to Record, Q to Quit", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    cv2.imshow("Gesture Data Collector", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif chr(key) in GESTURES.keys() and not recording:
        current_gesture = int(chr(key))
        recording = True
        frames_recorded = 0
        print(f"\nRecording {GESTURES[str(current_gesture)]} in 3 seconds...")
        cv2.waitKey(3000)

cap.release()
cv2.destroyAllWindows()
