function keyForDoctor(doctorId) {
    return `DOCTOR_NOTES_${doctorId}`;
}
export function getDoctorNotes(doctorId) {
    try {
        const raw = localStorage.getItem(keyForDoctor(doctorId));
        if (!raw)
            return [];
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
    }
    catch {
        return [];
    }
}
export function addDoctorNote(doctorId, text) {
    const current = getDoctorNotes(doctorId);
    const newNote = {
        id: current.length > 0 ? Math.max(...current.map((n) => n.id)) + 1 : 1,
        text,
        createdAt: new Date().toLocaleString(),
    };
    const next = [newNote, ...current];
    localStorage.setItem(keyForDoctor(doctorId), JSON.stringify(next));
    return newNote;
}
export function removeDoctorNote(doctorId, noteId) {
    const current = getDoctorNotes(doctorId);
    const next = current.filter((n) => n.id !== noteId);
    localStorage.setItem(keyForDoctor(doctorId), JSON.stringify(next));
}
