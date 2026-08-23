from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from backend.app.db.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    region = Column(String)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    full_name = Column(String)
    gender = Column(String)
    birth_date = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Encounter(Base):
    __tablename__ = "encounters"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    encounter_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    department = Column(String)
    status = Column(String, default="in-progress")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LabResult(Base):
    __tablename__ = "lab_results"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    test_code = Column(String)
    test_name = Column(String)
    value = Column(String)
    unit = Column(String)
    abnormal_flag = Column(String)
    critical = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RadiologyStudy(Base):
    __tablename__ = "radiology_studies"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    study_uid = Column(String, unique=True, index=True)
    modality = Column(String)
    description = Column(String)
    ohif_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    medication_name = Column(String)
    dosage = Column(String)
    frequency = Column(String)
    duration_days = Column(Integer)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DrugInventory(Base):
    __tablename__ = "drug_inventory"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    drug_name = Column(String, index=True)
    stock_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=50)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FHIRResource(Base):
    __tablename__ = "fhir_resources"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    resource_type = Column(String, index=True)
    resource_id = Column(String, index=True)
    resource_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    actor = Column(String)
    role = Column(String)
    action = Column(String)
    resource = Column(String)
    severity = Column(String)
    ip_address = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
