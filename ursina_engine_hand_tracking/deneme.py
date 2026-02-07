import cv2
import mediapipe as mp
from ursina import *
import threading


import mediapipe as mp
# Klasik yöntem yerine doğrudan alt modülü çağırıyoruz
from mediapipe.python.solutions import hands as mp_hands
# --- 1. MEDIA PIPE EL TAKİBİ AYARLARI ---
class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.hand_x, self.hand_y = 0, 0
        self.is_grabbing = False
        self.running = True

    def update(self):
        while self.running:
            success, img = self.cap.read()
            if not success: break
            img = cv2.flip(img, 1) # Görüntüyü ayna gibi çevir
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for hand_lms in results.multi_hand_landmarks:
                    # İşaret parmağı ucu (Landmark 8) ve Baş parmak ucu (Landmark 4)
                    index_finger = hand_lms.landmark[8]
                    thumb = hand_lms.landmark[4]
                    
                    # Koordinatları güncelle
                    self.hand_x = index_finger.x
                    self.hand_y = index_finger.y

                    # Mesafe ölçümü (Eğer parmaklar yakınsa 'tutma' hareketi yap)
                    dist = ((index_finger.x - thumb.x)**2 + (index_finger.y - thumb.y)**2)**0.5
                    self.is_grabbing = dist < 0.05 

            #cv2.imshow("El Takibi Test", img)
            #if cv2.waitKey(1) & 0xFF == ord('q'): break

    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()

# --- 2. URSINA 3D DÜNYASI ---
app = Ursina()

# El takibini arka planda başlat
tracker = HandTracker()
thread = threading.Thread(target=tracker.update, daemon=True)
thread.start()

# 3D Model (Kendi modelini eklemek için: Entity(model='modelim.obj', ...))
target_box = Entity(model='cube', color=color.azure, texture='white_cube', scale=2)
EditorCamera() # Fare ile dünyayı gezmek istersen

def update():
    # Koordinatları Ursina dünyasına göre ölçeklendir
    # MediaPipe 0-1 arası verir, biz bunu ekran koordinatına çekiyoruz
    target_x = (tracker.hand_x - 0.5) * 10
    target_y = (0.5 - tracker.hand_y) * 10

    # Eğer parmaklar birleştiyse (tutma modu) objeyi döndür
    if tracker.is_grabbing:
        #target_box.rotation_y += 2
        target_box.rotation_x += 1
        target_box.color = color.orange
    else:
        target_box.color = color.azure
        # Yumuşak takip (Lerp)
        target_box.x = lerp(target_box.x, target_x, time.dt * 5)
        target_box.y = lerp(target_box.y, target_y, time.dt * 5)

app.run()