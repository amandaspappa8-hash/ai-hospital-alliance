# Database Contract

## Purpose
Define the persistent data model for:
- Platform
- Web
- App
- AI
- Future production database

## Persistence Principles
1. Core business entities must be persistent
2. UI-only state must not be stored in core database unless needed
3. AI outputs must define whether they are transient or persistent
4. Shared entity IDs must remain stable across web/app/platform
5. Language labels must not be stored as translated values in business tables
6. Business enums must remain language-neutral

## Persistence Categories

### Persistent Core
- users
- patients
- appointments
- notes
- orders
- reports
- nursing_vitals
- nursing_notes
- mar_items
- doctor_assignments
- specialty_summaries if materialized later

### Persistent AI-Related
- ai_clinical_runs (later)
- ai_order_runs (later)
- pharmacy_reviews (later)
- reconciliation_snapshots (later)
- discharge_counseling_snapshots (later)

### Non-Persistent / Derived
- temporary UI filters
- page-only local state
- translated labels
- display formatting
- computed dashboard summaries unless materialized for performance

## Database Rules
- IDs must be stable
- timestamps must be explicit
- role values must be constant
- status values must be constant
- language translation must remain in UI layer
- app and web must consume same entity shapes where possible
