# Next Execution Decision

## Immediate Next Build Decision
The next real implementation task should be:

### Database repository foundation

## Why
- Persistence is the biggest gap between prototype and MVP
- Auth, web, app, and AI all depend on stable persistence
- Current system still uses in-memory stores and localStorage heavily

## First Migration Target
1. users
2. patients
3. notes
4. orders

## Principle
Do not break API contracts while replacing in-memory stores with repository-backed access.
