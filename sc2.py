import cv2
import mediapipe as mp
import pyautogui
import math
import time

capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

x1 = y1 = x2 = y2 = 0 

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

stable_start_time = None
last_position = None
double_click_done = False  # çift tıklama yapıldı mı kontrolü

while True:
    _, image = cap.read()
    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1)
    output_hands = capture_hands.process(image)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                if id == 8:  # İşaret parmağı
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1, y1 = x, y

                    current_position = (x, y)
                    if last_position and math.hypot(current_position[0] - last_position[0],
                                                    current_position[1] - last_position[1]) < 10:
                        if stable_start_time is None:
                            stable_start_time = time.time()
                            double_click_done = False
                        else:
                            held_duration = time.time() - stable_start_time
                            if 1 <= held_duration < 2 and not double_click_done:
                                print("1 saniye sabit: Tıklama")
                                pyautogui.click()
                                double_click_done = True
                            elif held_duration >= 2 and not double_click_done:
                                print("2 saniye sabit: Çift Tıklama")
                                pyautogui.doubleClick()
                                double_click_done = True
                    else:
                        stable_start_time = None
                        double_click_done = False

                    last_position = current_position

                if id == 4:  # Baş parmak
                    x2, y2 = x, y

        dist = math.hypot(y2 - y1, x2 - x1)
        print(f"İki parmak arası mesafe: {int(dist)} px")
        cv2.putText(image, f"Mesafe: {int(dist)} px", (10, 70), 
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    cv2.imshow("Hand movement video capture", image)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
