import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import { findDrugById, getInteractionsForDrugIds, searchDrugs, } from "@/lib/formulary";
function severityBadgeVariant(sev) {
    if (sev === "major")
        return "destructive";
    if (sev === "moderate")
        return "default";
    return "secondary";
}
export default function PrescriptionsPage() {
    // patient demo context
    const [patient, setPatient] = useState({
        age: 54,
        allergies: ["penicillin"],
        eGFR: 42,
        diabetes: true,
        pregnancy: false,
    });
    // drug search
    const [q, setQ] = useState("");
    const results = useMemo(() => searchDrugs(q), [q]);
    // rx lines
    const [rx, setRx] = useState([]);
    const drugIds = useMemo(() => rx.map((r) => r.drugId), [rx]);
    const interactionFindings = useMemo(() => getInteractionsForDrugIds(drugIds), [drugIds]);
    // clinical flags (simple demo rules)
    const flags = useMemo(() => {
        const out = [];
        for (const line of rx) {
            const d = findDrugById(line.drugId);
            if (!d)
                continue;
            // allergy demo
            if ((patient.allergies ?? []).some((a) => a.toLowerCase().includes("penicillin"))) {
                if ((d.tags ?? []).includes("beta-lactam")) {
                    out.push({
                        severity: "major",
                        title: "Allergy risk",
                        detail: `${d.name}: patient allergy includes "penicillin" (demo).`,
                    });
                }
            }
            // renal demo
            if (typeof patient.eGFR === "number" && patient.eGFR < 45) {
                if (d.renalAdjust) {
                    out.push({
                        severity: "moderate",
                        title: "Renal adjustment",
                        detail: `${d.name}: ${d.renalAdjust} (patient eGFR ${patient.eGFR}).`,
                    });
                }
            }
            // pregnancy demo
            if (patient.pregnancy) {
                if (d.pregnancy === "D" || d.pregnancy === "X") {
                    out.push({
                        severity: "major",
                        title: "Pregnancy warning",
                        detail: `${d.name}: pregnancy category ${d.pregnancy} (demo).`,
                    });
                }
            }
        }
        // add interaction findings as flags too
        for (const itx of interactionFindings) {
            const a = findDrugById(itx.a)?.name ?? itx.a;
            const b = findDrugById(itx.b)?.name ?? itx.b;
            out.push({
                severity: itx.severity,
                title: `Interaction: ${a} + ${b}`,
                detail: `${itx.summary} — ${itx.recommendation}`,
            });
        }
        // de-dup by title+detail
        const keySet = new Set();
        return out.filter((x) => {
            const k = `${x.title}|${x.detail}`;
            if (keySet.has(k))
                return false;
            keySet.add(k);
            return true;
        });
    }, [rx, patient, interactionFindings]);
    function addDrug(d) {
        setRx((prev) => {
            if (prev.some((x) => x.drugId === d.id))
                return prev;
            return [
                ...prev,
                {
                    drugId: d.id,
                    dose: d.strength ?? "",
                    frequency: "BID",
                    duration: "5 days",
                    notes: "",
                },
            ];
        });
    }
    function updateLine(idx, patch) {
        setRx((prev) => prev.map((x, i) => (i === idx ? { ...x, ...patch } : x)));
    }
    function removeLine(idx) {
        setRx((prev) => prev.filter((_, i) => i !== idx));
    }
    const exportJson = useMemo(() => {
        return JSON.stringify({
            patient,
            prescription: rx.map((r) => ({
                ...r,
                drug: findDrugById(r.drugId),
            })),
            safety: {
                flags,
            },
            meta: {
                createdAt: new Date().toISOString(),
                version: "demo-1",
            },
        }, null, 2);
    }, [patient, rx, flags]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: "Smart Prescriptions" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Create prescriptions linked to the hospital formulary, with safety checks (demo)." })] }), _jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base", children: "Patient context (demo)" }) }), _jsxs(CardContent, { className: "grid gap-4 md:grid-cols-5", children: [_jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Age" }), _jsx(Input, { value: patient.age ?? "", onChange: (e) => setPatient((p) => ({ ...p, age: Number(e.target.value || 0) })), placeholder: "e.g. 54" })] }), _jsxs("div", { className: "space-y-2 md:col-span-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Allergies (comma separated)" }), _jsx(Input, { value: (patient.allergies ?? []).join(", "), onChange: (e) => setPatient((p) => ({
                                            ...p,
                                            allergies: e.target.value
                                                .split(",")
                                                .map((s) => s.trim())
                                                .filter(Boolean),
                                        })), placeholder: "e.g. penicillin, latex" })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "eGFR" }), _jsx(Input, { value: patient.eGFR ?? "", onChange: (e) => setPatient((p) => ({ ...p, eGFR: Number(e.target.value || 0) })), placeholder: "e.g. 42" })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Diabetes (true/false)" }), _jsx(Input, { value: String(!!patient.diabetes), onChange: (e) => setPatient((p) => ({ ...p, diabetes: e.target.value === "true" })), placeholder: "true" })] })] })] }), _jsxs("div", { className: "grid gap-6 lg:grid-cols-2", children: [_jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base", children: "Add from Formulary" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsx(Input, { value: q, onChange: (e) => setQ(e.target.value), placeholder: "Search drugs (name / generic / strength / ATC)..." }), _jsx("div", { className: "rounded-xl border", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { children: "Drug" }), _jsx(TableHead, { children: "Route" }), _jsx(TableHead, { className: "w-[120px]" })] }) }), _jsxs(TableBody, { children: [results.slice(0, 10).map((d) => (_jsxs(TableRow, { children: [_jsxs(TableCell, { className: "font-medium", children: [d.name, _jsxs("div", { className: "text-xs text-muted-foreground", children: [(d.strength ?? "").trim(), " ", (d.form ?? "").trim()] })] }), _jsx(TableCell, { className: "text-xs", children: d.route }), _jsx(TableCell, { className: "text-right", children: _jsx(Button, { size: "sm", onClick: () => addDrug(d), children: "Add" }) })] }, d.id))), results.length === 0 ? (_jsx(TableRow, { children: _jsx(TableCell, { colSpan: 3, className: "text-sm text-muted-foreground", children: "No matches." }) })) : null] })] }) }), _jsx("div", { className: "text-xs text-muted-foreground", children: "Tip: Later we connect to national drug database + hospital rules + insurance formulary." })] })] }), _jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base", children: "Safety checks" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: flags.some((f) => f.severity === "major") ? "destructive" : "secondary", children: [flags.length, " findings"] }), _jsx("span", { className: "text-xs text-muted-foreground", children: "Demo rules: allergy / renal / pregnancy + drug\u2013drug interactions" })] }), _jsx("div", { className: "space-y-2", children: flags.length === 0 ? (_jsx("div", { className: "text-sm text-muted-foreground", children: "No warnings detected (demo)." })) : (flags.map((f, idx) => (_jsxs("div", { className: "rounded-xl border p-3", children: [_jsxs("div", { className: "flex items-center justify-between gap-3", children: [_jsx("div", { className: "font-medium", children: f.title }), _jsx(Badge, { variant: severityBadgeVariant(f.severity), children: f.severity })] }), _jsx("div", { className: "mt-1 text-sm text-muted-foreground", children: f.detail })] }, idx)))) })] })] })] }), _jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base", children: "Prescription" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsx("div", { className: "rounded-xl border", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { children: "Drug" }), _jsx(TableHead, { children: "Dose" }), _jsx(TableHead, { children: "Frequency" }), _jsx(TableHead, { children: "Duration" }), _jsx(TableHead, { children: "Notes" }), _jsx(TableHead, { className: "w-[80px]" })] }) }), _jsxs(TableBody, { children: [rx.map((line, idx) => {
                                                    const d = findDrugById(line.drugId);
                                                    return (_jsxs(TableRow, { children: [_jsxs(TableCell, { className: "font-medium", children: [d?.name ?? line.drugId, _jsxs("div", { className: "text-xs text-muted-foreground", children: [d?.strength ?? "", " ", d?.form ?? "", " \u2022 ", d?.route ?? ""] })] }), _jsx(TableCell, { children: _jsx(Input, { value: line.dose, onChange: (e) => updateLine(idx, { dose: e.target.value }) }) }), _jsx(TableCell, { children: _jsx(Input, { value: line.frequency, onChange: (e) => updateLine(idx, { frequency: e.target.value }) }) }), _jsx(TableCell, { children: _jsx(Input, { value: line.duration, onChange: (e) => updateLine(idx, { duration: e.target.value }) }) }), _jsx(TableCell, { children: _jsx(Input, { value: line.notes ?? "", onChange: (e) => updateLine(idx, { notes: e.target.value }) }) }), _jsx(TableCell, { className: "text-right", children: _jsx(Button, { variant: "outline", size: "sm", onClick: () => removeLine(idx), children: "Remove" }) })] }, line.drugId));
                                                }), rx.length === 0 ? (_jsx(TableRow, { children: _jsx(TableCell, { colSpan: 6, className: "text-sm text-muted-foreground", children: "No medications added yet." }) })) : null] })] }) }), _jsxs("div", { className: "grid gap-3 lg:grid-cols-2", children: [_jsxs("div", { children: [_jsx("div", { className: "text-sm font-medium mb-2", children: "Export (JSON)" }), _jsx(Textarea, { value: exportJson, readOnly: true, className: "min-h-[220px] font-mono text-xs" })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("div", { className: "text-sm font-medium", children: "Actions" }), _jsxs("div", { className: "flex flex-wrap gap-2", children: [_jsx(Button, { variant: "default", onClick: () => {
                                                            navigator.clipboard.writeText(exportJson);
                                                        }, children: "Copy JSON" }), _jsx(Button, { variant: "outline", onClick: () => {
                                                            setRx([]);
                                                        }, children: "Clear prescription" })] }), _jsxs("div", { className: "rounded-xl border p-3 text-sm text-muted-foreground", children: [_jsx("div", { className: "font-medium text-foreground", children: "Next upgrade (we will do it):" }), _jsxs("ul", { className: "list-disc pl-5 mt-2 space-y-1", children: [_jsx("li", { children: "ICD/diagnosis \u2192 suggested meds + guidelines" }), _jsx("li", { children: "Dose calculator (weight, age, eGFR, hepatic)" }), _jsx("li", { children: "Real drug DB + national formulary + insurance rules" }), _jsx("li", { children: "PDF print with signature + QR + audit trail" })] })] })] })] })] })] })] }));
}
