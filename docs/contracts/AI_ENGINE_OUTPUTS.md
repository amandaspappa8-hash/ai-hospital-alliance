# AI Engine Outputs

## Clinical Routing Output
- chief_complaint
- triage_level
- urgency_score
- route_to[]
- suggested_orders[]
- red_flags[]
- next_actions[]
- rationale[]

## Reconciliation Output
- patientId optional
- homeMeds[]
- admissionMeds[]
- dischargeMeds[]
- findings[]
- summary{}

## Discharge Counseling Output
- patientId optional
- dischargeMeds[]
- counseling[]
- generalAdvice[]
- summary{}

## Recommendations Output
- patientId optional
- age
- count
- medications[]
- recommendations[]
- summary{}

## Dose Safety Output
- patientId optional
- age
- count
- medications[]
- findings[]
- summary{}

## Interactions Output
- patientId optional
- count
- medications[]
- findings[]
- summary{}
