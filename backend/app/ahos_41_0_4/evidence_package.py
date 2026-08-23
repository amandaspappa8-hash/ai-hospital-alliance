import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

from backend.app.ahos_41_0_4.report_db_2000 import get_report
from backend.app.ahos_41_0_4.export_reports_xai import export_pdf_xai, export_json_xai
from backend.app.ahos_41_0_4.xai.gradcam import save_heatmap

EVIDENCE_DIR = Path("reports/rsna/evidence_packages")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def build_evidence_package(report_id: str):
    report = get_report(report_id)

    if not report:
        return None

    if "xai" not in report:
        xai = save_heatmap(report["image_path"])
        report["xai"] = xai

    pdf = export_pdf_xai(report)
    js = export_json_xai(report)

    package_dir = EVIDENCE_DIR / report_id
    package_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "package_id": f"EVIDENCE-{report_id}",
        "report_id": report_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "phase": "AHOS 41.2.3",
        "package_type": "XAI_AUDIT_EVIDENCE_PACKAGE",
        "included_files": []
    }

    files_to_copy = [
        ("clinical_report_pdf", pdf),
        ("clinical_report_json", js),
        ("xai_heatmap", report.get("xai", {}).get("heatmap")),
        ("xai_overlay", report.get("xai", {}).get("overlay")),
    ]

    for label, path in files_to_copy:
        if path and Path(path).exists():
            dst = package_dir / Path(path).name
            shutil.copy2(path, dst)
            manifest["included_files"].append({
                "type": label,
                "path": str(dst)
            })

    manifest_path = package_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    zip_path = EVIDENCE_DIR / f"{report_id}_evidence_package.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in package_dir.iterdir():
            z.write(f, arcname=f.name)

    return {
        "status": "created",
        "phase": "AHOS 41.2.3",
        "report_id": report_id,
        "package_dir": str(package_dir),
        "zip_file": str(zip_path),
        "manifest": str(manifest_path),
        "files_count": len(manifest["included_files"])
    }


def list_evidence_packages():
    packages = []

    for p in EVIDENCE_DIR.glob("*_evidence_package.zip"):
        packages.append({
            "zip_file": str(p),
            "size_bytes": p.stat().st_size
        })

    return packages
