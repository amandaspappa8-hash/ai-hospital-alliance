# Service Layer Contract

## Purpose
Introduce a service layer between:
- routes
- repositories

## Goal
Routes should handle HTTP only.
Services should handle business logic.
Repositories should handle data access.

## Initial Service Targets
- auth
- patients
- notes
- orders
- appointments

## Flow
route -> service -> repository

## Rules
1. Routes should stay thin
2. Services should preserve API contracts
3. Repositories should remain storage-focused
4. Future DB migration should not require route rewrites
