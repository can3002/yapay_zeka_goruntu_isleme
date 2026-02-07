import cv2
import argparse
from ultralytics import YOLO
import supervision as sv
import numpy as np

ZONE_POLYGON = np.array([
    [0, 0],
    [1280 // 2, 0],
    [1280 // 2, 720],
    [0, 720]
])

def parse_arguements() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", default=(1280,720), nargs=2, type=int)
    args = parser.parse_args()
    return args

def main():
    args = parse_arguements()
    frame_w, frame_h = args.webcam_resolution
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_h)

    model = YOLO("yolov8l.pt")
    box_annotator = sv.BoxAnnotator()
    
    zone = sv.PolygonZone(polygon=ZONE_POLYGON)
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone,
        color=sv.Color.RED,
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kamera görüntüsü alınamadı.")
            break

        results = model(frame)[0]

        detections = sv.Detections(
            xyxy=results.boxes.xyxy.cpu().numpy(),
            confidence=results.boxes.conf.cpu().numpy(),
            class_id=results.boxes.cls.cpu().numpy().astype(int)
        )

        # Kutuları çiz
        anot_frame = box_annotator.annotate(
            scene=frame.copy(),
            detections=detections,
        )

        # Zone trigger ve annotate
        mask = zone.trigger(detections=detections)  # zone içinde olan nesneler maskesi
        anot_frame = zone_annotator.annotate(scene=anot_frame)

        # Sayacı ekranda göster
        count_text = f"Objects in zone: {np.sum(mask)}"
        cv2.putText(anot_frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0,0,255), 2)

        cv2.imshow("yolov8", anot_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
