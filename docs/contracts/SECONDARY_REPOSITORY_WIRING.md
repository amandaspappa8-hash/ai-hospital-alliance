# Secondary Repository Wiring

## Target Routes
- GET /appointments
- POST /appointments
- GET /reports
- GET /nursing/vitals/{patient_id}
- POST /nursing/vitals/{patient_id}
- GET /nursing/notes/{patient_id}
- POST /nursing/notes/{patient_id}
- GET /mar/{patient_id}
- POST /mar/{patient_id}

## Goal
Move secondary clinical routes from direct in-memory access
to repository-backed access without changing API contracts.
