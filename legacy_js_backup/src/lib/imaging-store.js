const KEY_ORDERS = "aha_imaging_orders_v1";
const KEY_STUDIES = "aha_imaging_studies_v1";
function load(key, fallback) {
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
function save(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}
export function listOrders() {
    return load(KEY_ORDERS, []);
}
export function listStudies() {
    return load(KEY_STUDIES, []);
}
export function createOrder(input) {
    const orders = listOrders();
    const order = {
        ...input,
        id: String(Date.now()),
        status: "ORDERED",
        createdAt: new Date().toISOString(),
    };
    save(KEY_ORDERS, [order, ...orders]);
    // Auto-create a demo study to simulate PACS arrival (later: real DICOM)
    const studies = listStudies();
    const study = {
        studyId: `STUDY-${order.id}`,
        orderId: order.id,
        patientId: order.patientId,
        patientName: order.patientName,
        modality: order.modality,
        description: order.studyDescription,
        status: "AVAILABLE",
        studyDate: new Date().toISOString(),
        seriesCount: Math.floor(Math.random() * 6) + 1,
        instanceCount: Math.floor(Math.random() * 300) + 50,
        viewerUrl: `/pacs?study=${encodeURIComponent(`STUDY-${order.id}`)}`,
    };
    save(KEY_STUDIES, [study, ...studies]);
    return order;
}
export function clearImagingDemo() {
    localStorage.removeItem(KEY_ORDERS);
    localStorage.removeItem(KEY_STUDIES);
}
export function getStudyById(studyId) {
    return listStudies().find((s) => s.studyId === studyId);
}
