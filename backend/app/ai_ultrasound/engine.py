import cv2
from ultralytics import YOLO
from pathlib import Path

model = YOLO("yolov8n.pt")

UPLOAD_DIR = Path("app/uploads")
RESULT_DIR = Path("app/results")

def analyze_ultrasound(image_path: str):

    image = cv2.imread(image_path)

    results = model(image)

    findings = []

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            conf = float(box.conf[0])

            cls = int(box.cls[0])

            label = model.names[cls]

            color = (0, 0, 255)

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

            cv2.putText(
                image,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

            findings.append({
                "label": label,
                "confidence": conf,
                "location": [x1, y1, x2, y2]
            })

    output_path = RESULT_DIR / "result.jpg"

    cv2.imwrite(str(output_path), image)

    return {
        "success": True,
        "findings": findings,
        "output": str(output_path)
    }
