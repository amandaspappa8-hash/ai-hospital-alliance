import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
const PATIENTS = [
    { id: "P-10291", name: "Sarah Jones", department: "Cardiology", status: "in_care", age: 52, phone: "+218 91 000 0001", lastVisit: "2026-02-14" },
    { id: "P-10274", name: "John Smith", department: "Neurology", status: "waiting", age: 61, phone: "+218 92 000 0002", lastVisit: "2026-02-13" },
    { id: "P-10260", name: "Emily Brown", department: "Orthopedics", status: "discharged", age: 37, phone: "+218 93 000 0003", lastVisit: "2026-02-10" },
    { id: "P-10241", name: "Patient A", department: "Radiology", status: "in_care", age: 45, phone: "+218 94 000 0004", lastVisit: "2026-02-15" },
    { id: "P-10211", name: "Patient B", department: "ER", status: "waiting", age: 29, phone: "+218 95 000 0005", lastVisit: "2026-02-15" },
    { id: "P-10198", name: "Patient C", department: "Lab", status: "in_care", age: 70, phone: "+218 96 000 0006", lastVisit: "2026-02-12" },
];
function statusBadge(status) {
    switch (status) {
        case "in_care":
            return _jsx(Badge, { children: "In care" });
        case "waiting":
            return _jsx(Badge, { variant: "secondary", children: "Waiting" });
        case "discharged":
            return _jsx(Badge, { variant: "outline", children: "Discharged" });
    }
}
export default function PatientsPage() {
    const [q, setQ] = useState("");
    const [dept, setDept] = useState("all");
    const [status, setStatus] = useState("all");
    const [open, setOpen] = useState(false);
    const [selected, setSelected] = useState(null);
    const rows = useMemo(() => {
        const query = q.trim().toLowerCase();
        return PATIENTS.filter((p) => {
            const matchesQuery = !query ||
                p.name.toLowerCase().includes(query) ||
                p.id.toLowerCase().includes(query) ||
                p.phone.toLowerCase().includes(query);
            const matchesDept = dept === "all" ? true : p.department === dept;
            const matchesStatus = status === "all" ? true : p.status === status;
            return matchesQuery && matchesDept && matchesStatus;
        });
    }, [q, dept, status]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-start justify-between gap-4", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: "Patients" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Search, filter, and open patient details." })] }), _jsx(Button, { onClick: () => {
                            setSelected({
                                id: "NEW",
                                name: "New Patient",
                                department: "ER",
                                status: "waiting",
                                age: 0,
                                phone: "",
                                lastVisit: new Date().toISOString().slice(0, 10),
                            });
                            setOpen(true);
                        }, children: "+ New Patient" })] }), _jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-base", children: "Patients list" }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "flex flex-col gap-3 md:flex-row md:items-center", children: [_jsx("div", { className: "flex-1", children: _jsx(Input, { value: q, onChange: (e) => setQ(e.target.value), placeholder: "Search by name, ID, phone..." }) }), _jsxs("div", { className: "flex gap-2", children: [_jsxs(Select, { value: dept, onValueChange: (v) => setDept(v), children: [_jsx(SelectTrigger, { className: "w-[180px]", children: _jsx(SelectValue, { placeholder: "Department" }) }), _jsxs(SelectContent, { children: [_jsx(SelectItem, { value: "all", children: "All departments" }), _jsx(SelectItem, { value: "Cardiology", children: "Cardiology" }), _jsx(SelectItem, { value: "Neurology", children: "Neurology" }), _jsx(SelectItem, { value: "Orthopedics", children: "Orthopedics" }), _jsx(SelectItem, { value: "ER", children: "ER" }), _jsx(SelectItem, { value: "Radiology", children: "Radiology" }), _jsx(SelectItem, { value: "Lab", children: "Lab" })] })] }), _jsxs(Select, { value: status, onValueChange: (v) => setStatus(v), children: [_jsx(SelectTrigger, { className: "w-[160px]", children: _jsx(SelectValue, { placeholder: "Status" }) }), _jsxs(SelectContent, { children: [_jsx(SelectItem, { value: "all", children: "All statuses" }), _jsx(SelectItem, { value: "in_care", children: "In care" }), _jsx(SelectItem, { value: "waiting", children: "Waiting" }), _jsx(SelectItem, { value: "discharged", children: "Discharged" })] })] })] })] }), _jsx(Separator, {}), _jsx("div", { className: "rounded-xl border", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { className: "w-[120px]", children: "ID" }), _jsx(TableHead, { children: "Name" }), _jsx(TableHead, { children: "Department" }), _jsx(TableHead, { children: "Status" }), _jsx(TableHead, { className: "text-right", children: "Action" })] }) }), _jsxs(TableBody, { children: [rows.map((p) => (_jsxs(TableRow, { children: [_jsx(TableCell, { className: "font-medium", children: p.id }), _jsx(TableCell, { children: p.name }), _jsx(TableCell, { className: "text-muted-foreground", children: p.department }), _jsx(TableCell, { children: statusBadge(p.status) }), _jsx(TableCell, { className: "text-right", children: _jsx(Button, { variant: "outline", size: "sm", onClick: () => {
                                                                    setSelected(p);
                                                                    setOpen(true);
                                                                }, children: "Open" }) })] }, p.id))), rows.length === 0 && (_jsx(TableRow, { children: _jsx(TableCell, { colSpan: 5, className: "py-10 text-center text-muted-foreground", children: "No results." }) }))] })] }) })] })] }), _jsx(Sheet, { open: open, onOpenChange: setOpen, children: _jsxs(SheetContent, { className: "w-full sm:max-w-lg", children: [_jsx(SheetHeader, { children: _jsx(SheetTitle, { children: "Patient details" }) }), _jsxs("div", { className: "mt-6 space-y-4", children: [_jsxs("div", { className: "grid grid-cols-2 gap-3", children: [_jsxs("div", { className: "space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "ID" }), _jsx("div", { className: "font-medium", children: selected?.id ?? "-" })] }), _jsxs("div", { className: "space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Status" }), _jsx("div", { children: selected ? statusBadge(selected.status) : "-" })] }), _jsxs("div", { className: "space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Name" }), _jsx("div", { className: "font-medium", children: selected?.name ?? "-" })] }), _jsxs("div", { className: "space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Department" }), _jsx("div", { className: "font-medium", children: selected?.department ?? "-" })] }), _jsxs("div", { className: "space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Age" }), _jsx("div", { className: "font-medium", children: selected?.age ?? "-" })] }), _jsxs("div", { className: "space-y-1", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Phone" }), _jsx("div", { className: "font-medium", children: selected?.phone ?? "-" })] })] }), _jsx(Separator, {}), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-sm font-semibold", children: "Notes" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "This is a UI template. Next: connect real patient profile + visits + documents." })] }), _jsxs("div", { className: "flex gap-2 pt-2", children: [_jsx(Button, { className: "flex-1", children: "Save" }), _jsx(Button, { variant: "outline", className: "flex-1", onClick: () => setOpen(false), children: "Close" })] })] })] }) })] }));
}
