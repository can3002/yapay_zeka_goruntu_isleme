import cv2 
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detect = HandDetector(detectionCon=0.8, maxHands=2)
colorR = (255,0,0)

cx,cy, w ,h = 100,100,200,200




class DragRect():
    def __init__(self,posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def update(self,x,y):
        cx,cy = self.posCenter
        w,h = self.size

        if cx-w//2 < x <  cx+w//2 and cy-h//2 < y < cy+h//2:
                   colorR = (0, 255, 0)  # Yeşil
                   self.posCenter  = x,y

rect = DragRect([150,150])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hands,frame = detect.findHands(frame)

    colorR = (255, 0, 0)  # Varsayılan renk: kırmızı

    if hands:
        if len(hands) > 0:

            

            hand = hands[0]
            lmList = hand["lmList"]
            point = lmList[8]  # İşaret parmağı ucu
            point1 = lmList[12]
            x, y = point[0], point[1]
            l, _, frame = detect.findDistance(point[:2], point1[:2],frame)  # sadece (x, y)
            print(l)
            if l<50:
                 #call the update here
                rect.update(x,y)

           
            
    cx,cy = rect.posCenter
    w,h = rect.size
    
    cv2.rectangle(frame, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)

    cv2.imshow("Drag and Release", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
