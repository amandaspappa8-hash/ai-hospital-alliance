# AI Engine Contract

## Goal
Formalize AI engine input/output contracts for:
- clinical routing
- medication reconciliation
- discharge counseling
- medication recommendations
- dose safety
- interaction analysis

## Rules
1. Engine inputs must be plain data
2. Engine outputs must be serializable
3. Services call engines through stable interfaces
4. API routes must not depend on engine internals
5. Language translation stays outside core engine logic

## Engine List
- Clinical Routing Engine
- Medication Reconciliation Engine
- Discharge Counseling Engine
- Medication Recommendations Engine
- Dose Safety Engine
- Interaction Analysis Engine
