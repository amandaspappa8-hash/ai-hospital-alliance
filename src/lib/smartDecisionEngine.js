export function runSmartDecisionEngine(patient) {
    const condition = String(patient?.condition ?? "").toLowerCase();
    if (condition.includes("chest") || condition.includes("card")) {
        return {
            impression: "High-risk cardiac presentation suspected.",
            plan: [
                "Immediate ECG",
                "Troponin and cardiac enzymes",
                "Continuous monitoring",
            ],
            nextStep: "Admit patient to monitored cardiac unit.",
            riskLevel: "high",
        };
    }
    return {
        impression: "Stable general clinical presentation.",
        plan: [
            "Baseline laboratory screening",
            "Routine clinical review",
            "Follow-up with responsible department",
        ],
        nextStep: "Continue standard evaluation workflow.",
        riskLevel: "medium",
    };
}
