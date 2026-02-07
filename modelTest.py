import cv2
import numpy as np
import tensorflow as tf

# 1. Modeli yükle
model = tf.keras.models.load_model("my_model.keras")

# 2. Sınıf isimleri
class_names = np.array([
    "Speed limit 20 km/h", "Speed limit 30 km/h", "Speed limit 50 km/h",
    "Speed limit 60 km/h", "Speed limit 70 km/h", "Speed limit 80 km/h",
    "End of speed limit 80 km/h", "Speed limit 100 km/h", "Speed limit 120 km/h",
    "No passing", "No passing for vehicles over 3.5 metric tons",
    "Right-of-way at the next intersection", "Priority road",
    "Yield", "Stop", "No vehicles", "Vehicles over 3.5 metric tons prohibited",
    "No entry", "General caution", "Dangerous curve left",
    "Dangerous curve right", "Double curve", "Bumpy road", "Slippery road",

    "Road narrows on the right", "Road work", "Traffic signals",
    "Pedestrians", "Children crossing", "Bicycles crossing",
    "Beware of ice/snow", "Wild animals crossing", "End of all speed and passing limits",
    "Turn right ahead", "Turn left ahead", "Ahead only", "Go straight or right",
    "Go straight or left", "Keep right", "Keep left", "Roundabout mandatory",
    "End of no passing", "End of no passing by vehicles over 3.5 metric tons"
])

# 3. Kamera aç
cap = cv2.VideoCapture(0)

# Kırmızı renk için HSV aralıkları
lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Gürültü azaltma
    frame_blur = cv2.GaussianBlur(frame, (5, 5), 0)

    # Görüntüyü HSV renk uzayına çevir
    hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)

    # Kırmızı maskesi
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Maskeyi uygula ve konturları bul
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Çok küçük konturları at
            # Yaklaşık çokgen
            epsilon = 0.04 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            x, y, w, h = cv2.boundingRect(approx)

            # ROI’ye padding ekle (kırpmayı daha rahat yapmak için)
            pad = int(0.1 * w)  # %10 padding
            x1 = max(x - pad, 0)
            y1 = max(y - pad, 0)
            x2 = min(x + w + pad, frame.shape[1])
            y2 = min(y + h + pad, frame.shape[0])

            roi = frame[y1:y2, x1:x2]

            # Eğer ROI çok küçük değilse işle
            if roi.size == 0:
                continue

            # ROI’yi normalize etme öncesi kontrastı eşitle
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi_gray = cv2.equalizeHist(roi_gray)
            roi_eq = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2BGR)

            # Model input boyutu
            roi_resized = cv2.resize(roi_eq, (32, 32))

            # Model tahmini
            roi_array = roi_resized / 255.0
            roi_array = np.expand_dims(roi_array, axis=0)
            predictions = model.predict(roi_array, verbose=0)
            class_idx = np.argmax(predictions)
            confidence = np.max(predictions)
            class_name = class_names[class_idx]

            # Şekil
            if len(approx) == 3:
                shape = "Triangle"
            elif len(approx) > 7:
                shape = "Circle"
            else:
                shape = "Unknown"

            # Güven eşiği (örnek: %60 üstü)
            if confidence > 0.6:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame,
                            f"{class_name} ({shape}) {confidence*100:.1f}%",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(frame, f"Low confidence ({shape})",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    # Son görüntüyü göster
    cv2.imshow("Traffic Sign Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC ile çık
        break

cap.release()
cv2.destroyAllWindows()
