import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
const REPORTS = [
    { id: "R-7711", title: "CT Head", patient: "Patient A", type: "Radiology", status: "in_review", updated: "Today" },
    { id: "R-7709", title: "CBC Panel", patient: "Patient C", type: "Lab", status: "pending", updated: "Yesterday" },
    { id: "R-7701", title: "Discharge Summary", patient: "Emily Brown", type: "Discharge", status: "completed", updated: "3d ago" },
    { id: "R-7688", title: "ER Triage", patient: "Patient B", type: "ER", status: "pending", updated: "1w ago" },
];
function rBadge(s) {
    if (s === "pending")
        return _jsx(Badge, { variant: "secondary", children: "Pending" });
    if (s === "in_review")
        return _jsx(Badge, { children: "In review" });
    return _jsx(Badge, { variant: "outline", children: "Completed" });
}
export default function ReportsPage() {
    const [tab, setTab] = useState("all");
    const [q, setQ] = useState("");
    const rows = useMemo(() => {
        const query = q.trim().toLowerCase();
        return REPORTS.filter((r) => {
            const matchesQuery = !query ||
                r.title.toLowerCase().includes(query) ||
                r.patient.toLowerCase().includes(query) ||
                r.id.toLowerCase().includes(query);
            const matchesTab = tab === "all" ? true : tab === "pending" ? r.status !== "completed" : r.status === "completed";
            return matchesQuery && matchesTab;
        });
    }, [q, tab]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-start justify-between gap-4", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: "Reports" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Reports queue with quick actions." })] }), _jsx(Button, { variant: "outline", children: "Export" })] }), _jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { className: "pb-3", children: _jsx(CardTitle, { className: "text-base", children: "Reports" }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "flex flex-col gap-3 md:flex-row md:items-center md:justify-between", children: [_jsx("div", { className: "w-full md:max-w-sm", children: _jsx(Input, { value: q, onChange: (e) => setQ(e.target.value), placeholder: "Search reports..." }) }), _jsxs(Tabs, { value: tab, onValueChange: (v) => setTab(v), children: [_jsxs(TabsList, { children: [_jsx(TabsTrigger, { value: "all", children: "All" }), _jsx(TabsTrigger, { value: "pending", children: "Pending" }), _jsx(TabsTrigger, { value: "completed", children: "Completed" })] }), _jsx(TabsContent, { value: tab })] })] }), _jsx("div", { className: "rounded-xl border", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { className: "w-[110px]", children: "ID" }), _jsx(TableHead, { children: "Title" }), _jsx(TableHead, { children: "Patient" }), _jsx(TableHead, { children: "Type" }), _jsx(TableHead, { children: "Status" }), _jsx(TableHead, { className: "text-right", children: "Actions" })] }) }), _jsxs(TableBody, { children: [rows.map((r) => (_jsxs(TableRow, { children: [_jsx(TableCell, { className: "font-medium", children: r.id }), _jsx(TableCell, { children: r.title }), _jsx(TableCell, { className: "text-muted-foreground", children: r.patient }), _jsx(TableCell, { children: r.type }), _jsx(TableCell, { children: rBadge(r.status) }), _jsx(TableCell, { className: "text-right", children: _jsxs(DropdownMenu, { children: [_jsx(DropdownMenuTrigger, { asChild: true, children: _jsx(Button, { size: "sm", variant: "outline", children: "Menu" }) }), _jsxs(DropdownMenuContent, { align: "end", children: [_jsx(DropdownMenuItem, { children: "Open" }), _jsx(DropdownMenuItem, { children: "Assign reviewer" }), _jsx(DropdownMenuItem, { children: "Mark completed" })] })] }) })] }, r.id))), rows.length === 0 && (_jsx(TableRow, { children: _jsx(TableCell, { colSpan: 6, className: "py-10 text-center text-muted-foreground", children: "No results." }) }))] })] }) })] })] })] }));
}
