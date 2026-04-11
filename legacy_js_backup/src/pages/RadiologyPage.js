import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
const studiesSeed = [
    {
        id: "RAD-1001",
        patient: "Ali Hassan",
        modality: "CT",
        bodyPart: "Chest",
        priority: "Urgent",
        status: "In Progress",
        time: "09:15",
    },
    {
        id: "RAD-1002",
        patient: "Sara Omar",
        modality: "MRI",
        bodyPart: "Brain",
        priority: "Routine",
        status: "Scheduled",
        time: "10:00",
    },
    {
        id: "RAD-1003",
        patient: "Mohamed Salem",
        modality: "X-Ray",
        bodyPart: "Left Leg",
        priority: "STAT",
        status: "Critical",
        time: "08:40",
    },
    {
        id: "RAD-1004",
        patient: "Lina Kareem",
        modality: "Ultrasound",
        bodyPart: "Abdomen",
        priority: "Routine",
        status: "Completed",
        time: "07:55",
    },
];
function statusClasses(status) {
    switch (status) {
        case "Completed":
            return "bg-emerald-100 text-emerald-700 border border-emerald-200";
        case "In Progress":
            return "bg-cyan-100 text-cyan-700 border border-cyan-200";
        case "Scheduled":
            return "bg-sky-100 text-sky-700 border border-sky-200";
        case "Critical":
            return "bg-rose-100 text-rose-700 border border-rose-200";
        default:
            return "bg-slate-100 text-slate-700 border border-slate-200";
    }
}
function priorityClasses(priority) {
    switch (priority) {
        case "STAT":
            return "bg-rose-600 text-white";
        case "Urgent":
            return "bg-amber-500 text-white";
        case "Routine":
            return "bg-teal-600 text-white";
        default:
            return "bg-slate-600 text-white";
    }
}
export default function RadiologyPage() {
    const [query, setQuery] = useState("");
    const [reportText, setReportText] = useState("No acute cardiopulmonary abnormality. Mild bibasal linear atelectatic changes. Clinical correlation is advised.");
    const [selectedStudyId, setSelectedStudyId] = useState("RAD-1001");
    const filteredStudies = useMemo(() => {
        const q = query.trim().toLowerCase();
        if (!q)
            return studiesSeed;
        return studiesSeed.filter((study) => study.id.toLowerCase().includes(q) ||
            study.patient.toLowerCase().includes(q) ||
            study.modality.toLowerCase().includes(q) ||
            study.bodyPart.toLowerCase().includes(q));
    }, [query]);
    const selectedStudy = filteredStudies.find((study) => study.id === selectedStudyId) ??
        studiesSeed.find((study) => study.id === selectedStudyId) ??
        studiesSeed[0];
    return (_jsxs("div", { className: "min-h-screen bg-gradient-to-br from-cyan-50 via-teal-50 to-slate-100 p-6", children: [_jsxs("div", { className: "mb-6", children: [_jsx("h1", { className: "text-3xl font-bold text-teal-950", children: "Radiology Center" }), _jsx("p", { className: "mt-2 text-teal-800", children: "PACS, imaging workflow, AI triage, and radiology reporting" })] }), _jsxs("div", { className: "grid gap-6 md:grid-cols-4 mb-6", children: [_jsxs("div", { className: "rounded-2xl border border-cyan-200 bg-gradient-to-br from-cyan-100 to-teal-100 p-5 shadow-sm", children: [_jsx("div", { className: "text-sm text-teal-900", children: "Total Studies" }), _jsx("div", { className: "mt-3 text-3xl font-bold text-teal-950", children: "24" }), _jsx("div", { className: "mt-2 text-xs text-teal-800", children: "Today imaging volume" })] }), _jsxs("div", { className: "rounded-2xl border border-teal-200 bg-gradient-to-br from-teal-100 to-emerald-100 p-5 shadow-sm", children: [_jsx("div", { className: "text-sm text-teal-900", children: "In Progress" }), _jsx("div", { className: "mt-3 text-3xl font-bold text-teal-950", children: "6" }), _jsx("div", { className: "mt-2 text-xs text-teal-800", children: "Active radiology workflow" })] }), _jsxs("div", { className: "rounded-2xl border border-sky-200 bg-gradient-to-br from-sky-100 to-cyan-100 p-5 shadow-sm", children: [_jsx("div", { className: "text-sm text-teal-900", children: "Completed" }), _jsx("div", { className: "mt-3 text-3xl font-bold text-teal-950", children: "15" }), _jsx("div", { className: "mt-2 text-xs text-teal-800", children: "Finalized reports" })] }), _jsxs("div", { className: "rounded-2xl border border-rose-200 bg-gradient-to-br from-rose-50 to-orange-50 p-5 shadow-sm", children: [_jsx("div", { className: "text-sm text-rose-900", children: "Critical Alerts" }), _jsx("div", { className: "mt-3 text-3xl font-bold text-rose-700", children: "3" }), _jsx("div", { className: "mt-2 text-xs text-rose-800", children: "Require urgent review" })] })] }), _jsxs("div", { className: "grid gap-6 xl:grid-cols-12", children: [_jsxs("div", { className: "xl:col-span-4 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-cyan-200 bg-white/80 backdrop-blur p-5 shadow-sm", children: [_jsxs("div", { className: "flex items-center justify-between gap-3 mb-4", children: [_jsx("h2", { className: "text-xl font-bold text-teal-950", children: "Imaging Queue" }), _jsx("span", { className: "rounded-full bg-cyan-100 px-3 py-1 text-xs font-semibold text-cyan-700", children: "Live Queue" })] }), _jsx("input", { value: query, onChange: (e) => setQuery(e.target.value), placeholder: "Search patient, study, modality...", className: "w-full rounded-xl border border-cyan-200 bg-cyan-50/60 px-4 py-3 outline-none focus:border-teal-400" }), _jsx("div", { className: "mt-4 space-y-3", children: filteredStudies.map((study) => (_jsx("button", { onClick: () => setSelectedStudyId(study.id), className: `w-full rounded-2xl border p-4 text-left transition ${selectedStudyId === study.id
                                                ? "border-teal-400 bg-gradient-to-r from-cyan-50 to-teal-50 shadow"
                                                : "border-slate-200 bg-white hover:border-cyan-300 hover:bg-cyan-50/40"}`, children: _jsxs("div", { className: "flex items-start justify-between gap-3", children: [_jsxs("div", { children: [_jsx("div", { className: "font-semibold text-slate-900", children: study.patient }), _jsxs("div", { className: "mt-1 text-sm text-slate-600", children: [study.modality, " \u2022 ", study.bodyPart] }), _jsxs("div", { className: "mt-2 text-xs text-slate-500", children: ["Study ID: ", study.id, " \u2022 ", study.time] })] }), _jsxs("div", { className: "flex flex-col gap-2 items-end", children: [_jsx("span", { className: `rounded-full px-2.5 py-1 text-[11px] font-bold ${priorityClasses(study.priority)}`, children: study.priority }), _jsx("span", { className: `rounded-full px-2.5 py-1 text-[11px] font-semibold ${statusClasses(study.status)}`, children: study.status })] })] }) }, study.id))) })] }), _jsxs("div", { className: "rounded-2xl border border-teal-200 bg-gradient-to-br from-teal-100 to-cyan-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-teal-950 mb-4", children: "AI Findings" }), _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "rounded-xl bg-white/80 p-4 border border-teal-100", children: [_jsx("div", { className: "font-semibold text-teal-900", children: "Chest CT Triage" }), _jsx("div", { className: "mt-1 text-sm text-slate-700", children: "Mild lower-lobe atelectatic changes detected. No large pleural effusion." })] }), _jsxs("div", { className: "rounded-xl bg-white/80 p-4 border border-cyan-100", children: [_jsx("div", { className: "font-semibold text-cyan-900", children: "Brain MRI Signal Review" }), _jsx("div", { className: "mt-1 text-sm text-slate-700", children: "No obvious acute hemorrhagic signal pattern flagged by AI screening." })] }), _jsxs("div", { className: "rounded-xl bg-white/80 p-4 border border-rose-100", children: [_jsx("div", { className: "font-semibold text-rose-900", children: "Urgent Alert" }), _jsx("div", { className: "mt-1 text-sm text-slate-700", children: "STAT musculoskeletal trauma case requires consultant confirmation." })] })] })] })] }), _jsxs("div", { className: "xl:col-span-5 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-cyan-200 bg-white/80 p-5 shadow-sm", children: [_jsxs("div", { className: "flex items-center justify-between gap-3 mb-4", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-xl font-bold text-teal-950", children: "Study Viewer Panel" }), _jsx("p", { className: "text-sm text-slate-600 mt-1", children: "Selected study preview and imaging details" })] }), _jsx("button", { className: "rounded-xl bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700", children: "Open Viewer" })] }), _jsxs("div", { className: "rounded-2xl border border-dashed border-cyan-300 bg-gradient-to-br from-cyan-100 via-teal-50 to-white p-6", children: [_jsx("div", { className: "aspect-video rounded-2xl border border-cyan-200 bg-gradient-to-br from-slate-900 via-teal-950 to-cyan-950 p-6 text-white shadow-inner", children: _jsxs("div", { className: "flex h-full flex-col justify-between", children: [_jsxs("div", { children: [_jsx("div", { className: "text-lg font-semibold", children: "Imaging Preview" }), _jsxs("div", { className: "mt-2 text-sm text-cyan-100", children: [selectedStudy.modality, " \u2022 ", selectedStudy.bodyPart] })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4 text-sm", children: [_jsxs("div", { className: "rounded-xl bg-white/10 p-3 backdrop-blur", children: [_jsx("div", { className: "text-cyan-100", children: "Patient" }), _jsx("div", { className: "font-semibold", children: selectedStudy.patient })] }), _jsxs("div", { className: "rounded-xl bg-white/10 p-3 backdrop-blur", children: [_jsx("div", { className: "text-cyan-100", children: "Study ID" }), _jsx("div", { className: "font-semibold", children: selectedStudy.id })] }), _jsxs("div", { className: "rounded-xl bg-white/10 p-3 backdrop-blur", children: [_jsx("div", { className: "text-cyan-100", children: "Status" }), _jsx("div", { className: "font-semibold", children: selectedStudy.status })] }), _jsxs("div", { className: "rounded-xl bg-white/10 p-3 backdrop-blur", children: [_jsx("div", { className: "text-cyan-100", children: "Priority" }), _jsx("div", { className: "font-semibold", children: selectedStudy.priority })] })] })] }) }), _jsxs("div", { className: "mt-4 grid gap-3 sm:grid-cols-2", children: [_jsxs("div", { className: "rounded-xl bg-cyan-50 p-4 border border-cyan-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Modality" }), _jsx("div", { className: "font-semibold text-teal-950", children: selectedStudy.modality })] }), _jsxs("div", { className: "rounded-xl bg-teal-50 p-4 border border-teal-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Body Part" }), _jsx("div", { className: "font-semibold text-teal-950", children: selectedStudy.bodyPart })] })] })] })] }), _jsxs("div", { className: "rounded-2xl border border-teal-200 bg-gradient-to-br from-white to-teal-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-teal-950 mb-4", children: "Radiology Report" }), _jsx("textarea", { value: reportText, onChange: (e) => setReportText(e.target.value), className: "min-h-[220px] w-full rounded-2xl border border-cyan-200 bg-white px-4 py-4 outline-none focus:border-teal-400", placeholder: "Write radiology report..." }), _jsxs("div", { className: "mt-4 flex flex-wrap gap-3", children: [_jsx("button", { className: "rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white hover:bg-teal-700", children: "Save Report" }), _jsx("button", { className: "rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white hover:bg-cyan-700", children: "Finalize" }), _jsx("button", { className: "rounded-xl bg-slate-800 px-4 py-2 font-semibold text-white hover:bg-slate-900", children: "Send to PACS" })] })] })] }), _jsxs("div", { className: "xl:col-span-3 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-cyan-200 bg-gradient-to-br from-cyan-100 to-white p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-teal-950 mb-4", children: "Modality Load" }), _jsxs("div", { className: "space-y-3", children: [_jsx("div", { className: "rounded-xl bg-white p-4 border border-cyan-100", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "CT" }), _jsx("span", { className: "font-bold text-teal-950", children: "8" })] }) }), _jsx("div", { className: "rounded-xl bg-white p-4 border border-cyan-100", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "MRI" }), _jsx("span", { className: "font-bold text-teal-950", children: "5" })] }) }), _jsx("div", { className: "rounded-xl bg-white p-4 border border-cyan-100", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "X-Ray" }), _jsx("span", { className: "font-bold text-teal-950", children: "7" })] }) }), _jsx("div", { className: "rounded-xl bg-white p-4 border border-cyan-100", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Ultrasound" }), _jsx("span", { className: "font-bold text-teal-950", children: "4" })] }) })] })] }), _jsxs("div", { className: "rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-teal-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-teal-950 mb-4", children: "Quick Actions" }), _jsxs("div", { className: "space-y-3", children: [_jsx("button", { className: "w-full rounded-xl bg-teal-600 px-4 py-3 text-left font-semibold text-white hover:bg-teal-700", children: "+ New Imaging Order" }), _jsx("button", { className: "w-full rounded-xl bg-cyan-600 px-4 py-3 text-left font-semibold text-white hover:bg-cyan-700", children: "Open Worklist" }), _jsx("button", { className: "w-full rounded-xl bg-slate-800 px-4 py-3 text-left font-semibold text-white hover:bg-slate-900", children: "Review Critical Cases" })] })] })] })] })] }));
}
