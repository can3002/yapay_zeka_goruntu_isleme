import cv2
import mediapipe as mp
import pyautogui
x1 = y1 = x2 = y2 = 0
cap = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawu=mp.solutions.drawing_utils
while True:
    ret,imag = cap.read()
    imag = cv2.flip(imag,1)
    frame_height,frame_width,_ = imag.shape
    if not ret:
        break
    
    rgb = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)

    output = my_hands.process(rgb)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawu.draw_landmarks(imag,hand)
            landmarks = hand.landmark
            for id,landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=imag,center=(x,y),radius=8,color=(0,255,255),thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=imag,center=(x,y),radius=8,color=(0,255,255),thickness=3)
                    x2 = x
                    y2 = y
        dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4
        cv2.line(imag,(x1,y1),(x2,y2),(0,255,0),5)
        if dist > 30:
             pyautogui.press("volumeup")
        else:
             pyautogui.press("volumedown")

    cv2.imshow("hand volume control",imag)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
