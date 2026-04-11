# AI Service Layer Status

## Wired Through Services
- POST /ai/clinical-route
- POST /ai/clinical-route-and-create-orders/{patient_id}
- GET /drug-intel/reconciliation/{patient_id}
- GET /drug-intel/discharge-counseling/{patient_id}
- GET /drug-intel/recommendations/{patient_id}
- POST /drug-intel/recommendations
- GET /drug-intel/dose-safety/{patient_id}
- POST /drug-intel/dose-safety
- GET /drug-intel/interactions/{patient_id}
- POST /drug-intel/interactions

## Architecture
- routes -> services -> repositories / AI engines

## Preserved
- API contracts preserved
- Web compatibility preserved
- App compatibility preserved

## Next Step
Split remaining AI helper logic from main.py into dedicated engine/service modules.
