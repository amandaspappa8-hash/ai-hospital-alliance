import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import AdminLayout from "@/layouts/AdminLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
const stats = [
    { title: "Total Patients", value: "2,420", hint: "+4.7% / month" },
    { title: "New Appointments", value: "226", hint: "+10.3% / month" },
    { title: "Pending Reports", value: "193", hint: "-2.5% / month" },
    { title: "Active Beds", value: "106", hint: "Stable" },
];
const rows = [
    { id: "A-1021", name: "Sara Ali", dept: "Cardiology", status: "In Review" },
    { id: "A-1022", name: "John Smith", dept: "Neurology", status: "Approved" },
    { id: "A-1023", name: "Mona Omar", dept: "Radiology", status: "Pending" },
    { id: "A-1024", name: "Khaled Noor", dept: "Orthopedics", status: "Approved" },
];
function StatusBadge({ s }) {
    if (s === "Approved")
        return _jsx(Badge, { children: "Approved" });
    if (s === "Pending")
        return _jsx(Badge, { variant: "secondary", children: "Pending" });
    return _jsx(Badge, { variant: "outline", children: "In Review" });
}
export default function Dashboard() {
    return (_jsxs(AdminLayout, { title: "Dashboard", subtitle: "Overview of key hospital metrics", actions: _jsx(Button, { variant: "outline", size: "sm", children: "New" }), children: [_jsx("div", { className: "grid gap-4 md:grid-cols-2 lg:grid-cols-4", children: stats.map((s) => (_jsxs(Card, { children: [_jsx(CardHeader, { className: "pb-2", children: _jsx(CardTitle, { className: "text-sm font-medium text-muted-foreground", children: s.title }) }), _jsxs(CardContent, { children: [_jsx("div", { className: "text-2xl font-semibold", children: s.value }), _jsx("div", { className: "text-xs text-muted-foreground", children: s.hint })] })] }, s.title))) }), _jsxs("div", { className: "mt-6 flex items-center justify-between gap-3", children: [_jsx("div", { className: "text-sm font-medium", children: "Recent Appointments" }), _jsx("div", { className: "w-full max-w-sm", children: _jsx(Input, { placeholder: "Search patient\u2026" }) })] }), _jsx(Separator, { className: "my-4" }), _jsxs(Card, { children: [_jsx(CardHeader, { className: "pb-2", children: _jsx(CardTitle, { className: "text-base", children: "Appointments" }) }), _jsx(CardContent, { children: _jsx("div", { className: "overflow-x-auto", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { className: "w-[120px]", children: "Ref" }), _jsx(TableHead, { children: "Patient" }), _jsx(TableHead, { children: "Department" }), _jsx(TableHead, { className: "text-right", children: "Status" })] }) }), _jsx(TableBody, { children: rows.map((r) => (_jsxs(TableRow, { children: [_jsx(TableCell, { className: "font-medium", children: r.id }), _jsx(TableCell, { children: r.name }), _jsx(TableCell, { className: "text-muted-foreground", children: r.dept }), _jsx(TableCell, { className: "text-right", children: _jsx(StatusBadge, { s: r.status }) })] }, r.id))) })] }) }) })] })] }));
}
