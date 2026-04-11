def generate_radiology_report(prediction):
    if prediction["abnormal"] > 0.7:
        return "Findings suggest abnormal radiological pattern. Further evaluation recommended."
    else:
        return "No significant abnormality detected."
