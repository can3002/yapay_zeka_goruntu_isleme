from ursina import *
import cv2
import mediapipe as mp
#El Takip Sistemi
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_utils
mphands = mp.solutions.hands
cap = cv2.VideoCapture(0)
hands = mphands.Hands()
#Ursina Simülasyon Ortamı
app = Ursina()
cube = Entity(model = "cube", scale = 3, color = color.blue)
thumb_tip_x = None
thumb_tip_y = None
index_tip_x = None
index_tip_y = None
left_distance = None
right_distance = None

rotation_speed = 130

#Frame okuma
def update():
    global thumb_tip_x, thumb_tip_y, index_tip_x, index_tip_y
    global left_distance, right_distance, rotation_speed
    ret,frame = cap.read()
    if not ret:
        return
    frame = cv2.cvtColor(cv2.flip(frame,1),cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_index = results.multi_hand_landmarks.index(hand_landmarks)
            hand_label = results.multi_handedness[hand_index].classification[0].label

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,mphands.HAND_CONNECTIONS
            )
            # BAŞ PARMAK
            thumb_tip_x = hand_landmarks.landmark[4].x
            thumb_tip_y = hand_landmarks.landmark[4].y

            # İŞARET PARMAĞI
            index_tip_x = hand_landmarks.landmark[8].x
            index_tip_y = hand_landmarks.landmark[8].y

            if hand_label == "Left":
                dx = hand_landmarks.landmark[8].x - hand_landmarks.landmark[4].x
                dy = hand_landmarks.landmark[8].y - hand_landmarks.landmark[4].y
                left_distance = (dx*dx + dy*dy) ** 0.5
                
                
                rotate_cube_left()

            if hand_label == "Right":
                dx = hand_landmarks.landmark[8].x - hand_landmarks.landmark[4].x
                dy = hand_landmarks.landmark[8].y - hand_landmarks.landmark[4].y
                right_distance = (dx*dx + dy*dy) ** 0.5
                
                rotate_cube_right()


    # mesafeyi hıza map et

    cv2.imshow('Handtracker', frame)
    
def rotate_cube_left():
    if left_distance is None:
        return
    mesafe = 0.05
    
    if left_distance < mesafe:
        cube.rotation_y += rotation_speed * time.dt
    
def rotate_cube_right():
    if right_distance is None:
        return
    mesafe = 0.05
    
    if right_distance < mesafe:
        cube.rotation_y -= rotation_speed * time.dt
    
def input(key):
    if key == 'escape':
        cap.release()
        cv2.destroyAllWindows()
        application.quit()

app.run()