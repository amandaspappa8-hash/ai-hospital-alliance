# Engineering Rules

## Before writing any feature/function:
1. Define whether it belongs to Shared / Platform / Web / App / AI
2. Define input and output contract
3. Define role access
4. Define impact on:
   - browser
   - app
   - platform
5. Define persistence needs
6. Define monitoring/logging needs

## Function writing rule
Every new function should answer:
- Can web use it?
- Can app use it?
- Does backend expose it safely?
- Is there one API contract for both web and app?
- Is business logic separated from UI?

## Folder rule
- Shared logic should not live inside page UI when reusable
- API shape should be documented before expanding UI
- AI logic should stay in backend/services or shared engine layer
