# Persistence Rules

## Web
- Web should consume stable IDs
- Web should not depend on translated backend enums
- Web may cache but not redefine business entities

## App
- App must consume same stable entity IDs
- App should use same contracts for:
  - patients
  - appointments
  - notes
  - orders
  - reports
  - AI outputs
- Offline model can be added later without changing core entity meaning

## Platform
- Platform owns persistence rules
- API should remain source of truth
- In-memory demo state must later map to DB entities with minimal contract changes

## AI
- AI outputs must define:
  - transient output
  - persisted output
  - audit requirement
- Suggested orders created by AI should persist as orders with source=ai
- Human-readable rationale may be stored as snapshot later

## Languages
- No translated values in core persistence
- Enums stay stable in English-like neutral constants
- UI handles translation
