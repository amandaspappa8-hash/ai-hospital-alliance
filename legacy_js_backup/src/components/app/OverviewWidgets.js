import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, } from "recharts";
const visitors = [
    { d: "Mon", v: 120 },
    { d: "Tue", v: 160 },
    { d: "Wed", v: 140 },
    { d: "Thu", v: 220 },
    { d: "Fri", v: 180 },
    { d: "Sat", v: 260 },
    { d: "Sun", v: 240 },
];
const recent = [
    { id: "P-10291", name: "Patient A", dept: "Cardiology", status: "In Review" },
    { id: "P-10274", name: "Patient B", dept: "Radiology", status: "Completed" },
    { id: "P-10260", name: "Patient C", dept: "ER", status: "Pending" },
    { id: "P-10241", name: "Patient D", dept: "Lab", status: "In Review" },
];
export function OverviewChart() {
    return (_jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-sm", children: "Visitors Statistics" }) }), _jsx(CardContent, { className: "h-56", children: _jsx(ResponsiveContainer, { width: "100%", height: "100%", children: _jsxs(LineChart, { data: visitors, children: [_jsx(XAxis, { dataKey: "d", tickLine: false, axisLine: false }), _jsx(YAxis, { tickLine: false, axisLine: false, width: 30 }), _jsx(Tooltip, {}), _jsx(Line, { type: "monotone", dataKey: "v", strokeWidth: 2, dot: false })] }) }) })] }));
}
export function RecentActivity() {
    return (_jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-sm", children: "Recent Activity" }) }), _jsxs(CardContent, { className: "text-sm", children: [_jsxs("div", { className: "grid grid-cols-4 gap-2 pb-2 font-medium text-muted-foreground", children: [_jsx("div", { children: "ID" }), _jsx("div", { children: "Name" }), _jsx("div", { children: "Department" }), _jsx("div", { children: "Status" })] }), _jsx("div", { className: "space-y-2", children: recent.map((r) => (_jsxs("div", { className: "grid grid-cols-4 gap-2 items-center", children: [_jsx("div", { className: "font-mono text-xs", children: r.id }), _jsx("div", { children: r.name }), _jsx("div", { className: "text-muted-foreground", children: r.dept }), _jsx("div", { children: _jsx(Badge, { variant: r.status === "Completed" ? "default" : "secondary", children: r.status }) })] }, r.id))) })] })] }));
}
