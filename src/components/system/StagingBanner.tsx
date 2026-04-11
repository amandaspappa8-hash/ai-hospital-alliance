import { appEnv, isStaging } from "@/lib/env"

export default function StagingBanner() {
  if (!isStaging) return null

  return (
    <div
      style={{
        width: "100%",
        background: "#f59e0b",
        color: "#111827",
        padding: "10px 16px",
        fontWeight: 700,
        textAlign: "center",
        letterSpacing: "0.2px",
        position: "sticky",
        top: 0,
        zIndex: 9999,
        boxShadow: "0 2px 10px rgba(0,0,0,0.12)",
      }}
    >
      STAGING ENVIRONMENT — current mode: {appEnv}
    </div>
  )
}
