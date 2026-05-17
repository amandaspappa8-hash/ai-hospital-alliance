#!/usr/bin/env python3
import argparse
import json
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent.parent / "backend" / "data"
OUTPUT_FILE = OUTPUT_DIR / "icd11_simplified.json"

ESSENTIAL_CODES = [
    {"code": "CA40", "title": "Community-acquired pneumonia", "title_ar": "الالتهاب الرئوي المكتسب من المجتمع", "chapter": "11", "is_leaf": True},
    {"code": "CA41", "title": "Hospital-acquired pneumonia", "title_ar": "الالتهاب الرئوي المستشفوي", "chapter": "11", "is_leaf": True},
    {"code": "CA22", "title": "Chronic obstructive pulmonary disease", "title_ar": "مرض الانسداد الرئوي المزمن", "chapter": "11", "is_leaf": True},
    {"code": "CA20", "title": "Acute bronchitis", "title_ar": "التهاب الشعب الهوائية الحاد", "chapter": "11", "is_leaf": True},
    {"code": "CA23", "title": "Asthma", "title_ar": "الربو", "chapter": "11", "is_leaf": True},
    {"code": "CB00", "title": "Pulmonary embolism", "title_ar": "الانسداد الرئوي", "chapter": "11", "is_leaf": True},
    {"code": "CA42", "title": "COVID-19", "title_ar": "كوفيد-19", "chapter": "11", "is_leaf": True},
    {"code": "BA80", "title": "Essential hypertension", "title_ar": "ارتفاع ضغط الدم الأساسي", "chapter": "9", "is_leaf": True},
    {"code": "BA41", "title": "Angina pectoris", "title_ar": "الذبحة الصدرية", "chapter": "9", "is_leaf": True},
    {"code": "BA60", "title": "Acute myocardial infarction", "title_ar": "احتشاء عضلة القلب الحاد", "chapter": "9", "is_leaf": True},
    {"code": "BD10", "title": "Stroke", "title_ar": "السكتة الدماغية", "chapter": "9", "is_leaf": True},
    {"code": "BC43", "title": "Heart failure", "title_ar": "قصور القلب", "chapter": "9", "is_leaf": True},
    {"code": "BA84", "title": "Atrial fibrillation", "title_ar": "الرجفان الأذيني", "chapter": "9", "is_leaf": True},
    {"code": "5A10", "title": "Type 2 diabetes mellitus", "title_ar": "السكري من النوع الثاني", "chapter": "5", "is_leaf": True},
    {"code": "JA00", "title": "Type 1 diabetes mellitus", "title_ar": "السكري من النوع الأول", "chapter": "5", "is_leaf": True},
    {"code": "5B55", "title": "Obesity", "title_ar": "السمنة", "chapter": "5", "is_leaf": True},
    {"code": "5A00", "title": "Hypothyroidism", "title_ar": "قصور الغدة الدرقية", "chapter": "5", "is_leaf": True},
    {"code": "5A20", "title": "Hyperthyroidism", "title_ar": "فرط نشاط الغدة الدرقية", "chapter": "5", "is_leaf": True},
    {"code": "DA40", "title": "Acute appendicitis", "title_ar": "التهاب الزائدة الدودية الحاد", "chapter": "10", "is_leaf": True},
    {"code": "DA91", "title": "Peptic ulcer disease", "title_ar": "مرض قرحة المعدة", "chapter": "10", "is_leaf": True},
    {"code": "DB93", "title": "Gallstones", "title_ar": "حصوات المرارة", "chapter": "10", "is_leaf": True},
    {"code": "DA20", "title": "Acute gastroenteritis", "title_ar": "التهاب المعدة والأمعاء الحاد", "chapter": "10", "is_leaf": True},
    {"code": "GC08", "title": "Urinary tract infection", "title_ar": "التهاب المسالك البولية", "chapter": "14", "is_leaf": True},
    {"code": "GB60", "title": "Kidney stones", "title_ar": "حصوات الكلى", "chapter": "14", "is_leaf": True},
    {"code": "GC40", "title": "Acute kidney injury", "title_ar": "الفشل الكلوي الحاد", "chapter": "14", "is_leaf": True},
    {"code": "GB61", "title": "Chronic kidney disease", "title_ar": "الفشل الكلوي المزمن", "chapter": "14", "is_leaf": True},
    {"code": "MB24", "title": "Fever", "title_ar": "حمى", "chapter": "21", "is_leaf": True},
    {"code": "MD12", "title": "Abdominal pain", "title_ar": "ألم في البطن", "chapter": "21", "is_leaf": True},
    {"code": "MA01", "title": "Headache", "title_ar": "صداع", "chapter": "21", "is_leaf": True},
    {"code": "MD81", "title": "Nausea and vomiting", "title_ar": "غثيان وقيء", "chapter": "21", "is_leaf": True},
    {"code": "MD90", "title": "Diarrhea", "title_ar": "إسهال", "chapter": "21", "is_leaf": True},
    {"code": "MA72", "title": "Chest pain", "title_ar": "ألم في الصدر", "chapter": "21", "is_leaf": True},
    {"code": "MD21", "title": "Shortness of breath", "title_ar": "ضيق في التنفس", "chapter": "21", "is_leaf": True},
    {"code": "MC10", "title": "Back pain", "title_ar": "ألم في الظهر", "chapter": "21", "is_leaf": True},
    {"code": "6A70", "title": "Major depressive disorder", "title_ar": "اضطراب الاكتئاب الكبير", "chapter": "6", "is_leaf": True},
    {"code": "6B00", "title": "Generalised anxiety disorder", "title_ar": "اضطراب القلق العام", "chapter": "6", "is_leaf": True},
    {"code": "1C62", "title": "Sepsis", "title_ar": "الإنتان", "chapter": "1", "is_leaf": True},
    {"code": "1C10", "title": "Tuberculosis", "title_ar": "السل", "chapter": "1", "is_leaf": True},
    {"code": "1D41", "title": "Malaria", "title_ar": "الملاريا", "chapter": "1", "is_leaf": True},
    {"code": "NB90", "title": "Burn", "title_ar": "حرق", "chapter": "22", "is_leaf": True},
    {"code": "NA00", "title": "Fracture of skull", "title_ar": "كسر الجمجمة", "chapter": "22", "is_leaf": True},
    {"code": "5A11", "title": "Type 2 diabetes with complications", "title_ar": "السكري من النوع الثاني مع مضاعفات", "chapter": "5", "is_leaf": True},
    {"code": "BA80.1", "title": "Hypertensive heart disease", "title_ar": "مرض القلب الناجم عن ارتفاع ضغط الدم", "chapter": "9", "is_leaf": True},
]

def generate_essential_bundle():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(ESSENTIAL_CODES, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ Essential bundle saved: {len(ESSENTIAL_CODES)} codes")
    logger.info(f"   File: {OUTPUT_FILE}")

def download_from_who(chapters=None):
    try:
        import httpx
    except ImportError:
        logger.error("httpx not installed. Run: pip install httpx")
        return

    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get("https://id.who.int/icd", follow_redirects=True)
            if resp.status_code >= 500:
                raise Exception("Server error")
        logger.info("✅ WHO API reachable — but full download requires credentials")
        logger.info("   Register free at: https://icdaccessmanagement.who.int/")
        logger.info("   Then set: WHO_ICD11_CLIENT_ID and WHO_ICD11_CLIENT_SECRET")
        logger.info("   Generating essential bundle instead...")
    except Exception:
        logger.warning("⚠️  WHO API not reachable — generating essential bundle")

    generate_essential_bundle()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download ICD-11 codes")
    parser.add_argument("--bundled-only", action="store_true", help="Generate essential offline bundle only")
    parser.add_argument("--chapters", nargs="+", help="Chapters to download from WHO API")
    args = parser.parse_args()

    if args.bundled_only:
        generate_essential_bundle()
    else:
        download_from_who(args.chapters)
