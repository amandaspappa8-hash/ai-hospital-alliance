export function buildVisitTimeline(patient) {
    const now = new Date();
    const date = now.toLocaleDateString();
    const time = now.toLocaleTimeString();
    return [
        {
            id: "vt-1",
            time: `${date} ${time}`,
            title: "Patient Selected",
            description: `Opened profile for ${patient?.name ?? "Unknown Patient"}`,
            status: "done",
        },
        {
            id: "vt-2",
            time: `${date} ${time}`,
            title: "Clinical Review",
            description: `Department: ${patient?.department ?? "General"}`,
            status: "active",
        },
        {
            id: "vt-3",
            time: `${date} ${time}`,
            title: "Decision Preparation",
            description: `Condition: ${patient?.condition ?? "N/A"}`,
            status: "pending",
        },
    ];
}
