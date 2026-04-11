# Database Decision

## Current State
- Demo/in-memory platform
- UI and API contracts are already forming
- Project is ready for persistence planning

## Recommended Next Step
Adopt a production-ready relational persistence model.

## Recommended Primary Option
- PostgreSQL

## Why
- Good fit for hospital/business entities
- Clear relational structure
- Strong support for audit/history models
- Good fit for future auth, orders, notes, MAR, and reporting
- Good support for API stability and app/web sharing

## ORM / Access Layer
- To be decided later:
  - SQLAlchemy
  - Prisma-like pattern later if stack changes

## Migration Principle
Move from in-memory stores to DB-backed repositories
without breaking:
- API contracts
- Web consumers
- App consumers
- AI contracts
