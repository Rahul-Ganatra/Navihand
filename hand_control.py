import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import os
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)

# For smoothing
smooth_x, smooth_y = 0, 0
alpha = 0.2  # Smoothing factor

drag_mode = False
lock_cooldown = 0  # To prevent repeated locking

def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    pip_joints = [3, 6, 10, 14, 18]
    fingers = []
    # Thumb: compare x for right hand, y for left hand
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for tip, pip in zip(tips[1:], pip_joints[1:]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

with mp_hands.Hands(
    max_num_hands=2,  # Allow detection of two hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Could not read frame from camera. Retrying...")
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # --- Lock screen if both hands are detected ---
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            # Use the index finger tip of the first hand for message position
            x_tip = int(results.multi_hand_landmarks[0].landmark[8].x * w)
            y_tip = int(results.multi_hand_landmarks[0].landmark[8].y * h)
            if time.time() - lock_cooldown > 5:
                cv2.putText(frame, "Locking Screen...", (x_tip, y_tip-120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow("Hand Mouse", frame)
                cv2.waitKey(500)
                os.system("rundll32.exe user32.dll,LockWorkStation")
                lock_cooldown = time.time()

        # --- Use first hand for movement and gestures ---
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            fingers = fingers_up(hand_landmarks)
            x_tip = int(hand_landmarks.landmark[8].x * w)
            y_tip = int(hand_landmarks.landmark[8].y * h)
            smooth_x = int(alpha * (hand_landmarks.landmark[8].x * screen_width) + (1 - alpha) * smooth_x)
            smooth_y = int(alpha * (hand_landmarks.landmark[8].y * screen_height) + (1 - alpha) * smooth_y)
            pyautogui.moveTo(smooth_x, smooth_y)

            # Left Click: Peace sign (index and middle up, others down)
            if fingers == [0, 1, 1, 0, 0]:
                pyautogui.click()
                cv2.putText(frame, "Left Click!", (x_tip, y_tip-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Right Click: "3" sign (index, middle, ring up, others down)
            if fingers == [0, 1, 1, 1, 0]:
                pyautogui.rightClick()
                cv2.putText(frame, "Right Click!", (x_tip, y_tip-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # Grab/Drag: Fist (all fingers down)
            if fingers == [0, 0, 0, 0, 0]:
                if not drag_mode:
                    pyautogui.mouseDown()
                    drag_mode = True
                    cv2.putText(frame, "Grab Start", (x_tip, y_tip-90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            elif drag_mode:
                pyautogui.mouseUp()
                drag_mode = False
                cv2.putText(frame, "Grab End", (x_tip, y_tip-90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Mouse", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
