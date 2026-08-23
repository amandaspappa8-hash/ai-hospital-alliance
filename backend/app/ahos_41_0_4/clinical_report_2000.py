from datetime import datetime
from backend.app.ahos_41_0_4.infer_rsna_2000 import predict

def generate_clinical_report(image_path: str):
    ai = predict(image_path)
    prob = ai["pneumonia_probability"]
    prediction = ai["prediction"]
    risk = ai["risk_level"]

    if prediction == "PNEUMONIA_OPACITY":
        impression = "AI findings suggest possible lung opacity compatible with suspected pneumonia pattern."
        recommendation = "Recommend radiologist review, clinical correlation, oxygen saturation assessment, CBC/CRP if clinically indicated."
    else:
        impression = "No AI-detected pneumonia opacity pattern on this processed chest X-ray image."
        recommendation = "Recommend routine clinical correlation. Radiologist confirmation remains required."

    return {
        "report_id": "AHOS-RSNA-2000-" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "phase": "AHOS 41.1.5",
        "module": "RSNA 2000 Clinical Report Generator",
        "image_path": image_path,
        "ai_model": "rsna_resnet18_2000.pt",
        "threshold": 0.30,
        "ai_result": {
            "pneumonia_probability": prob,
            "prediction": prediction,
            "risk_level": risk
        },
        "clinical_report": {
            "exam": "Chest X-ray",
            "ai_findings": prediction,
            "impression": impression,
            "recommendation": recommendation,
            "disclaimer": "This is an AI-assisted research output, not a final medical diagnosis. Final interpretation must be made by a licensed radiologist."
        }
    }
