import cv2
import mediapipe as mp
import numpy as np
import time
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# --- Calculator UI and Logic (Simplified for example) ---
button_positions = {
    "7": (50, 150), "8": (150, 150), "9": (250, 150), "/": (350, 150),
    "4": (50, 250), "5": (150, 250), "6": (250, 250), "*": (350, 250),
    "1": (50, 350), "2": (150, 350), "3": (250, 350), "-": (350, 350),
    "0": (50, 450), "C": (150, 450), "=": (250, 450), "+": (350, 450),
}
button_size = 80
calc_display = ""
last_click_time = 0
click_debounce_time = 0.5 # seconds

def draw_calculator(img, hand_x, hand_y):
    global calc_display

    # Display area
    cv2.rectangle(img, (50, 50), (430, 120), (200, 200, 200), -1)
    cv2.rectangle(img, (50, 50), (430, 120), (50, 50, 50), 2)
    cv2.putText(img, calc_display, (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    for text, (x, y) in button_positions.items():
        x1, y1 = x, y
        x2, y2 = x + button_size, y + button_size
        
        color = (255, 0, 0) # Default button color
        if x1 < hand_x < x2 and y1 < hand_y < y2:
            color = (0, 255, 0) # Hover color

        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
        cv2.putText(img, text, (x1 + 25, y1 + 55), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img

def distance(point1, point2):
    return math.hypot(point2[0] - point1[0], point2[1] - point1[1])

def is_pinch(hand_landmarks, img_width, img_height, threshold=40):
    # Calculate distance between thumb tip and index finger tip
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_coords = (int(thumb_tip.x * img_width), int(thumb_tip.y * img_height))
    index_coords = (int(index_tip.x * img_width), int(index_tip.y * img_height))
    dist = distance(thumb_coords, index_coords)
    return dist < threshold, index_coords

def handle_button_press(hand_x, hand_y, current_time):
    global calc_display, last_click_time

    if current_time - last_click_time < click_debounce_time:
        return # Debounce

    for text, (x, y) in button_positions.items():
        x1, y1 = x, y
        x2, y2 = x + button_size, y + button_size

        if x1 < hand_x < x2 and y1 < hand_y < y2:
            last_click_time = current_time
            if text == "C":
                calc_display = ""
            elif text == "=":
                try:
                    # Use eval with caution; here input is controlled by button presses only
                    calc_display = str(eval(calc_display))
                except Exception:
                    calc_display = "Error"
            else:
                calc_display += text
            break # Only process one click

# --- Main Video Loop ---
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1) # Mirror the frame
        
        # Convert the BGR image to RGB.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the image and find hands.
        results = hands.process(rgb_frame)

        hand_x, hand_y = -1, -1 # Default: hand not found or not pointing
        pinch_detected = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                h, w, c = frame.shape
                pinch_detected, (hand_x, hand_y) = is_pinch(hand_landmarks, w, h)

                # Draw a circle at the index finger tip for visual feedback
                cv2.circle(frame, (hand_x, hand_y), 10, (255, 255, 0), -1)

                if pinch_detected:
                    handle_button_press(hand_x, hand_y, time.time())
                     
        # Draw calculator UI
        frame = draw_calculator(frame, hand_x, hand_y)

        cv2.imshow('Virtual Calculator', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Exiting program...")

cap.release()
hands.close()
cv2.destroyAllWindows()
