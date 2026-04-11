export function buildDigitalSignature(doctorName = "Dr Mohammed Elfallah") {
    return {
        doctorName,
        role: "Clinical Pharmacist",
        signedAt: new Date().toLocaleString(),
        signatureText: `Digitally signed by ${doctorName}`,
    };
}
