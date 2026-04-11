import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { createOrder, listOrders } from "@/lib/imaging-store";
export default function ImagingOrdersPage() {
    const [patientId, setPatientId] = useState("P-10023");
    const [patientName, setPatientName] = useState("Demo Patient");
    const [modality, setModality] = useState("");
    const [studyDescription, setStudyDescription] = useState("Chest imaging");
    const [priority, setPriority] = useState("ROUTINE");
    const [tick, setTick] = useState(0);
    const orders = useMemo(() => {
        void tick;
        return listOrders();
    }, [tick]);
    function submit() {
        if (!modality)
            return;
        createOrder({
            patientId,
            patientName,
            modality,
            studyDescription,
            priority,
        });
        setTick((t) => t + 1);
    }
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: "Imaging Orders" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Create orders for MRI/CT/US/X-ray and physiologic tests (ECG/EEG). Demo store now \u2014 later DICOM/HL7." })] }), _jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base", children: "Create order" }) }), _jsxs(CardContent, { className: "grid gap-4 md:grid-cols-6", children: [_jsxs("div", { className: "space-y-2 md:col-span-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Patient Name" }), _jsx(Input, { value: patientName, onChange: (e) => setPatientName(e.target.value) })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Patient ID" }), _jsx(Input, { value: patientId, onChange: (e) => setPatientId(e.target.value) })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Modality" }), _jsxs(Select, { onValueChange: (v) => setModality(v), children: [_jsx(SelectTrigger, { children: _jsx(SelectValue, { placeholder: "Choose..." }) }), _jsxs(SelectContent, { children: [_jsx(SelectItem, { value: "XRAY", children: "X-Ray" }), _jsx(SelectItem, { value: "CT", children: "CT" }), _jsx(SelectItem, { value: "MRI", children: "MRI" }), _jsx(SelectItem, { value: "ULTRASOUND", children: "Ultrasound" }), _jsx(SelectItem, { value: "ECG", children: "ECG" }), _jsx(SelectItem, { value: "EEG", children: "EEG" }), _jsx(SelectItem, { value: "PET", children: "PET" })] })] })] }), _jsxs("div", { className: "space-y-2 md:col-span-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Study Description" }), _jsx(Input, { value: studyDescription, onChange: (e) => setStudyDescription(e.target.value) })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Priority" }), _jsxs(Select, { onValueChange: (v) => setPriority(v), defaultValue: "ROUTINE", children: [_jsx(SelectTrigger, { children: _jsx(SelectValue, {}) }), _jsxs(SelectContent, { children: [_jsx(SelectItem, { value: "ROUTINE", children: "Routine" }), _jsx(SelectItem, { value: "URGENT", children: "Urgent" })] })] })] }), _jsx("div", { className: "flex items-end", children: _jsx(Button, { className: "w-full", onClick: submit, disabled: !modality, children: "Send Order" }) })] })] }), _jsxs(Card, { className: "rounded-2xl", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between", children: [_jsx(CardTitle, { className: "text-base", children: "Orders Queue" }), _jsxs(Badge, { variant: "secondary", children: [orders.length, " orders"] })] }), _jsxs(CardContent, { children: [_jsx("div", { className: "rounded-xl border", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { children: "Patient" }), _jsx(TableHead, { children: "Modality" }), _jsx(TableHead, { children: "Description" }), _jsx(TableHead, { children: "Priority" }), _jsx(TableHead, { children: "Status" }), _jsx(TableHead, { children: "Created" })] }) }), _jsxs(TableBody, { children: [orders.map((o) => (_jsxs(TableRow, { children: [_jsxs(TableCell, { className: "font-medium", children: [o.patientName, _jsx("div", { className: "text-xs text-muted-foreground", children: o.patientId })] }), _jsx(TableCell, { children: o.modality }), _jsx(TableCell, { className: "text-sm", children: o.studyDescription }), _jsx(TableCell, { children: _jsx(Badge, { variant: o.priority === "URGENT" ? "destructive" : "secondary", children: o.priority }) }), _jsx(TableCell, { children: o.status }), _jsx(TableCell, { className: "text-xs text-muted-foreground", children: new Date(o.createdAt).toLocaleString() })] }, o.id))), orders.length === 0 ? (_jsx(TableRow, { children: _jsx(TableCell, { colSpan: 6, className: "text-sm text-muted-foreground", children: "No orders yet. Create one above." }) })) : null] })] }) }), _jsx("div", { className: "mt-3 text-xs text-muted-foreground", children: "Next: we will push orders to real devices using DICOM MWL (imaging) and HL7 ORU (ECG/EEG results)." })] })] })] }));
}
