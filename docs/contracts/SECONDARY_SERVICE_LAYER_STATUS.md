# Secondary Service Layer Status

## Wired Through Services
- GET /reports
- GET /nursing/vitals/{patient_id}
- POST /nursing/vitals/{patient_id}
- GET /nursing/notes/{patient_id}
- POST /nursing/notes/{patient_id}
- GET /mar/{patient_id}
- POST /mar/{patient_id}

## Architecture
- routes -> services -> repositories

## Preserved
- API contracts preserved
- Web compatibility preserved
- App compatibility preserved

## Next Step
Move remaining domains:
- labs
- radiology
- doctor assignments
- AI-adjacent persistence flows
