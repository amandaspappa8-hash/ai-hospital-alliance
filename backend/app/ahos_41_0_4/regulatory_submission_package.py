import zipfile
import json
from pathlib import Path
from datetime import datetime

DOSSIER_DIR = Path("reports/rsna/regulatory_dossiers")
EXPORT_DIR = Path("reports/rsna/regulatory_exports")
SUBMISSION_DIR = Path("reports/rsna/regulatory_submissions")

SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

def latest_file(folder: Path, pattern: str):
    files = sorted(folder.glob(pattern), reverse=True)
    return files[0] if files else None

def build_submission_package(report_id: str):
    dossier_pdf = latest_file(DOSSIER_DIR, f"*{report_id}*.pdf")
    dossier_json = latest_file(DOSSIER_DIR, f"*{report_id}*.json")
    regulatory_zip = latest_file(EXPORT_DIR, f"*{report_id}*.zip")

    if not dossier_pdf:
        return {
            "status": "blocked",
            "reason": "DOSSIER_PDF_NOT_FOUND",
            "report_id": report_id
        }

    submission_id = "REG-SUBMISSION-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
    package_dir = SUBMISSION_DIR / submission_id
    package_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "submission_id": submission_id,
        "phase": "AHOS 41.3.2",
        "report_id": report_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "contents": {
            "dossier_pdf": str(dossier_pdf) if dossier_pdf else None,
            "dossier_json": str(dossier_json) if dossier_json else None,
            "regulatory_export_zip": str(regulatory_zip) if regulatory_zip else None
        },
        "submission_scope": [
            "FDA SaMD audit preparation",
            "EU CE/MDR technical file preparation",
            "Radiology AI governance package",
            "Clinical review and lock traceability",
            "Integrity verification and recovery evidence"
        ],
        "disclaimer": "Submission package is for research and regulatory-preparation only."
    }

    manifest_path = package_dir / "submission_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    readme = f"""AHOS 41.3.2 Regulatory Submission Package

Submission ID: {submission_id}
Report ID: {report_id}

Included:
- Regulatory PDF dossier
- Dossier JSON
- Regulatory audit ZIP, if available
- Submission manifest

Scope:
FDA SaMD / EU CE MDR preparation package.

Disclaimer:
This package is not an official regulatory submission.
"""

    readme_path = package_dir / "README.txt"
    readme_path.write_text(readme)

    zip_path = SUBMISSION_DIR / f"{submission_id}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(manifest_path, arcname="submission_manifest.json")
        z.write(readme_path, arcname="README.txt")

        if dossier_pdf:
            z.write(dossier_pdf, arcname=dossier_pdf.name)

        if dossier_json:
            z.write(dossier_json, arcname=dossier_json.name)

        if regulatory_zip:
            z.write(regulatory_zip, arcname=regulatory_zip.name)

    return {
        "status": "created",
        "phase": "AHOS 41.3.2",
        "report_id": report_id,
        "submission_id": submission_id,
        "zip_file": str(zip_path),
        "package_dir": str(package_dir),
        "manifest": str(manifest_path),
        "readme": str(readme_path)
    }

def list_submission_packages(limit: int = 20):
    packages = []
    for p in sorted(SUBMISSION_DIR.glob("*.zip"), reverse=True)[:limit]:
        packages.append({
            "zip_file": str(p),
            "size_bytes": p.stat().st_size
        })
    return packages
