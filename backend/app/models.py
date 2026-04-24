from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .db import Base

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(String(20), primary_key=True)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    phone = Column(String(30))
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("User", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password = Column(String(256), nullable=False)
    name = Column(String(120))
    role = Column(String(40), nullable=False)
    hospital_id = Column(String(20), ForeignKey("hospitals.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    hospital = relationship("Hospital", back_populates="users")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True)
    hospital_id = Column(String(20), ForeignKey("hospitals.id"))
    doctors = relationship("Doctor", back_populates="department")
    patients = relationship("Patient", back_populates="department")

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(String(20), primary_key=True)
    name = Column(String(120), nullable=False)
    specialty = Column(String(100))
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    hospital_id = Column(String(20), ForeignKey("hospitals.id"), nullable=True)
    experience = Column(String(40))
    status = Column(String(40), default="Available")
    rating = Column(Float, default=0.0)
    patients_count = Column(Integer, default=0)
    schedule = Column(String(80))
    phone = Column(String(30))
    created_at = Column(DateTime, default=datetime.utcnow)
    department = relationship("Department", back_populates="doctors")
    hospital = relationship("Hospital", back_populates="doctors")
    assignments = relationship("DoctorAssignment", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(String(20), primary_key=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer)
    gender = Column(String(20))
    phone = Column(String(30))
    condition = Column(String(200))
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    hospital_id = Column(String(20), ForeignKey("hospitals.id"), nullable=True)
    status = Column(String(40), default="Active")
    admitted_at = Column(DateTime, default=datetime.utcnow)
    discharged_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    hospital = relationship("Hospital", back_populates="patients")
    department = relationship("Department", back_populates="patients")
    notes = relationship("ClinicalNote", back_populates="patient")
    orders = relationship("ClinicalOrder", back_populates="patient")
    vitals = relationship("NursingVital", back_populates="patient")
    nursing_notes = relationship("NursingNote", back_populates="patient")
    mar_items = relationship("MARItem", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    assignments = relationship("DoctorAssignment", back_populates="patient")
    reports = relationship("Report", back_populates="patient")
    lab_orders = relationship("LabOrder", back_populates="patient")
    radiology_orders = relationship("RadiologyOrder", back_populates="patient")

class ClinicalNote(Base):
    __tablename__ = "clinical_notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="notes")
    author = relationship("User")

class ClinicalOrder(Base):
    __tablename__ = "clinical_orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    item = Column(String(200), nullable=False)
    type = Column(String(80), default="manual")
    priority = Column(String(20), default="Routine")
    status = Column(String(40), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    patient = relationship("Patient", back_populates="orders")
    author = relationship("User")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=True)
    doctor_id = Column(String(20), ForeignKey("doctors.id"), nullable=True)
    department = Column(String(100))
    date = Column(String(20))
    time = Column(String(10))
    status = Column(String(40), default="Scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class DoctorAssignment(Base):
    __tablename__ = "doctor_assignments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(String(20), ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    condition = Column(String(200))
    status = Column(String(40), default="Assigned")
    assigned_at = Column(DateTime, default=datetime.utcnow)
    doctor = relationship("Doctor", back_populates="assignments")
    patient = relationship("Patient", back_populates="assignments")

class NursingVital(Base):
    __tablename__ = "nursing_vitals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    nurse_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    temperature = Column(String(20))
    blood_pressure = Column(String(20))
    heart_rate = Column(String(20))
    respiratory_rate = Column(String(20))
    oxygen_saturation = Column(String(20))
    recorded_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="vitals")
    nurse = relationship("User")

class NursingNote(Base):
    __tablename__ = "nursing_notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    nurse_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="nursing_notes")
    nurse = relationship("User")

class MARItem(Base):
    __tablename__ = "mar_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    medication = Column(String(200), nullable=False)
    dose = Column(String(80))
    route = Column(String(40))
    schedule = Column(String(80))
    status = Column(String(40), default="Pending")
    given_at = Column(String(10))
    pharmacy_review = Column(String(100))
    ai_flag = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    patient = relationship("Patient", back_populates="mar_items")

class Report(Base):
    __tablename__ = "reports"
    id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(200))
    type = Column(String(80))
    status = Column(String(40), default="In Progress")
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    patient = relationship("Patient", back_populates="reports")
    author = relationship("User")

class LabOrder(Base):
    __tablename__ = "lab_orders"
    id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=True)
    ordered_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    section = Column(String(80))
    tests = Column(JSON)
    priority = Column(String(20), default="Routine")
    status = Column(String(40), default="Pending")
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    patient = relationship("Patient", back_populates="lab_orders")
    ordered_by_user = relationship("User")

class RadiologyOrder(Base):
    __tablename__ = "radiology_orders"
    id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=True)
    ordered_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    section = Column(String(40))
    studies = Column(JSON)
    priority = Column(String(20), default="Routine")
    status = Column(String(40), default="Pending")
    study_uid = Column(String(200))
    report = Column(Text)
    ai_result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    patient = relationship("Patient", back_populates="radiology_orders")
    ordered_by_user = relationship("User")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=True)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="moderate")
    source = Column(String(80))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient")

class AIInferenceRun(Base):
    __tablename__ = "ai_inference_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=True)
    model_type = Column(String(40))
    input_path = Column(String(500))
    result = Column(JSON)
    risk_level = Column(String(20))
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient")
    requested_by_user = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(String(50), nullable=False)
    action      = Column(String(100), nullable=False)
    resource    = Column(String(100), nullable=False)
    resource_id = Column(String(100), default="")
    details     = Column(Text, default="")
    ip_address  = Column(String(50), default="")
    success     = Column(Boolean, default=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    user_id    = Column(String(50), nullable=False)
    token_hash = Column(String(200), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked    = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
