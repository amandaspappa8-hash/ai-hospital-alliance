# Repository Foundation Contract

## Purpose
Create a repository layer that separates:
- API/routes
- business logic
- data access

## Initial Repository Targets
- users
- patients
- notes
- orders

## Rules
1. Route handlers should not own persistence details
2. Repository methods should be stable and reusable
3. API contracts must not change during migration
4. Web and App must continue using same response shapes
5. AI should consume stable repository-backed entities later

## Current Mode
- in-memory repositories

## Future Mode
- PostgreSQL-backed repositories

## Repository Design Principle
Use the same repository interface now and later,
only swap implementation from in-memory to database.
