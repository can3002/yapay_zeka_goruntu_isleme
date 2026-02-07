import cv2
from cvzone.HandTrackingModule import HandDetector
import pygetwindow as gw
import pyautogui
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detect = HandDetector(detectionCon=0.8, maxHands=1)

# Ekran çözünürlüğü
screen_w, screen_h = pyautogui.size()

# Elde edilen pencerenin bilgisi
selected_window = None
last_move_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hands, frame = detect.findHands(frame)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        if len(lmList) >= 12:
            point = lmList[8]    # İşaret parmağı ucu
            point1 = lmList[12]  # Orta parmak ucu

            # Mesafe ölçümü
            distance, _, _ = detect.findDistance(point[:2], point1[:2])

            # Parmağın ekran koordinatına dönüşümü (kamera 1280x720'den gerçek ekran çözünürlüğüne)
            x_screen = int(screen_w * point[0] / 1280)
            y_screen = int(screen_h * point[1] / 720)

            # Sadece yakınlaştırıldığında (parmaklar kapalı) pencere taşı
            if distance < 40:
                # Her 0.5 saniyede bir pencere hareket ettir
                if time.time() - last_move_time > 0.5:
                    # İlk seferde pencereyi bul
                    if selected_window is None:
                        for win in gw.getWindowsWithTitle(''):
                            if win.visible:
                                if abs(win.left - x_screen) < 100 and abs(win.top - y_screen) < 100:
                                    selected_window = win
                                    break
                    
                    # Seçilen pencereyi hareket ettir
                    if selected_window:
                        try:
                            selected_window.moveTo(x_screen, y_screen)
                        except:
                            selected_window = None

                    last_move_time = time.time()
            else:
                selected_window = None  # parmaklar açıkken pencere bırak

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
