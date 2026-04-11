# API Contracts

## Contract Template

### Endpoint
- Method:
- Path:

### Purpose
-

### Consumers
- Web:
- App:
- AI:
- Languages:

### Request
```json
{}

## 2) أنشئ ملف inventory للـ endpoints
```bash
cd ~/Projects/ai-hospital-alliance && \
cat > docs/contracts/API_INVENTORY.md << 'EOF'
# API Inventory

## Core
- GET /
- POST /auth/login
- GET /patients
- GET /patients/{patient_id}
- GET /orders/{patient_id}
- POST /orders/{patient_id}
- GET /notes/{patient_id}
- POST /notes/{patient_id}
- GET /appointments
- POST /appointments
- GET /reports

## Doctors / Specialties
- GET /doctors/summary
- GET /doctors/by-specialty/{name}
- GET /doctors/{doctor_id}
- GET /doctor-assignments/{doctor_id}
- POST /doctor-assignments/{doctor_id}
- POST /doctor-assignments/{doctor_id}/{assignment_id}/status
- DELETE /doctor-assignments/{doctor_id}/{assignment_id}
- GET /specialties/summary

## PACS / Nursing / MAR
- GET /pacs/studies
- GET /nursing/vitals/{patient_id}
- POST /nursing/vitals/{patient_id}
- GET /nursing/notes/{patient_id}
- POST /nursing/notes/{patient_id}
- GET /mar/{patient_id}
- POST /mar/{patient_id}
- PUT /mar/{patient_id}/{id}/status
- PUT /mar/{patient_id}/{id}/pharmacist-review

## AI Clinical
- POST /clinical-route
- POST /clinical-route-and-create-orders/{patient_id}

## Drug Intelligence
- GET /drug-intel/reconciliation/{patient_id}
- GET /drug-intel/discharge-counseling/{patient_id}
- GET /drug-intel/recommendations/{patient_id}
- POST /drug-intel/recommendations
- GET /drug-intel/dose-safety/{patient_id}
- POST /drug-intel/dose-safety
- GET /drug-intel/interactions/{patient_id}
- POST /drug-intel/interactions
- GET /drug-intel/search
- GET /drug-intel/dailymed

---

## Endpoint
- Method: POST
- Path: /auth/login

### Purpose
- Authenticate user and return session token plus role context

### Consumers
- Web: Login page
- App: Future mobile login
- AI: No
- Languages: UI labels only

### Request
```json
{
  "username": "admin",
  "password": "admin123"
}
{
  "access_token": "demo-token-admin",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "name": "System Admin",
    "role": "Admin"
  }
}
[
  {
    "id": "P-1001",
    "name": "Ahmed Ali",
    "age": 45,
    "gender": "Male",
    "phone": "+218910000001",
    "condition": "Chest Pain",
    "department": "Cardiology",
    "status": "Active"
  }
]
{
  "id": "P-1001",
  "name": "Ahmed Ali",
  "age": 45,
  "gender": "Male",
  "phone": "+218910000001",
  "condition": "Chest Pain",
  "department": "Cardiology",
  "status": "Active"
}
{
  "chief_complaint": "severe chest pain radiating to arm",
  "age": 65,
  "gender": "male",
  "vitals": {
    "bp": "160/100",
    "hr": 120
  }
}
{
  "chief_complaint": "severe chest pain radiating to arm",
  "triage_level": "urgent",
  "urgency_score": 6,
  "route_to": ["Emergency", "Cardiology"],
  "suggested_orders": [
    {
      "name": "ECG",
      "priority": "stat",
      "category": "cardiac"
    }
  ],
  "red_flags": ["tachycardia"],
  "next_actions": [
    "Immediate physician review"
  ],
  "rationale": [
    "Chest pain identified as main complaint."
  ]
}
{
  "chief_complaint": "fever and cough",
  "age": 42,
  "gender": "male",
  "vitals": {
    "temp": "38.5",
    "hr": 102
  }
}
{
  "clinical_route": {
    "triage_level": "urgent",
    "route_to": ["Emergency"]
  },
  "created_orders": [
    {
      "id": 1,
      "item": "CBC",
      "status": "Draft"
    }
  ]
}
{
  "findings": [
    {
      "severity": "high",
      "title": "Bleeding risk",
      "detail": "NSAID + anticoagulant combination may increase bleeding risk."
    }
  ],
  "summary": {
    "high_risk_count": 1,
    "moderate_risk_count": 0
  }
}

---

# المرحلة 4 — إنشاء جدول توافق Web / App / AI / Languages

## 6) أنشئ مصفوفة رسمية للعقود
```bash
cd ~/Projects/ai-hospital-alliance && \
cat > docs/contracts/API_CONTRACT_MATRIX.md << 'EOF'
# API Contract Matrix

| Endpoint | Web | App | AI | Languages | Priority |
|---|---|---|---|---|---|
| /auth/login | Yes | Yes | No | UI only | P0 |
| /patients | Yes | Yes | Indirect | UI only | P0 |
| /patients/{patient_id} | Yes | Yes | Indirect | UI only | P0 |
| /appointments | Yes | Yes | No | UI only | P1 |
| /reports | Yes | Yes | Partial | UI only | P1 |
| /orders/{patient_id} | Yes | Yes | Indirect | UI only | P0 |
| /notes/{patient_id} | Yes | Yes | Indirect | UI only | P1 |
| /ai/clinical-route | Yes | Yes | Core | Human text later | P0 |
| /ai/clinical-route-and-create-orders/{patient_id} | Yes | Yes | Core | Human text later | P0 |
| /drug-intel/interactions/{patient_id} | Yes | Yes | Core | Human text later | P0 |
| /drug-intel/dose-safety/{patient_id} | Yes | Yes | Core | Human text later | P0 |
| /drug-intel/recommendations/{patient_id} | Yes | Yes | Core | Human text later | P0 |
| /drug-intel/reconciliation/{patient_id} | Yes | Yes | Core | Human text later | P1 |
| /drug-intel/discharge-counseling/{patient_id} | Yes | Yes | Core | Human text later | P1 |
