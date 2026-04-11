import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { OverviewChart, RecentActivity } from "@/components/app/OverviewWidgets";
export default function OverviewPage() {
    const stats = [
        { title: "Total Patients", value: "2,420" },
        { title: "New Appointments", value: "226" },
        { title: "Pending Reports", value: "193" },
        { title: "Bed Occupancy", value: "78%" },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: "Overview" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Hospital operations snapshot." })] }), _jsx("div", { className: "grid gap-4 sm:grid-cols-2 lg:grid-cols-4", children: stats.map((s) => (_jsxs(Card, { className: "rounded-2xl", children: [_jsx(CardHeader, { className: "pb-2", children: _jsx(CardTitle, { className: "text-sm text-muted-foreground", children: s.title }) }), _jsx(CardContent, { className: "text-2xl font-bold", children: s.value })] }, s.title))) }), _jsxs("div", { className: "grid gap-4 lg:grid-cols-3", children: [_jsx("div", { className: "lg:col-span-2", children: _jsx(OverviewChart, {}) }), _jsx(RecentActivity, {})] })] }));
}
