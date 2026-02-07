import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import numpy as np
import time
import os
import threading

# Windows ekran klavyesini başlat
def open_osk():
    os.system('osk')

threading.Thread(target=open_osk, daemon=True).start()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

detector = HandDetector(detectionCon=0.8, maxHands=2)

screen_w, screen_h = pyautogui.size()
click_state = {}
drag_state = {}

click_timeout = 0.5  # çift tıklama için max süre
drag_threshold = 40  # parmak mesafesi eşiği

# Ekran klavyesi ekranın alt kısmında olacağı varsayımı
keyboard_top = screen_h - 300  # tahmini değer
keyboard_bottom = screen_h

def check_click_and_drag(hand_id, length, current_time, cursor_x, cursor_y):
    global click_state, drag_state

    if hand_id not in click_state:
        click_state[hand_id] = {'prev_time': 0, 'click_count': 0}
    if hand_id not in drag_state:
        drag_state[hand_id] = False

    state = click_state[hand_id]
    dragging = drag_state[hand_id]

    if length < drag_threshold:
        if not dragging:
            pyautogui.mouseDown()
            drag_state[hand_id] = True
            print(f"Hand {hand_id}: Drag start")
        else:
            pyautogui.moveTo(cursor_x, cursor_y)

        if length < 20:
            if current_time - state['prev_time'] < click_timeout:
                pyautogui.doubleClick()
                print(f"Hand {hand_id}: Double Click")
                state['click_count'] = 0
                state['prev_time'] = 0
            else:
                state['click_count'] = 1
                state['prev_time'] = current_time

        elif length < 40:
            if current_time - state['prev_time'] > click_timeout:
                pyautogui.click()
                print(f"Hand {hand_id}: Single Click")

                # Ekran klavyesinde tıklanıyorsa
                if keyboard_top < cursor_y < keyboard_bottom:
                    pyautogui.click()
                    print("Clicked on On-Screen Keyboard")

                state['prev_time'] = current_time
                state['click_count'] = 0

    else:
        if dragging:
            pyautogui.mouseUp()
            drag_state[hand_id] = False
            print(f"Hand {hand_id}: Drag end")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        current_time = time.time()

        for i, hand in enumerate(hands):
            lmList = hand["lmList"]
            if len(lmList) >= 9:
                x, y = lmList[8][:2]
                fx = np.interp(x, [0, 640], [0, screen_w])
                fy = np.interp(y, [0, 480], [0, screen_h])
                pyautogui.moveTo(fx, fy)

                length, _, _ = detector.findDistance(lmList[8][:2], lmList[4][:2], img)
                check_click_and_drag(i, length, current_time, fx, fy)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
