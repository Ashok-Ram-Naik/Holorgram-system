import cv2
import mediapipe as mp
import math

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky

    def detect_gesture(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        gesture = "None"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                
                if len(lm_list) != 0:
                    fingers = []
                    
                    # Thumb (check if thumb is to the right/left of the second joint, simplistic approach)
                    # For simplicity, we check y-axis for thumb as well, but x-axis is better
                    if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    
                    # 4 Fingers
                    for id in range(1, 5):
                        if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                            
                    total_fingers = fingers.count(1)
                    
                    if total_fingers == 5 or total_fingers == 4:
                        gesture = "OPEN_PALM" # Rotate
                    elif total_fingers == 0:
                        gesture = "CLOSED_FIST" # Stop/Select
                    elif total_fingers == 2 and fingers[1] == 1 and fingers[2] == 1:
                        gesture = "TWO_FINGERS" # Zoom
                    elif total_fingers == 1 and fingers[1] == 1:
                        gesture = "SWIPE" # Change object
                        
        return gesture, results.multi_hand_landmarks

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = GestureDetector()
    while True:
        success, img = cap.read()
        if not success:
            break
            
        gesture, landmarks = detector.detect_gesture(img)
        cv2.putText(img, f'Gesture: {gesture}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Gesture Recognition", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
