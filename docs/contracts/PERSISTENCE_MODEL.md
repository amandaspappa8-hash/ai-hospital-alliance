# Persistence Model

## Core Tables

### users
- id
- username
- name
- role
- email (later)
- password_hash (later)
- status
- created_at
- updated_at
- last_login_at (later)

### patients
- id
- name
- age
- gender
- phone
- condition
- department
- status
- created_at
- updated_at

### appointments
- id
- patient_id
- patient_name_snapshot
- department
- doctor
- date
- time
- status
- created_at
- updated_at

### notes
- id
- patient_id
- text
- author_user_id (later)
- created_at
- updated_at

### orders
- id
- patient_id
- item
- type
- priority
- status
- source (manual/ai)
- created_at
- updated_at

### reports
- id
- patient_id
- title
- type
- status
- body (later if persisted fully)
- created_at
- updated_at

### nursing_vitals
- id
- patient_id
- temperature
- blood_pressure
- heart_rate
- respiratory_rate
- oxygen_saturation
- recorded_at
- recorded_by_user_id (later)

### nursing_notes
- id
- patient_id
- text
- recorded_at
- recorded_by_user_id (later)

### mar_items
- id
- patient_id
- medication
- dose
- route
- schedule
- status
- given_at
- pharmacist_review_status (later)
- pharmacist_review_note (later)
- created_at
- updated_at

### doctor_assignments
- id
- doctor_id
- patient_id
- specialty
- priority
- status
- created_at
- updated_at

## AI Tables (Later)

### ai_clinical_runs
- id
- patient_id nullable
- chief_complaint
- input_payload
- output_payload
- urgency_score
- triage_level
- created_at
- created_by_user_id nullable

### ai_order_runs
- id
- patient_id
- input_payload
- output_payload
- created_order_count
- created_at

### pharmacy_reviews
- id
- patient_id
- medication_set_snapshot
- findings_snapshot
- reviewer_user_id
- status
- note
- created_at

### discharge_counseling_snapshots
- id
- patient_id
- medication_snapshot
- counseling_payload
- created_at
