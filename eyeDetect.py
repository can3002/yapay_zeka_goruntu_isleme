import cv2
import dlib
from math import hypot
import serial
import time

# Kamera ve Arduino bağlantısı
cap = cv2.VideoCapture(0)
arduino = serial.Serial('COM3', 9600)  # Arduino bağlı COM portu
time.sleep(2)  # bağlantının oturması için bekle

# Dlib yüz ve landmark algılayıcı
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_SIMPLEX

# Göz noktalarının orta noktasını hesaplayan fonksiyon
def midpoint(p1, p2):
    return (int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2))

# Göz kapalı/açık oranını hesaplayan fonksiyon
def blink_ratio(eye_points, facial_landmarks):
    left_p = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_p = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_p = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    verlenght = hypot((center_p[0] - center_bottom[0]), (center_p[1] - center_bottom[1]))
    horlenght = hypot((left_p[0] - right_p[0]), (left_p[1] - right_p[1]))

    if verlenght == 0:  # sıfıra bölme hatası önlemi
        return 100

    ratio = horlenght / verlenght
    return ratio

print("Göz kontrollü motor sistemi başlatıldı. 'q' tuşuna basarak çıkabilirsiniz.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera açılmadı!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if faces:  # Parmak kontrol kodundaki 'if hands:' mantığı gibi
        face = faces[0]  # İlk yüzü al
        landmarks = predictor(gray, face)

        # Sol ve sağ göz oranlarını hesapla
        left_eye_ratio = blink_ratio([36,37,38,39,40,41], landmarks)
        right_eye_ratio = blink_ratio([42,43,44,45,46,47], landmarks)
        blink = (left_eye_ratio + right_eye_ratio) / 2

        # Göz kapalı mı?
        if blink > 4.7:
            cv2.putText(frame, "MOTOR STOP", (50, 150), font, 1, (0, 0, 255), 2)
            data = '0'  # Arduino'ya gönderilecek veri
        else:
            cv2.putText(frame, "MOTOR RUN", (50, 150), font, 1, (0, 255, 0), 2)
            data = '1'  # Arduino'ya gönderilecek veri

        arduino.write(f"{data}\n".encode("utf-8"))  # Parmak kodundaki string format mantığı

    else:
        # Yüz algılanmadı
        cv2.putText(frame, "YUZ ALGILANMADI", (50, 150), font, 1, (0, 0, 255), 2)
        arduino.write(b'0\n')  # Güvenlik için motor dur

    cv2.imshow("Kamera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizlik
cap.release()
arduino.close()
cv2.destroyAllWindows()
print("Program sonlandırıldı.")
