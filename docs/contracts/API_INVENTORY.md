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
