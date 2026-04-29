"""Run this after docker compose up to populate PostgreSQL"""

import os, sys

sys.path.insert(0, "/app")
os.environ.setdefault("DATABASE_URL", "postgresql://aiha:aiha123@db:5432/aiha_db")

from .db import create_tables, SessionLocal
from .models import *

create_tables()
db = SessionLocal()

try:
    if db.query(Hospital).count() > 0:
        print("✅ Database already seeded")
        db.close()
        sys.exit(0)

    db.add(
        Hospital(
            id="H-001",
            name="AI Hospital Alliance",
            address="Medical City, Tripoli",
            phone="+218910000000",
        )
    )
    db.flush()

    depts = [
        Department(name="Cardiology", code="CARD", hospital_id="H-001"),
        Department(name="Emergency", code="ER", hospital_id="H-001"),
        Department(name="ICU", code="ICU", hospital_id="H-001"),
        Department(name="Radiology", code="RAD", hospital_id="H-001"),
        Department(name="Neurology", code="NEURO", hospital_id="H-001"),
        Department(name="Pediatrics", code="PEDS", hospital_id="H-001"),
        Department(name="Orthopedics", code="ORTH", hospital_id="H-001"),
    ]
    db.add_all(depts)
    db.flush()
    dm = {d.code: d.id for d in depts}

    try:
        from .auth import hash_password

        pw = hash_password
    except:
        pw = lambda x: x

    db.add_all(
        [
            User(
                username="admin",
                password=pw("admin123"),
                name="System Admin",
                role="Admin",
                hospital_id="H-001",
            ),
            User(
                username="doctor",
                password=pw("doctor123"),
                name="Dr. Mohammed",
                role="Doctor",
                hospital_id="H-001",
            ),
            User(
                username="nurse",
                password=pw("nurse123"),
                name="Nurse Sara",
                role="Nurse",
                hospital_id="H-001",
            ),
            User(
                username="radiology",
                password=pw("radio123"),
                name="Radiology User",
                role="Radiology",
                hospital_id="H-001",
            ),
        ]
    )

    db.add_all(
        [
            Doctor(
                id="D-1001",
                name="Dr. Sarah Jones",
                specialty="Neurology",
                department_id=dm["NEURO"],
                hospital_id="H-001",
                experience="12 years",
                status="Available",
                rating=4.9,
                patients_count=28,
                schedule="08:00-16:00",
                phone="+218910100001",
            ),
            Doctor(
                id="D-1002",
                name="Dr. John Smith",
                specialty="Cardiology",
                department_id=dm["CARD"],
                hospital_id="H-001",
                experience="15 years",
                status="On Call",
                rating=4.8,
                patients_count=34,
                schedule="09:00-17:00",
                phone="+218910100002",
            ),
            Doctor(
                id="D-1003",
                name="Dr. Emily Brown",
                specialty="Orthopedics",
                department_id=dm["ORTH"],
                hospital_id="H-001",
                experience="10 years",
                status="Available",
                rating=4.7,
                patients_count=22,
                schedule="08:30-15:30",
                phone="+218910100003",
            ),
            Doctor(
                id="D-1004",
                name="Dr. Ahmed Kareem",
                specialty="Emergency",
                department_id=dm["ER"],
                hospital_id="H-001",
                experience="9 years",
                status="In Surgery",
                rating=4.6,
                patients_count=19,
                schedule="24/7",
                phone="+218910100004",
            ),
            Doctor(
                id="D-1005",
                name="Dr. Lina Salem",
                specialty="Radiology",
                department_id=dm["RAD"],
                hospital_id="H-001",
                experience="11 years",
                status="Available",
                rating=4.9,
                patients_count=17,
                schedule="10:00-18:00",
                phone="+218910100005",
            ),
            Doctor(
                id="D-1006",
                name="Dr. Omar Hassan",
                specialty="Pediatrics",
                department_id=dm["PEDS"],
                hospital_id="H-001",
                experience="13 years",
                status="Offline",
                rating=4.8,
                patients_count=26,
                schedule="09:00-14:00",
                phone="+218910100006",
            ),
            Doctor(
                id="D-1007",
                name="Dr. Noor Al-Masri",
                specialty="ICU",
                department_id=dm["ICU"],
                hospital_id="H-001",
                experience="14 years",
                status="Available",
                rating=4.9,
                patients_count=12,
                schedule="07:00-15:00",
                phone="+218910100007",
            ),
            Doctor(
                id="D-1008",
                name="Dr. Youssef Adel",
                specialty="Cardiology",
                department_id=dm["CARD"],
                hospital_id="H-001",
                experience="8 years",
                status="Available",
                rating=4.5,
                patients_count=16,
                schedule="12:00-20:00",
                phone="+218910100008",
            ),
        ]
    )

    db.add_all(
        [
            Patient(
                id="P-1001",
                name="Ahmed Ali",
                age=45,
                gender="Male",
                phone="+218910000001",
                condition="Chest Pain",
                department_id=dm["CARD"],
                hospital_id="H-001",
                status="Active",
            ),
            Patient(
                id="P-1002",
                name="Sara Omar",
                age=31,
                gender="Female",
                phone="+218910000002",
                condition="Fever",
                department_id=dm["ER"],
                hospital_id="H-001",
                status="Under Observation",
            ),
            Patient(
                id="P-1003",
                name="Mona Salem",
                age=62,
                gender="Female",
                phone="+218910000003",
                condition="Low Oxygen Saturation",
                department_id=dm["ICU"],
                hospital_id="H-001",
                status="Critical",
            ),
            Patient(
                id="P-1004",
                name="Khalid Hassan",
                age=55,
                gender="Male",
                phone="+218910000004",
                condition="Diabetes Type 2",
                department_id=dm["CARD"],
                hospital_id="H-001",
                status="Active",
            ),
            Patient(
                id="P-1005",
                name="Fatima Ali",
                age=28,
                gender="Female",
                phone="+218910000005",
                condition="Appendicitis",
                department_id=dm["ER"],
                hospital_id="H-001",
                status="Under Observation",
            ),
        ]
    )

    db.add_all(
        [
            Appointment(
                id="A-2001",
                patient_id="P-1001",
                doctor_id="D-1002",
                department="Cardiology",
                date="2026-04-15",
                time="10:00",
                status="Scheduled",
            ),
            Appointment(
                id="A-2002",
                patient_id="P-1002",
                doctor_id="D-1004",
                department="Emergency",
                date="2026-04-15",
                time="11:30",
                status="Waiting",
            ),
            Appointment(
                id="A-2003",
                patient_id="P-1003",
                doctor_id="D-1007",
                department="ICU",
                date="2026-04-15",
                time="08:00",
                status="Scheduled",
            ),
        ]
    )

    db.add_all(
        [
            Alert(
                patient_id="P-1003",
                message="CRITICAL: SpO2 87% — immediate respiratory intervention",
                severity="critical",
                source="nursing",
            ),
            Alert(
                patient_id="P-1001",
                message="CRITICAL: ST elevation — possible STEMI",
                severity="critical",
                source="cardiology",
            ),
            Alert(
                patient_id="P-1004",
                message="HIGH: Blood glucose 320 mg/dL",
                severity="high",
                source="lab",
            ),
        ]
    )

    db.commit()
    print(
        f"✅ PostgreSQL seeded! Patients: {db.query(Patient).count()}, Doctors: {db.query(Doctor).count()}"
    )
except Exception as e:
    db.rollback()
    print(f"❌ Seed error: {e}")
    import traceback

    traceback.print_exc()
finally:
    db.close()
