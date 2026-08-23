from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text
from datetime import datetime
from uuid import uuid4
from .database import Base

def uid(prefix):
    return f"{prefix}-{uuid4().hex[:10].upper()}"

class Hospital(Base):
    __tablename__ = "ahos_hospitals"

    id = Column(String, primary_key=True, default=lambda: uid("HOSP"))
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=True)
    tenant_id = Column(String, nullable=False, default="default")
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class AhosUser(Base):
    __tablename__ = "ahos_users"

    id = Column(String, primary_key=True, default=lambda: uid("USER"))
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(Text, nullable=False)
    role = Column(String, nullable=False, default="viewer")
    tenant_id = Column(String, nullable=False, default="default")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ClinicalCase(Base):
    __tablename__ = "ahos_clinical_cases"

    id = Column(String, primary_key=True, default=lambda: uid("CASE"))
    hospital_id = Column(String, nullable=False)
    patient_id = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    ai_prediction = Column(String, nullable=False)
    ai_confidence = Column(Float, nullable=False)
    clinician_decision = Column(String, nullable=False)
    agreement = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MonitoringMetric(Base):
    __tablename__ = "ahos_monitoring_metrics"

    id = Column(String, primary_key=True, default=lambda: uid("METRIC"))
    hospital_id = Column(String, nullable=False)
    cpu_usage = Column(Float, default=0)
    memory_usage = Column(Float, default=0)
    api_latency_ms = Column(Integer, default=0)
    status = Column(String, default="healthy")
    created_at = Column(DateTime, default=datetime.utcnow)

class Partnership(Base):
    __tablename__ = "ahos_partnerships"

    id = Column(String, primary_key=True, default=lambda: uid("PARTNER"))
    partner_name = Column(String, nullable=False)
    partner_type = Column(String, nullable=False)
    country = Column(String, nullable=False)
    strategic_value = Column(Integer, default=0)
    deal_value_usd = Column(Float, default=0)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
