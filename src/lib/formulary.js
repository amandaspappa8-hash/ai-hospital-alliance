export const formulary = [
    {
        id: "amox_500_po_tab",
        name: "Amoxicillin",
        genericName: "Amoxicillin",
        strength: "500 mg",
        form: "capsule",
        route: "PO",
        atc: "J01CA04",
        warnings: ["Allergy to penicillins may cause anaphylaxis."],
        renalAdjust: "Adjust dose if eGFR < 30 (demo).",
        maxDailyDose: "3 g/day (demo)",
        pregnancy: "B",
        tags: ["antibiotic", "beta-lactam"],
    },
    {
        id: "azith_500_po_tab",
        name: "Azithromycin",
        genericName: "Azithromycin",
        strength: "500 mg",
        form: "tablet",
        route: "PO",
        atc: "J01FA10",
        warnings: ["QT prolongation risk (demo)."],
        hepaticAdjust: "Use caution in severe hepatic impairment (demo).",
        pregnancy: "B",
        tags: ["antibiotic", "macrolide"],
    },
    {
        id: "warfarin_po_tab",
        name: "Warfarin",
        genericName: "Warfarin",
        form: "tablet",
        route: "PO",
        atc: "B01AA03",
        warnings: ["High bleeding risk. Monitor INR."],
        pregnancy: "X",
        tags: ["anticoagulant"],
    },
    {
        id: "ibuprofen_400_po_tab",
        name: "Ibuprofen",
        genericName: "Ibuprofen",
        strength: "400 mg",
        form: "tablet",
        route: "PO",
        atc: "M01AE01",
        warnings: ["GI bleed risk; renal risk; avoid in late pregnancy (demo)."],
        renalAdjust: "Avoid/limit if CKD (demo).",
        maxDailyDose: "1200–2400 mg/day (demo)",
        pregnancy: "C",
        tags: ["NSAID", "pain"],
    },
    {
        id: "metformin_500_po_tab",
        name: "Metformin",
        genericName: "Metformin",
        strength: "500 mg",
        form: "tablet",
        route: "PO",
        atc: "A10BA02",
        warnings: ["Lactic acidosis risk in severe renal impairment."],
        renalAdjust: "Avoid if eGFR < 30; reduce if 30–45 (demo).",
        tags: ["diabetes"],
    },
    {
        id: "simvastatin_20_po_tab",
        name: "Simvastatin",
        genericName: "Simvastatin",
        strength: "20 mg",
        form: "tablet",
        route: "PO",
        atc: "C10AA01",
        warnings: ["Myopathy risk; CYP3A4 interactions."],
        tags: ["lipids"],
    },
];
export const interactions = [
    {
        a: "warfarin_po_tab",
        b: "ibuprofen_400_po_tab",
        severity: "major",
        summary: "Increased bleeding risk (anticoagulant + NSAID).",
        recommendation: "Avoid combination if possible; consider PPI and close monitoring.",
    },
    {
        a: "warfarin_po_tab",
        b: "azith_500_po_tab",
        severity: "moderate",
        summary: "May increase INR/bleeding risk (demo).",
        recommendation: "Monitor INR more frequently; adjust dose as needed.",
    },
    {
        a: "simvastatin_20_po_tab",
        b: "azith_500_po_tab",
        severity: "moderate",
        summary: "Increased statin level → myopathy risk (demo).",
        recommendation: "Consider temporary hold or alternative antibiotic; monitor muscle symptoms.",
    },
];
export function findDrugById(id) {
    return formulary.find((d) => d.id === id);
}
export function searchDrugs(query) {
    const q = query.trim().toLowerCase();
    if (!q)
        return formulary;
    return formulary.filter((d) => {
        const hay = `${d.name} ${d.genericName ?? ""} ${d.strength ?? ""} ${d.form ?? ""} ${d.atc ?? ""}`.toLowerCase();
        return hay.includes(q);
    });
}
export function getInteractionsForDrugIds(drugIds) {
    const set = new Set(drugIds);
    return interactions.filter((x) => set.has(x.a) && set.has(x.b) || set.has(x.b) && set.has(x.a));
}
