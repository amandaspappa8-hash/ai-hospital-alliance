import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
export default function LabsPage() {
    const [patients, setPatients] = useState([]);
    const [selectedPatientId, setSelectedPatientId] = useState("");
    const [orders, setOrders] = useState([]);
    const [catalog, setCatalog] = useState({});
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [form, setForm] = useState({
        section: "classical",
        tests: "",
        priority: "Routine",
    });
    const [selectedTests, setSelectedTests] = useState([]);
    const [labSearch, setLabSearch] = useState("");
    const [activeTab, setActiveTab] = useState("catalog");
    const [ordersStatusFilter, setOrdersStatusFilter] = useState("all");
    const [resultsFilter, setResultsFilter] = useState("all");
    const [resultsSearch, setResultsSearch] = useState("");
    useEffect(() => {
        setForm((prev) => ({
            ...prev,
            tests: selectedTests.join(", "),
        }));
    }, [selectedTests]);
    useEffect(() => {
        if (!successMessage)
            return;
        const t = setTimeout(() => setSuccessMessage(""), 2500);
        return () => clearTimeout(t);
    }, [successMessage]);
    useEffect(() => {
        Promise.all([apiGet("/patients"), apiGet("/labs/catalog"), apiGet("/labs/orders")])
            .then(([p, c, o]) => {
            const patientsList = Array.isArray(p) ? p : [];
            setPatients(patientsList);
            if (patientsList.length > 0)
                setSelectedPatientId(patientsList[0].id);
            setCatalog((c || {}));
            setOrders(Array.isArray(o) ? o : []);
        })
            .catch(() => setError("Failed to load laboratory data"));
    }, []);
    const filteredCatalogTests = useMemo(() => {
        const items = catalog[form.section] || [];
        const q = labSearch.trim().toLowerCase();
        if (!q)
            return items;
        return items.filter((test) => test.toLowerCase().includes(q));
    }, [catalog, form.section, labSearch]);
    const selectedPatient = useMemo(() => patients.find((p) => p.id === selectedPatientId), [patients, selectedPatientId]);
    const filteredOrders = useMemo(() => orders.filter((o) => !selectedPatientId || o.patientId === selectedPatientId), [orders, selectedPatientId]);
    const totalOrdersCount = filteredOrders.length;
    const pendingOrdersCount = filteredOrders.filter((order) => order.status === "Pending").length;
    const completedOrdersCount = filteredOrders.filter((order) => order.status === "Completed").length;
    const resultsAvailableCount = filteredOrders.filter((order) => order.result).length;
    const filteredOrdersByStatus = useMemo(() => {
        if (ordersStatusFilter === "all")
            return filteredOrders;
        return filteredOrders.filter((order) => order.status === ordersStatusFilter);
    }, [filteredOrders, ordersStatusFilter]);
    const filteredResults = useMemo(() => {
        let items = [...filteredOrders];
        if (resultsFilter === "has_result") {
            items = items.filter((order) => order.result);
        }
        else if (resultsFilter === "no_result") {
            items = items.filter((order) => !order.result);
        }
        const q = resultsSearch.trim().toLowerCase();
        if (q) {
            items = items.filter((order) => order.tests.some((test) => test.toLowerCase().includes(q)));
        }
        return items;
    }, [filteredOrders, resultsFilter, resultsSearch]);
    const copySelectedTests = async () => {
        try {
            if (selectedTests.length === 0)
                return;
            await navigator.clipboard.writeText(selectedTests.join(", "));
            setSuccessMessage("Selected tests copied to clipboard");
        }
        catch {
            setError("Failed to copy selected tests");
        }
    };
    const downloadFile = (filename, content, mimeType) => {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };
    const exportSelectedAsTxt = () => {
        if (selectedTests.length === 0)
            return;
        downloadFile(`${form.section}-selected-tests.txt`, selectedTests.join("\n"), "text/plain;charset=utf-8");
        setSuccessMessage("Selected tests exported as TXT");
    };
    const exportSelectedAsCsv = () => {
        if (selectedTests.length === 0)
            return;
        const rows = ["section,test", ...selectedTests.map((test) => `"${form.section}","${test.replace(/"/g, '""')}"`)];
        downloadFile(`${form.section}-selected-tests.csv`, rows.join("\n"), "text/csv;charset=utf-8");
        setSuccessMessage("Selected tests exported as CSV");
    };
    const exportResultsAsTxt = () => {
        if (filteredResults.length === 0)
            return;
        const content = filteredResults
            .map((order) => {
            return [
                `Patient: ${order.patientName}`,
                `Tests: ${order.tests.join(", ")}`,
                `Status: ${order.status}`,
                `Result: ${order.result || "No result entered yet"}`,
                `Section: ${order.section}`,
                `Priority: ${order.priority}`,
                "------------------------------",
            ].join("\n");
        })
            .join("\n");
        const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "lab-results.txt";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        setSuccessMessage("Results exported as TXT");
    };
    const exportResultsAsCsv = () => {
        if (filteredResults.length === 0)
            return;
        const rows = [
            "patientName,tests,status,result,section,priority",
            ...filteredResults.map((order) => [
                `"${order.patientName.replace(/"/g, '""')}"`,
                `"${order.tests.join(" | ").replace(/"/g, '""')}"`,
                `"${order.status.replace(/"/g, '""')}"`,
                `"${(order.result || "No result entered yet").replace(/"/g, '""')}"`,
                `"${order.section.replace(/"/g, '""')}"`,
                `"${order.priority.replace(/"/g, '""')}"`
            ].join(",")),
        ];
        const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "lab-results.csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        setSuccessMessage("Results exported as CSV");
    };
    const printResults = () => {
        if (filteredResults.length === 0)
            return;
        const html = `
      <html>
        <head>
          <title>Lab Results</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 24px; }
            h1 { margin-bottom: 20px; }
            .card { border: 1px solid #ddd; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
            .label { font-weight: bold; }
          </style>
        </head>
        <body>
          <h1>Laboratory Results</h1>
          ${filteredResults.map((order) => `
            <div class="card">
              <div><span class="label">Patient:</span> ${order.patientName}</div>
              <div><span class="label">Tests:</span> ${order.tests.join(", ")}</div>
              <div><span class="label">Status:</span> ${order.status}</div>
              <div><span class="label">Result:</span> ${order.result || "No result entered yet"}</div>
              <div><span class="label">Section:</span> ${order.section}</div>
              <div><span class="label">Priority:</span> ${order.priority}</div>
            </div>
          `).join("")}
        </body>
      </html>
    `;
        const printWindow = window.open("", "_blank");
        if (!printWindow) {
            setError("Failed to open print window");
            return;
        }
        printWindow.document.open();
        printWindow.document.write(html);
        printWindow.document.close();
        printWindow.focus();
        printWindow.print();
        setSuccessMessage("Print view opened");
    };
    const submitOrder = async (e) => {
        e.preventDefault();
        if (!selectedPatient)
            return;
        try {
            await apiPost("/labs/orders", {
                patientId: selectedPatient.id,
                patientName: selectedPatient.name,
                section: form.section,
                tests: form.tests.split(",").map((t) => t.trim()).filter(Boolean),
                priority: form.priority,
                status: "Pending",
            });
            const refreshed = await apiGet("/labs/orders");
            setOrders(Array.isArray(refreshed) ? refreshed : []);
            setForm({
                section: form.section,
                tests: "",
                priority: "Routine",
            });
            setSelectedTests([]);
            setSuccessMessage("Lab order added");
        }
        catch {
            setError("Failed to save lab order");
        }
    };
    return (_jsx("div", { style: pageStyle, children: _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { children: [_jsx("h1", { style: { margin: 0, fontSize: 42, fontWeight: 800 }, children: "Laboratory \u2022 NEW UI \u2022 GLASS ACTIVE" }), _jsx("div", { style: { marginTop: 8, color: "#cbd5e1" }, children: "SMART LABORATORY WORKFLOW \u2022 GLASS ACTIVE" })] }), error && _jsx("div", { style: errorStyle, children: error }), successMessage && _jsx("div", { style: successStyle, children: successMessage }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsx("button", { type: "button", style: tabBtnStyle(activeTab === "catalog"), onClick: () => setActiveTab("catalog"), children: "Catalog" }), _jsx("button", { type: "button", style: tabBtnStyle(activeTab === "selected"), onClick: () => setActiveTab("selected"), children: "Selected Tests" }), _jsx("button", { type: "button", style: tabBtnStyle(activeTab === "orders"), onClick: () => setActiveTab("orders"), children: "Orders" }), _jsx("button", { type: "button", style: tabBtnStyle(activeTab === "results"), onClick: () => setActiveTab("results"), children: "Results" })] }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsxs("div", { style: itemStyle, children: [_jsx("strong", { children: "Total Orders:" }), " ", totalOrdersCount] }), _jsxs("div", { style: itemStyle, children: [_jsx("strong", { children: "Pending:" }), " ", pendingOrdersCount] }), _jsxs("div", { style: itemStyle, children: [_jsx("strong", { children: "Completed:" }), " ", completedOrdersCount] }), _jsxs("div", { style: itemStyle, children: [_jsx("strong", { children: "Results Available:" }), " ", resultsAvailableCount] })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1.1fr 2fr", gap: 20 }, children: [_jsxs("div", { style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Patients" }), _jsx("div", { style: { display: "grid", gap: 14 }, children: patients.map((patient) => (_jsxs("button", { onClick: () => setSelectedPatientId(patient.id), style: {
                                            ...itemStyle,
                                            textAlign: "left",
                                            cursor: "pointer",
                                            border: selectedPatientId === patient.id
                                                ? "1px solid rgba(56,189,248,0.95)"
                                                : "1px solid rgba(148,163,184,0.22)",
                                        }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: patient.name }), _jsx("div", { style: { marginTop: 6, color: "#cbd5e1" }, children: patient.id }), _jsxs("div", { style: { marginTop: 6, color: "#e2e8f0" }, children: [patient.department ?? "General", " \u2022 ", patient.condition ?? "-"] })] }, patient.id))) })] }), _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Selected Patient" }), selectedPatient ? (_jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Name:" }), " ", selectedPatient.name] }), _jsxs("div", { children: [_jsx("strong", { children: "ID:" }), " ", selectedPatient.id] }), _jsxs("div", { children: [_jsx("strong", { children: "Department:" }), " ", selectedPatient.department ?? "-"] }), _jsxs("div", { children: [_jsx("strong", { children: "Status:" }), " ", selectedPatient.status ?? "-"] }), _jsxs("div", { style: { gridColumn: "1 / -1" }, children: [_jsx("strong", { children: "Condition:" }), " ", selectedPatient.condition ?? "-"] })] })) : (_jsx("div", { children: "No patient selected" }))] }), activeTab === "catalog" && (_jsxs("form", { onSubmit: submitOrder, style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Create Lab Order" }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10, marginBottom: 14 }, children: Object.keys(catalog).map((section) => (_jsx("button", { type: "button", onClick: () => {
                                                    setForm({ ...form, section });
                                                    setSelectedTests([]);
                                                    setLabSearch("");
                                                }, style: {
                                                    ...itemStyle,
                                                    cursor: "pointer",
                                                    textTransform: "capitalize",
                                                    border: form.section === section
                                                        ? "1px solid rgba(56,189,248,0.95)"
                                                        : "1px solid rgba(96,165,250,0.26)",
                                                }, children: section.replaceAll("_", " ") }, section))) }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 2fr 1fr", gap: 10 }, children: [_jsx("input", { style: inputStyle, value: form.section, readOnly: true, placeholder: "Section" }), _jsx("input", { style: inputStyle, placeholder: "Selected tests", value: form.tests, readOnly: true }), _jsxs("select", { value: form.priority, onChange: (e) => setForm({ ...form, priority: e.target.value }), style: inputStyle, children: [_jsx("option", { value: "Routine", children: "Routine" }), _jsx("option", { value: "Urgent", children: "Urgent" })] })] }), _jsxs("div", { style: { marginTop: 16, ...itemStyle, maxHeight: 320, overflowY: "auto" }, children: [_jsxs("div", { style: {
                                                        display: "flex",
                                                        justifyContent: "space-between",
                                                        alignItems: "center",
                                                        gap: 10,
                                                        marginBottom: 12,
                                                        flexWrap: "wrap",
                                                    }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }, children: [_jsxs("div", { style: { fontSize: 18, fontWeight: 800, textTransform: "capitalize" }, children: ["Available Tests \u2014 ", form.section.replaceAll("_", " ")] }), _jsxs("span", { style: {
                                                                        display: "inline-block",
                                                                        padding: "6px 10px",
                                                                        borderRadius: 999,
                                                                        fontSize: 12,
                                                                        fontWeight: 800,
                                                                        background: "rgba(14,165,233,0.18)",
                                                                        border: "1px solid rgba(56,189,248,0.35)",
                                                                        color: "#bae6fd",
                                                                    }, children: ["Selected: ", selectedTests.length] })] }), _jsxs("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" }, children: [_jsx("button", { type: "button", onClick: () => setSelectedTests(filteredCatalogTests), style: secondaryBtn, children: "Select All" }), _jsx("button", { type: "button", onClick: () => setSelectedTests([]), style: secondaryBtn, children: "Clear Selected" }), _jsx("button", { type: "button", onClick: copySelectedTests, style: secondaryBtn, children: "Copy Selected" }), _jsx("button", { type: "button", onClick: exportSelectedAsTxt, style: secondaryBtn, children: "Export TXT" }), _jsx("button", { type: "button", onClick: exportSelectedAsCsv, style: secondaryBtn, children: "Export CSV" })] })] }), _jsx("div", { style: { marginBottom: 12 }, children: _jsx("input", { style: inputStyle, placeholder: "Search tests in this section...", value: labSearch, onChange: (e) => setLabSearch(e.target.value) }) }), filteredCatalogTests.length ? (_jsx("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }, children: filteredCatalogTests.map((test) => (_jsx("button", { type: "button", onClick: () => setSelectedTests((prev) => prev.includes(test)
                                                            ? prev.filter((item) => item !== test)
                                                            : [...prev, test]), style: {
                                                            textAlign: "left",
                                                            padding: "10px 12px",
                                                            borderRadius: 12,
                                                            border: selectedTests.includes(test)
                                                                ? "1px solid rgba(56,189,248,0.95)"
                                                                : "1px solid rgba(148,163,184,0.25)",
                                                            background: selectedTests.includes(test)
                                                                ? "linear-gradient(135deg, rgba(37,99,235,0.34), rgba(14,165,233,0.18))"
                                                                : "rgba(255,255,255,0.05)",
                                                            color: "#f8fafc",
                                                            cursor: "pointer",
                                                            fontWeight: selectedTests.includes(test) ? 800 : 500,
                                                        }, children: test }, test))) })) : (_jsx("div", { style: { color: "#cbd5e1" }, children: "No tests match this search in the current section" }))] }), _jsx("div", { style: { marginTop: 14 }, children: _jsx("button", { type: "submit", style: primaryBtn, children: "Add Lab Order" }) })] })), activeTab === "selected" && (_jsxs("div", { style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Selected Tests" }), _jsx("div", { style: { display: "grid", gap: 12 }, children: selectedTests.length === 0 ? (_jsx("div", { style: { color: "#cbd5e1" }, children: "No tests selected yet" })) : (selectedTests.map((test) => (_jsx("div", { style: itemStyle, children: test }, test)))) })] })), activeTab === "orders" && (_jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }, children: [_jsx("h2", { style: titleStyle, children: "Lab Orders" }), _jsxs("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" }, children: [_jsx("button", { type: "button", style: tabBtnStyle(ordersStatusFilter === "all"), onClick: () => setOrdersStatusFilter("all"), children: "All" }), _jsx("button", { type: "button", style: tabBtnStyle(ordersStatusFilter === "Pending"), onClick: () => setOrdersStatusFilter("Pending"), children: "Pending" }), _jsx("button", { type: "button", style: tabBtnStyle(ordersStatusFilter === "Completed"), onClick: () => setOrdersStatusFilter("Completed"), children: "Completed" })] })] }), _jsxs("div", { style: { marginTop: 12, color: "#cbd5e1" }, children: ["Current filter: ", ordersStatusFilter === "all" ? "All" : ordersStatusFilter] }), _jsx("div", { style: { display: "grid", gap: 12, marginTop: 14 }, children: filteredOrdersByStatus.length === 0 ? (_jsx("div", { style: { color: "#cbd5e1" }, children: "No lab orders for this filter" })) : filteredOrdersByStatus.map((order) => (_jsxs("div", { style: itemStyle, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: order.patientName }), _jsx("div", { style: { marginTop: 6, color: "#e2e8f0" }, children: order.tests.join(" • ") }), _jsxs("div", { style: { marginTop: 8, color: "#cbd5e1" }, children: ["Section: ", order.section, " \u2022 Priority: ", order.priority] }), _jsx("div", { style: { marginTop: 10 }, children: _jsx("span", { style: badgeStyle(order.status), children: order.status }) }), order.result ? (_jsxs("div", { style: { marginTop: 10, color: "#cbd5e1" }, children: ["Result: ", order.result] })) : null] }, order.id))) })] })), activeTab === "results" && (_jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }, children: [_jsx("h2", { style: titleStyle, children: "Results" }), _jsxs("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" }, children: [_jsx("button", { type: "button", style: tabBtnStyle(resultsFilter === "all"), onClick: () => setResultsFilter("all"), children: "All Results" }), _jsx("button", { type: "button", style: tabBtnStyle(resultsFilter === "has_result"), onClick: () => setResultsFilter("has_result"), children: "Has Result" }), _jsx("button", { type: "button", style: tabBtnStyle(resultsFilter === "no_result"), onClick: () => setResultsFilter("no_result"), children: "No Result" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: printResults, children: "Print Results" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: exportResultsAsTxt, children: "Export TXT" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: exportResultsAsCsv, children: "Export CSV" })] })] }), _jsx("div", { style: { marginTop: 12 }, children: _jsx("input", { style: inputStyle, placeholder: "Search by test name...", value: resultsSearch, onChange: (e) => setResultsSearch(e.target.value) }) }), _jsxs("div", { style: { marginTop: 12, color: "#cbd5e1" }, children: ["Current filter: ", resultsFilter === "all" ? "All Results" : resultsFilter === "has_result" ? "Has Result" : "No Result"] }), _jsx("div", { style: { display: "grid", gap: 12, marginTop: 14 }, children: filteredResults.length === 0 ? (_jsx("div", { style: { color: "#cbd5e1" }, children: "No results match this filter" })) : (filteredResults.map((order) => (_jsxs("div", { style: itemStyle, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: order.patientName }), _jsx("div", { style: { marginTop: 6, color: "#e2e8f0" }, children: order.tests.join(" • ") }), _jsx("div", { style: { marginTop: 8 }, children: _jsx("span", { style: badgeStyle(order.status), children: order.status }) }), _jsxs("div", { style: { marginTop: 10, color: "#cbd5e1" }, children: ["Result: ", order.result || "No result entered yet"] })] }, order.id)))) })] }))] })] })] }) }));
}
const pageStyle = {
    minHeight: "100vh",
    background: "linear-gradient(180deg, #0f172a 0%, #111827 100%)",
    color: "#f8fafc",
    padding: 24,
};
const cardStyle = {
    background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
    border: "1px solid rgba(96,165,250,0.28)",
    borderRadius: 24,
    padding: 22,
    boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
};
const itemStyle = {
    background: "linear-gradient(180deg, rgba(37,99,235,0.18), rgba(15,23,42,0.30))",
    border: "1px solid rgba(96,165,250,0.26)",
    borderRadius: 18,
    padding: 16,
    boxShadow: "0 8px 18px rgba(0,0,0,0.18)",
};
const inputStyle = {
    width: "100%",
    border: "1px solid rgba(148,163,184,0.35)",
    borderRadius: 14,
    padding: "12px 14px",
    background: "rgba(255,255,255,0.08)",
    color: "#f8fafc",
    outline: "none",
};
const secondaryBtn = {
    border: "1px solid rgba(148,163,184,0.35)",
    borderRadius: 12,
    padding: "8px 12px",
    background: "rgba(255,255,255,0.08)",
    color: "#e5e7eb",
    fontWeight: 700,
    cursor: "pointer",
};
const primaryBtn = {
    border: "none",
    borderRadius: 14,
    padding: "12px 16px",
    background: "linear-gradient(135deg, #0ea5e9, #2563eb)",
    color: "white",
    fontWeight: 700,
    cursor: "pointer",
};
const titleStyle = {
    marginTop: 0,
    marginBottom: 16,
    fontSize: 28,
};
const errorStyle = {
    background: "linear-gradient(180deg, rgba(127,29,29,0.5), rgba(69,10,10,0.55))",
    border: "1px solid rgba(248,113,113,0.45)",
    color: "#fecaca",
    borderRadius: 20,
    padding: 16,
};
const successStyle = {
    background: "linear-gradient(180deg, rgba(20,83,45,0.5), rgba(5,46,22,0.55))",
    border: "1px solid rgba(74,222,128,0.45)",
    color: "#bbf7d0",
    borderRadius: 20,
    padding: 16,
};
const tabBtnStyle = (active) => ({
    border: active ? "1px solid rgba(56,189,248,0.95)" : "1px solid rgba(148,163,184,0.35)",
    borderRadius: 14,
    padding: "10px 14px",
    background: active
        ? "linear-gradient(135deg, rgba(37,99,235,0.34), rgba(14,165,233,0.18))"
        : "rgba(255,255,255,0.08)",
    color: "#e5e7eb",
    fontWeight: 800,
    cursor: "pointer",
});
const badgeStyle = (status) => ({
    display: "inline-block",
    padding: "6px 10px",
    borderRadius: 999,
    fontSize: 13,
    fontWeight: 800,
    background: status === "Completed" ? "#dcfce7" : status === "Processing" ? "#dbeafe" : "#fef3c7",
    color: status === "Completed" ? "#166534" : status === "Processing" ? "#1d4ed8" : "#92400e",
});
