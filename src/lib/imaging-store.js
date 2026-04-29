const KEY_ORDERS = "aha_imaging_orders_v1";
const KEY_STUDIES = "aha_imaging_studies_v1";
function safeLoad(key, fallback) {
    try {
        const raw = localStorage.getItem(key);
        if (!raw)
            return fallback;
        return JSON.parse(raw);
    }
    catch {
        return fallback;
    }
}
function safeSave(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    }
    catch { }
}
export function listOrders() { return safeLoad(KEY_ORDERS, []); }
export function listStudies() { return safeLoad(KEY_STUDIES, []); }
export function createOrder(input) {
    const orders = listOrders();
    const order = {
        ...input, id: String(Date.now()), status: "ORDERED", createdAt: new Date().toISOString()
    };
    safeSave(KEY_ORDERS, [order, ...orders]);
    const studies = listStudies();
    const study = {
        studyId: `STUDY-${order.id}`, orderId: order.id,
        patientId: order.patientId, patientName: order.patientName,
        modality: order.modality, description: order.studyDescription,
        status: "AVAILABLE", studyDate: new Date().toISOString(),
        seriesCount: Math.floor(Math.random() * 6) + 1,
        instanceCount: Math.floor(Math.random() * 300) + 50,
        viewerUrl: `/pacs?study=${encodeURIComponent(`STUDY-${order.id}`)}`,
    };
    safeSave(KEY_STUDIES, [study, ...studies]);
    return order;
}
export function clearImagingDemo() {
    try {
        localStorage.removeItem(KEY_ORDERS);
        localStorage.removeItem(KEY_STUDIES);
    }
    catch { }
}
export function getStudyById(studyId) {
    return listStudies().find(s => s.studyId === studyId);
}
