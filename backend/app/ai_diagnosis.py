def auto_diagnose(mask):
    import numpy as np

    volume = np.array(mask)
    tumor_size = volume.sum()

    if tumor_size > 5000:
        return {
            "diagnosis": "Large Tumor Detected",
            "risk": "CRITICAL",
            "action": "Immediate intervention required"
        }
    elif tumor_size > 1000:
        return {
            "diagnosis": "Moderate Lesion",
            "risk": "HIGH",
            "action": "Further imaging needed"
        }
    else:
        return {
            "diagnosis": "No significant abnormality",
            "risk": "LOW",
            "action": "Routine follow-up"
        }
