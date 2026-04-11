# Service Layer Status

## Wired Through Services
- POST /auth/login
- GET /patients
- GET /patients/{patient_id}
- GET /notes/{patient_id}
- POST /notes/{patient_id}
- GET /orders/{patient_id}
- POST /orders/{patient_id}
- GET /appointments
- POST /appointments

## Architecture
- routes -> services -> repositories

## Preserved
- API contracts preserved
- Web compatibility preserved
- App compatibility preserved

## Next Step
Move more clinical domains to service-backed flow:
- reports
- nursing
- mar
- labs
- radiology
