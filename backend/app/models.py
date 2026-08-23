from sqlalchemy.orm import relationship, backref
import uuid
from datetime import datetime, date
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, Date,
    ForeignKey, Enum, JSON, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, TSVECTOR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class TenantStatus(str, PyEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    CANCELLED = "cancelled"

class TenantPlan(str, PyEnum):
    STARTER = "starter"
    GROWTH = "growth"
    ENTERPRISE = "enterprise"

class UserRole(str, PyEnum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    PHARMACIST = "pharmacist"
    LAB_TECH = "lab_tech"
    RADIOLOGIST = "radiologist"
    RECEPTIONIST = "receptionist"

class Gender(str, PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class RiskLevel(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class TenantMixin:
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)

class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(Enum(TenantStatus), default=TenantStatus.TRIAL, nullable=False)
    plan = Column(Enum(TenantPlan), default=TenantPlan.STARTER, nullable=False)
    admin_email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50))
    country = Column(String(100))
    city = Column(String(100))
    timezone = Column(String(50), default="UTC")
    locale = Column(String(10), default="ar")
    stripe_customer_id = Column(String(100), unique=True)
    stripe_subscription_id = Column(String(100), unique=True)
    monthly_patient_quota = Column(Integer, default=500)
    current_month_patients = Column(Integer, default=0)
    settings = Column(JSONB, default=dict)
    clinical_brain_enabled = Column(Boolean, default=True)
    icd11_enabled = Column(Boolean, default=True)
    dicom_enabled = Column(Boolean, default=False)
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    patients = relationship("Patient", back_populates="tenant", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="tenant", cascade="all, delete-orphan")

class User(Base, TimestampMixin, TenantMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_user_email_per_tenant"),
        Index("ix_users_tenant_role", "tenant_id", "role"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    full_name = Column(String(255), nullable=False)
    full_name_ar = Column(String(255))
    phone = Column(String(50))
    license_number = Column(String(100))
    specialty = Column(String(100))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    tenant = relationship("Tenant", back_populates="users")
    department = relationship("Department")

class Department(Base, TimestampMixin, TenantMixin):
    __tablename__ = "departments"
    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_dept_code_per_tenant"),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255))
    code = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    tenant = relationship("Tenant", back_populates="departments")

class Patient(Base, TimestampMixin, TenantMixin):
    __tablename__ = "patients"
    __table_args__ = (
        UniqueConstraint("tenant_id", "mrn", name="uq_mrn_per_tenant"),
        Index("ix_patients_search", "tenant_id", "search_vector", postgresql_using="gin"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    mrn = Column(String(50), nullable=False)
    full_name = Column(String(255), nullable=False)
    full_name_ar = Column(String(255))
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    national_id = Column(String(50))
    nationality = Column(String(100))
    blood_type = Column(String(10))
    phone = Column(String(50))
    phone_emergency = Column(String(50))
    email = Column(String(255))
    address = Column(Text)
    allergies = Column(ARRAY(String), default=list)
    chronic_conditions = Column(ARRAY(String), default=list)
    current_medications = Column(JSONB, default=list)
    insurance_provider = Column(String(255))
    insurance_number = Column(String(100))
    insurance_expiry = Column(Date)
    search_vector = Column(TSVECTOR)
    tenant = relationship("Tenant", back_populates="patients")
    encounters = relationship("Encounter", back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient")

class Encounter(Base, TimestampMixin, TenantMixin):
    __tablename__ = "encounters"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    attending_doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    encounter_type = Column(String(50))
    chief_complaint = Column(Text)
    status = Column(String(50), default="active")
    admitted_at = Column(DateTime(timezone=True))
    discharged_at = Column(DateTime(timezone=True))
    primary_diagnosis_code = Column(String(20))
    primary_diagnosis_text = Column(String(500))
    secondary_diagnoses = Column(JSONB, default=list)
    discharge_summary = Column(Text)
    patient = relationship("Patient", back_populates="encounters")
    attending_doctor = relationship("User", foreign_keys=[attending_doctor_id])
    vitals = relationship("Vitals", back_populates="encounter", cascade="all, delete-orphan")
    lab_orders = relationship("LabOrder", back_populates="encounter", cascade="all, delete-orphan")
    radiology_orders = relationship("RadiologyOrder", back_populates="encounter")
    medications = relationship("MedicationOrder", back_populates="encounter")
    ai_analyses = relationship("ClinicalAIAnalysis", back_populates="encounter")

class Vitals(Base, TimestampMixin, TenantMixin):
    __tablename__ = "vitals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    temperature = Column(Float)
    systolic_bp = Column(Integer)
    diastolic_bp = Column(Integer)
    heart_rate = Column(Integer)
    respiratory_rate = Column(Integer)
    oxygen_saturation = Column(Float)
    weight_kg = Column(Float)
    height_cm = Column(Float)
    bmi = Column(Float)
    pain_score = Column(Integer)
    blood_glucose = Column(Float)
    notes = Column(Text)
    encounter = relationship("Encounter", back_populates="vitals")

class LabOrder(Base, TimestampMixin, TenantMixin):
    __tablename__ = "lab_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    ordered_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    test_name = Column(String(255), nullable=False)
    test_code = Column(String(50))
    status = Column(String(50), default="pending")
    priority = Column(String(20), default="routine")
    collected_at = Column(DateTime(timezone=True))
    resulted_at = Column(DateTime(timezone=True))
    results = relationship("LabResult", back_populates="order", cascade="all, delete-orphan")
    encounter = relationship("Encounter", back_populates="lab_orders")

class LabResult(Base, TimestampMixin, TenantMixin):
    __tablename__ = "lab_results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("lab_orders.id"), nullable=False)
    parameter_name = Column(String(255), nullable=False)
    value = Column(String(100), nullable=False)
    unit = Column(String(50))
    reference_min = Column(Float)
    reference_max = Column(Float)
    is_abnormal = Column(Boolean, default=False)
    is_critical = Column(Boolean, default=False)
    direction = Column(String(10))
    order = relationship("LabOrder", back_populates="results")

class RadiologyOrder(Base, TimestampMixin, TenantMixin):
    __tablename__ = "radiology_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    ordered_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    modality = Column(String(50))
    body_part = Column(String(100))
    clinical_indication = Column(Text)
    dicom_study_uid = Column(String(255))
    report = Column(Text)
    impression = Column(Text)
    is_critical = Column(Boolean, default=False)
    performed_at = Column(DateTime(timezone=True))
    reported_at = Column(DateTime(timezone=True))
    encounter = relationship("Encounter", back_populates="radiology_orders")

class MedicationOrder(Base, TimestampMixin, TenantMixin):
    __tablename__ = "medication_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    prescribed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    dispensed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    drug_name = Column(String(255), nullable=False)
    drug_name_ar = Column(String(255))
    generic_name = Column(String(255))
    dose = Column(String(100))
    route = Column(String(50))
    frequency = Column(String(100))
    duration_days = Column(Integer)
    quantity = Column(Integer)
    drug_interaction_alerts = Column(JSONB, default=list)
    dispensed_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    encounter = relationship("Encounter", back_populates="medications")

class ICD11Code(Base):
    __tablename__ = "icd11_codes"
    __table_args__ = (
        Index("ix_icd11_search", "search_vector", postgresql_using="gin"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    entity_id = Column(String(100))
    title = Column(String(500), nullable=False)
    title_ar = Column(String(500))
    definition = Column(Text)
    parent_code = Column(String(20), ForeignKey("icd11_codes.code"), nullable=True)
    chapter = Column(String(5))
    block = Column(String(50))
    is_leaf = Column(Boolean, default=True)
    search_vector = Column(TSVECTOR)
    children = relationship("ICD11Code", primaryjoin="ICD11Code.parent_code == foreign(ICD11Code.code)", uselist=True)

class ICD11Mapping(Base):
    __tablename__ = "icd11_mappings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    icd10_code = Column(String(20), nullable=False, index=True)
    icd11_code = Column(String(20), ForeignKey("icd11_codes.code"), nullable=False)
    mapping_type = Column(String(20))
    icd11 = relationship("ICD11Code")

class ClinicalAIAnalysis(Base, TimestampMixin, TenantMixin):
    __tablename__ = "clinical_ai_analyses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    requested_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    input_payload = Column(JSONB, nullable=False)
    risk_score = Column(Integer)
    risk_level = Column(Enum(RiskLevel))
    differential_diagnosis = Column(JSONB, default=list)
    recommended_treatment = Column(JSONB, default=list)
    drug_interaction_alerts = Column(JSONB, default=list)
    critical_alerts = Column(JSONB, default=list)
    disposition = Column(String(100))
    clinical_summary = Column(Text)
    ai_provider = Column(String(50))
    ai_model = Column(String(100))
    latency_ms = Column(Integer)
    tokens_used = Column(Integer)
    doctor_accepted = Column(Boolean, nullable=True)
    doctor_notes = Column(Text)
    actual_diagnosis_code = Column(String(20), ForeignKey("icd11_codes.code"), nullable=True)
    encounter = relationship("Encounter", back_populates="ai_analyses")

class Appointment(Base, TimestampMixin, TenantMixin):
    __tablename__ = "appointments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=20)
    status = Column(String(50), default="scheduled")
    reason = Column(Text)
    notes = Column(Text)
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("User", foreign_keys=[doctor_id])

class AuditLog(Base, TenantMixin):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_tenant_time", "tenant_id", "created_at"),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(UUID(as_uuid=True))
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    changes = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=True)
    message = Column(Text, nullable=False)
    severity = Column(String(20), nullable=True)
    source = Column(String(80), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
