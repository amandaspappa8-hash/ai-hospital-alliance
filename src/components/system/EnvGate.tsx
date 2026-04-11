import type { ReactNode } from "react"
import { validateFrontendEnv, isProduction } from "@/lib/env"

type Props = {
  children: ReactNode
}

export default function EnvGate({ children }: Props) {
  const result = validateFrontendEnv()

  if (result.ok) {
    return <>{children}</>
  }

  if (isProduction) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "24px",
          background: "#111827",
          color: "#ffffff",
        }}
      >
        <div
          style={{
            width: "100%",
            maxWidth: "780px",
            borderRadius: "16px",
            padding: "24px",
            background: "rgba(255,255,255,0.06)",
            border: "1px solid rgba(255,255,255,0.12)",
          }}
        >
          <h1 style={{ marginTop: 0 }}>Environment Validation Failed</h1>
          <p>The application cannot safely start in production.</p>
          <ul>
            {result.issues.map((issue) => (
              <li key={issue}>{issue}</li>
            ))}
          </ul>
        </div>
      </div>
    )
  }

  console.warn("[EnvGate] frontend env issues", result.issues)
  return <>{children}</>
}
