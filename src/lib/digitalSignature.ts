import type { DigitalSignature } from "@/types/clinical"

export function buildDigitalSignature(doctorName = "Dr Mohammed Elfallah"): DigitalSignature {
  return {
    doctorName,
    role: "Clinical Pharmacist",
    signedAt: new Date().toLocaleString(),
    signatureText: `Digitally signed by ${doctorName}`,
  }
}
