export const AI_DRUG_FORMULARY = [
    {
        name: "Aspirin 81 mg",
        generic: "aspirin",
        category: "Antiplatelet",
        usualDose: "81 mg once daily",
        route: ["PO"],
        frequency: ["Once daily"],
        warnings: [
            "Bleeding risk may increase with NSAIDs",
            "Use caution in history of GI bleeding",
        ],
        contraindications: [
            "Active bleeding",
            "Severe aspirin allergy",
        ],
        counseling: [
            "Take after food unless physician instructed otherwise",
            "Report black stool, bleeding, vomiting blood, or severe dizziness",
            "Avoid extra NSAIDs unless approved",
        ],
    },
    {
        name: "Atorvastatin 40 mg",
        generic: "atorvastatin",
        category: "Statin",
        usualDose: "40 mg once daily",
        route: ["PO"],
        frequency: ["Evening", "Once daily"],
        warnings: [
            "Monitor muscle pain",
            "Use caution in liver disease",
        ],
        contraindications: [
            "Active liver disease",
            "Known severe statin intolerance",
        ],
        counseling: [
            "Take once daily in the evening",
            "Report severe muscle pain or dark urine",
            "Avoid excess alcohol",
        ],
    },
    {
        name: "Metoprolol 50 mg",
        generic: "metoprolol",
        category: "Beta blocker",
        usualDose: "50 mg once daily or as prescribed",
        route: ["PO"],
        frequency: ["Once daily", "Twice daily"],
        warnings: [
            "May cause dizziness or slow pulse",
            "Use caution in asthma or severe bradycardia",
        ],
        contraindications: [
            "Severe bradycardia",
            "Cardiogenic shock",
        ],
        counseling: [
            "Take at the same time each day",
            "Do not stop suddenly",
            "Seek help if fainting, very slow heart rate, or breathing worsens",
        ],
    },
    {
        name: "Ibuprofen 400 mg",
        generic: "ibuprofen",
        category: "NSAID",
        usualDose: "400 mg every 8 hours as needed",
        route: ["PO"],
        frequency: ["q8h PRN"],
        warnings: [
            "May increase GI bleeding risk",
            "Avoid with aspirin unless physician approves",
        ],
        contraindications: [
            "Active GI bleeding",
            "Severe NSAID allergy",
            "Severe renal impairment without review",
        ],
        counseling: [
            "Take after food",
            "Do not combine with other NSAIDs unless approved",
            "Seek help if stomach pain, black stool, or bleeding occurs",
        ],
    },
];
export function searchDrugFormulary(query) {
    const q = query.trim().toLowerCase();
    if (!q)
        return [];
    return AI_DRUG_FORMULARY.filter((drug) => drug.name.toLowerCase().includes(q) ||
        drug.generic.toLowerCase().includes(q) ||
        drug.category.toLowerCase().includes(q));
}
export function getDrugCounselingFromFormulary(name) {
    const q = name.trim().toLowerCase();
    return AI_DRUG_FORMULARY.find((drug) => drug.name.toLowerCase() === q ||
        drug.generic.toLowerCase() === q) || null;
}
