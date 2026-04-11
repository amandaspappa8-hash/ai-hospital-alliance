import React from "react"

type Props = {
  children: React.ReactNode
}

type State = {
  hasError: boolean
  error?: Error | null
}

export default class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
    }
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("[ErrorBoundary] Caught UI error", {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
    })
  }

  handleReload = () => {
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "#0b1020",
            color: "#ffffff",
            padding: "24px",
          }}
        >
          <div
            style={{
              width: "100%",
              maxWidth: "720px",
              borderRadius: "16px",
              padding: "24px",
              background: "rgba(255,255,255,0.06)",
              border: "1px solid rgba(255,255,255,0.12)",
              boxShadow: "0 10px 40px rgba(0,0,0,0.25)",
            }}
          >
            <h1 style={{ marginTop: 0, marginBottom: "12px", fontSize: "28px" }}>
              System UI Error
            </h1>

            <p style={{ opacity: 0.9, lineHeight: 1.7 }}>
              Something went wrong in the interface. The application caught the
              error to prevent a full crash.
            </p>

            <div
              style={{
                marginTop: "16px",
                padding: "12px",
                borderRadius: "10px",
                background: "rgba(0,0,0,0.25)",
                overflowX: "auto",
                fontFamily: "monospace",
                fontSize: "14px",
              }}
            >
              {this.state.error?.message || "Unknown UI error"}
            </div>

            <div style={{ marginTop: "18px", display: "flex", gap: "12px", flexWrap: "wrap" }}>
              <button
                onClick={this.handleReload}
                style={{
                  border: "none",
                  borderRadius: "10px",
                  padding: "12px 18px",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Reload App
              </button>

              <button
                onClick={() => history.back()}
                style={{
                  border: "1px solid rgba(255,255,255,0.2)",
                  background: "transparent",
                  color: "#fff",
                  borderRadius: "10px",
                  padding: "12px 18px",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Go Back
              </button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
