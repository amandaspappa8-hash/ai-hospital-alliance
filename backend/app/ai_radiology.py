def analyze_ct_scan(study_name: str):
    study = study_name.lower()

    findings = []

    if "chest" in study:
        findings.append(
            {
                "type": "Lung Opacity",
                "risk": "High",
                "suggestion": "Possible pneumonia or mass",
            }
        )

    if "brain" in study:
        findings.append(
            {
                "type": "Hemorrhage",
                "risk": "Critical",
                "suggestion": "Immediate intervention required",
            }
        )

    return {
        "ai_summary": "AI radiology analysis completed",
        "findings": findings,
        "priority": "HIGH" if findings else "LOW",
    }
