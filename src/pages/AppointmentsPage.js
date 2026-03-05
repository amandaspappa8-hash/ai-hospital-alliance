import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
const APPTS = [
    { id: "A-9001", patient: "Sarah Jones", doctor: "Dr. Priscilla", department: "Cardiology", date: "2026-02-15", time: "10:30", status: "upcoming" },
    { id: "A-9002", patient: "John Smith", doctor: "Dr. Cooper", department: "Neurology", date: "2026-02-15", time: "12:00", status: "upcoming" },
    { id: "A-8990", patient: "Emily Brown", doctor: "Dr. Lane", department: "Orthopedics", date: "2026-02-12", time: "09:00", status: "completed" },
    { id: "A-8988", patient: "Patient B", doctor: "Dr. Kumar", department: "ER", date: "2026-02-11", time: "15:15", status: "cancelled" },
];
function apptBadge(s) {
    if (s === "upcoming")
        return _jsx(Badge, { children: "Upcoming" });
    if (s === "completed")
        return _jsx(Badge, { variant: "secondary", children: "Completed" });
    return _jsx(Badge, { variant: "outline", children: "Cancelled" });
}
export default function AppointmentsPage() {
    const [tab, setTab] = useState("list");
    const [q, setQ] = useState("");
    const [status, setStatus] = useState("all");
    const [date, setDate] = useState(new Date());
    const rows = useMemo(() => {
        const query = q.trim().toLowerCase();
        return APPTS.filter((a) => {
            const matchesQuery = !query ||
                a.patient.toLowerCase().includes(query) ||
                a.doctor.toLowerCase().includes(query) ||
                a.id.toLowerCase().includes(query);
            const matchesStatus = status === "all" ? true : a.status === status;
            return matchesQuery && matchesStatus;
        });
    }, [q, status]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-start justify-between gap-4", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: "Appointments" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "List + Calendar view, with create dialog." })] }), _jsxs(Dialog, { children: [_jsx(DialogTrigger, { asChild: true, children: _jsx(Button, { children: "+ New appointment" }) }), _jsxs(DialogContent, { className: "sm:max-w-lg", children: [_jsx(DialogHeader, { children: _jsx(DialogTitle, { children: "Create appointment" }) }), _jsxs("div", { className: "grid gap-3", children: [_jsx(Input, { placeholder: "Patient name" }), _jsx(Input, { placeholder: "Doctor name" }), _jsxs("div", { className: "grid grid-cols-2 gap-2", children: [_jsx(Input, { placeholder: "Date (YYYY-MM-DD)" }), _jsx(Input, { placeholder: "Time (HH:mm)" })] }), _jsxs(Select, { defaultValue: "upcoming", children: [_jsx(SelectTrigger, { children: _jsx(SelectValue, { placeholder: "Status" }) }), _jsxs(SelectContent, { children: [_jsx(SelectItem, { value: "upcoming", children: "Upcoming" }), _jsx(SelectItem, { value: "completed", children: "Completed" }), _jsx(SelectItem, { value: "cancelled", children: "Cancelled" })] })] }), _jsxs("div", { className: "flex gap-2 pt-2", children: [_jsx(Button, { className: "flex-1", children: "Save" }), _jsx(Button, { variant: "outline", className: "flex-1", children: "Cancel" })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: "Demo UI only \u2014 next step: connect API + validation + RBAC." })] })] })] })] }), _jsxs(Tabs, { value: tab, onValueChange: (v) => setTab(v), children: [_jsxs(TabsList, { children: [_jsx(TabsTrigger, { value: "list", children: "List" }), _jsx(TabsTrigger, { value: "calendar", children: "Calendar" })] }), _jsx(TabsContent, { value: "list", className: "mt-4", children: _jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-base", children: "Appointments" }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "flex flex-col gap-3 md:flex-row md:items-center", children: [_jsx("div", { className: "flex-1", children: _jsx(Input, { value: q, onChange: (e) => setQ(e.target.value), placeholder: "Search by patient, doctor, ID..." }) }), _jsxs(Select, { value: status, onValueChange: (v) => setStatus(v), children: [_jsx(SelectTrigger, { className: "w-[180px]", children: _jsx(SelectValue, { placeholder: "Status" }) }), _jsxs(SelectContent, { children: [_jsx(SelectItem, { value: "all", children: "All statuses" }), _jsx(SelectItem, { value: "upcoming", children: "Upcoming" }), _jsx(SelectItem, { value: "completed", children: "Completed" }), _jsx(SelectItem, { value: "cancelled", children: "Cancelled" })] })] })] }), _jsx("div", { className: "rounded-xl border", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { className: "w-[110px]", children: "ID" }), _jsx(TableHead, { children: "Patient" }), _jsx(TableHead, { children: "Doctor" }), _jsx(TableHead, { children: "Date" }), _jsx(TableHead, { children: "Time" }), _jsx(TableHead, { children: "Status" })] }) }), _jsxs(TableBody, { children: [rows.map((a) => (_jsxs(TableRow, { children: [_jsx(TableCell, { className: "font-medium", children: a.id }), _jsx(TableCell, { children: a.patient }), _jsx(TableCell, { className: "text-muted-foreground", children: a.doctor }), _jsx(TableCell, { children: a.date }), _jsx(TableCell, { children: a.time }), _jsx(TableCell, { children: apptBadge(a.status) })] }, a.id))), rows.length === 0 && (_jsx(TableRow, { children: _jsx(TableCell, { colSpan: 6, className: "py-10 text-center text-muted-foreground", children: "No results." }) }))] })] }) })] })] }) }), _jsx(TabsContent, { value: "calendar", className: "mt-4", children: _jsxs("div", { className: "grid gap-4 lg:grid-cols-3", children: [_jsxs(Card, { className: "rounded-2xl lg:col-span-1", children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-base", children: "Pick a date" }) }), _jsx(CardContent, { children: _jsx(Calendar, { mode: "single", selected: date, onSelect: setDate }) })] }), _jsxs(Card, { className: "rounded-2xl lg:col-span-2", children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-base", children: "Day schedule" }) }), _jsx(CardContent, { className: "text-sm text-muted-foreground", children: "Demo: connect selected date to real schedule list + time slots." })] })] }) })] })] }));
}
