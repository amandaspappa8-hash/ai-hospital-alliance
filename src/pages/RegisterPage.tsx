import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"

const API = import.meta.env.VITE_API_BASE_URL || ""

const PLANS = [
  {
    id: "trial",
    name: "Trial",
    price: "Free",
    duration: "14 days",
    users: "5 users",
    patients: "50 patients",
    ai: "20 AI calls/day",
    color: "#6B7280",
    features: ["Basic EMR", "Labs", "Radiology"],
  },
  {
    id: "starter",
    name: "Starter",
    price: "$299/mo",
    duration: "Monthly",
    users: "25 users",
    patients: "500 patients",
    ai: "200 AI calls/day",
    color: "#2563EB",
    features: ["Basic EMR", "Labs", "Radiology", "Pharmacy", "Reports"],
  },
  {
    id: "professional",
    name: "Professional",
    price: "$799/mo",
    duration: "Monthly",
    users: "100 users",
    patients: "5,000 patients",
    ai: "1,000 AI calls/day",
    color: "#7C3AED",
    popular: true,
    features: ["All Starter features", "AI Diagnosis", "FHIR Export", "Audit Logs", "2FA"],
  },
  {
    id: "enterprise",
    name: "Enterprise",
    price: "Custom",
    duration: "Annual",
    users: "Unlimited",
    patients: "Unlimited",
    ai: "Unlimited AI",
    color: "#DC2626",
    features: ["All features", "Dedicated support", "Custom integrations", "SLA guarantee"],
  },
]

export default function RegisterPage() {
  const navigate = useNavigate()
  const [step, setStep] = useState<"plan" | "form" | "success">("plan")
  const [selectedPlan, setSelectedPlan] = useState("trial")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [result, setResult] = useState<any>(null)

  const [form, setForm] = useState({
    hospital_name: "",
    admin_name: "",
    admin_email: "",
    admin_password: "",
    confirm_password: "",
    country: "",
    phone: "",
  })

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError("")
    if (form.admin_password !== form.confirm_password) {
      setError("Passwords do not match")
      return
    }
    if (form.admin_password.length < 12) {
      setError("Password must be at least 12 characters")
      return
    }
    setLoading(true)
    try {
      const res = await fetch(`${API}/saas/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          hospital_name: form.hospital_name,
          admin_name: form.admin_name,
          admin_email: form.admin_email,
          admin_password: form.admin_password,
          country: form.country,
          phone: form.phone,
          plan: selectedPlan,
        }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || "Registration failed")
      setResult(data)
      setStep("success")
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const plan = PLANS.find(p => p.id === selectedPlan)!

  return (
    <div style={styles.page}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.logo}>
          <span style={styles.logoIcon}>⚕</span>
          <span style={styles.logoText}>AI Hospital Alliance</span>
        </div>
        <Link to="/login" style={styles.loginLink}>Already have an account → Login</Link>
      </div>

      {step === "plan" && (
        <div style={styles.container}>
          <div style={styles.heroText}>
            <h1 style={styles.h1}>Choose your plan</h1>
            <p style={styles.sub}>Start with a 14-day free trial. No credit card required.</p>
          </div>

          <div style={styles.plansGrid}>
            {PLANS.map(p => (
              <div
                key={p.id}
                onClick={() => setSelectedPlan(p.id)}
                style={{
                  ...styles.planCard,
                  border: selectedPlan === p.id
                    ? `2px solid ${p.color}`
                    : "2px solid #1F2937",
                  background: selectedPlan === p.id
                    ? `linear-gradient(135deg, ${p.color}15, #111827)`
                    : "#111827",
                  transform: selectedPlan === p.id ? "translateY(-4px)" : "none",
                  boxShadow: selectedPlan === p.id
                    ? `0 8px 32px ${p.color}30`
                    : "none",
                }}
              >
                {p.popular && <div style={{ ...styles.badge, background: p.color }}>Most Popular</div>}
                <div style={{ color: p.color, fontSize: 28, marginBottom: 8 }}>●</div>
                <div style={styles.planName}>{p.name}</div>
                <div style={{ ...styles.planPrice, color: p.color }}>{p.price}</div>
                <div style={styles.planDuration}>{p.duration}</div>
                <div style={styles.divider} />
                <div style={styles.stat}><span style={styles.statIcon}>👥</span>{p.users}</div>
                <div style={styles.stat}><span style={styles.statIcon}>🏥</span>{p.patients}</div>
                <div style={styles.stat}><span style={styles.statIcon}>🤖</span>{p.ai}</div>
                <div style={styles.divider} />
                {p.features.map(f => (
                  <div key={f} style={styles.feature}><span style={{ color: p.color }}>✓</span> {f}</div>
                ))}
              </div>
            ))}
          </div>

          <div style={{ textAlign: "center", marginTop: 32 }}>
            <button
              onClick={() => setStep("form")}
              style={{ ...styles.btn, background: plan.color }}
            >
              Continue with {plan.name} →
            </button>
          </div>
        </div>
      )}

      {step === "form" && (
        <div style={styles.formContainer}>
          <div style={styles.formCard}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 24 }}>
              <button onClick={() => setStep("plan")} style={styles.backBtn}>← Back</button>
              <div>
                <h2 style={styles.formTitle}>Register your hospital</h2>
                <div style={{ color: plan.color, fontSize: 13, fontWeight: 600 }}>
                  {plan.name} Plan — {plan.price}
                </div>
              </div>
            </div>

            {error && <div style={styles.errorBox}>{error}</div>}

            <form onSubmit={handleSubmit}>
              <div style={styles.formGrid}>
                <div style={styles.fieldFull}>
                  <label style={styles.label}>Hospital Name *</label>
                  <input
                    name="hospital_name"
                    value={form.hospital_name}
                    onChange={handleChange}
                    required
                    placeholder="e.g. National Medical Center"
                    style={styles.input}
                  />
                </div>

                <div style={styles.field}>
                  <label style={styles.label}>Admin Full Name *</label>
                  <input
                    name="admin_name"
                    value={form.admin_name}
                    onChange={handleChange}
                    required
                    placeholder="Dr. Ahmed Al-Mansouri"
                    style={styles.input}
                  />
                </div>

                <div style={styles.field}>
                  <label style={styles.label}>Admin Email *</label>
                  <input
                    name="admin_email"
                    type="email"
                    value={form.admin_email}
                    onChange={handleChange}
                    required
                    placeholder="admin@hospital.com"
                    style={styles.input}
                  />
                </div>

                <div style={styles.field}>
                  <label style={styles.label}>Password * (min 12 chars)</label>
                  <input
                    name="admin_password"
                    type="password"
                    value={form.admin_password}
                    onChange={handleChange}
                    required
                    minLength={12}
                    placeholder="••••••••••••"
                    style={styles.input}
                  />
                </div>

                <div style={styles.field}>
                  <label style={styles.label}>Confirm Password *</label>
                  <input
                    name="confirm_password"
                    type="password"
                    value={form.confirm_password}
                    onChange={handleChange}
                    required
                    placeholder="••••••••••••"
                    style={styles.input}
                  />
                </div>

                <div style={styles.field}>
                  <label style={styles.label}>Country</label>
                  <input
                    name="country"
                    value={form.country}
                    onChange={handleChange}
                    placeholder="Libya, Saudi Arabia, UAE..."
                    style={styles.input}
                  />
                </div>

                <div style={styles.field}>
                  <label style={styles.label}>Phone</label>
                  <input
                    name="phone"
                    value={form.phone}
                    onChange={handleChange}
                    placeholder="+218 91 000 0000"
                    style={styles.input}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                style={{
                  ...styles.btn,
                  background: loading ? "#374151" : plan.color,
                  width: "100%",
                  marginTop: 24,
                  opacity: loading ? 0.7 : 1,
                }}
              >
                {loading ? "Creating your hospital…" : "Create Account →"}
              </button>
            </form>
          </div>
        </div>
      )}

      {step === "success" && result && (
        <div style={styles.formContainer}>
          <div style={{ ...styles.formCard, textAlign: "center" }}>
            <div style={{ fontSize: 64, marginBottom: 16 }}>🏥</div>
            <h2 style={{ ...styles.formTitle, color: "#10B981" }}>Hospital registered!</h2>
            <p style={{ color: "#9CA3AF", marginBottom: 24 }}>
              Welcome to AI Hospital Alliance. Your hospital ID is:
            </p>

            <div style={styles.infoBox}>
              <div style={styles.infoRow}>
                <span style={styles.infoLabel}>Hospital ID</span>
                <code style={styles.infoValue}>{result.hospital_id}</code>
              </div>
              <div style={styles.infoRow}>
                <span style={styles.infoLabel}>Plan</span>
                <code style={{ ...styles.infoValue, color: plan.color }}>{result.plan}</code>
              </div>
              {result.trial_ends_at && (
                <div style={styles.infoRow}>
                  <span style={styles.infoLabel}>Trial ends</span>
                  <code style={styles.infoValue}>
                    {new Date(result.trial_ends_at).toLocaleDateString()}
                  </code>
                </div>
              )}
            </div>

            <div style={{ ...styles.infoBox, background: "#FEF3C7", border: "1px solid #F59E0B", marginTop: 16 }}>
              <div style={{ color: "#92400E", fontWeight: 700, marginBottom: 8 }}>
                ⚠️ Save your API Key — shown only once!
              </div>
              <code style={{ ...styles.infoValue, wordBreak: "break-all", color: "#92400E" }}>
                {result.api_key}
              </code>
            </div>

            <div style={{ marginTop: 24 }}>
              {(result.next_steps || []).map((s: string, i: number) => (
                <div key={i} style={styles.nextStep}>
                  <span style={{ color: "#10B981", fontWeight: 700 }}>{i + 1}.</span> {s}
                </div>
              ))}
            </div>

            <button
              onClick={() => navigate("/ahos-login")}
              style={{ ...styles.btn, background: "#10B981", marginTop: 24, width: "100%" }}
            >
              Go to Login →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    background: "#030712",
    color: "#F9FAFB",
    fontFamily: "'IBM Plex Sans', 'Segoe UI', system-ui, sans-serif",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "20px 40px",
    borderBottom: "1px solid #1F2937",
  },
  logo: { display: "flex", alignItems: "center", gap: 10 },
  logoIcon: { fontSize: 24, color: "#3B82F6" },
  logoText: { fontWeight: 700, fontSize: 18, letterSpacing: "-0.5px" },
  loginLink: {
    color: "#6B7280",
    textDecoration: "none",
    fontSize: 14,
    transition: "color 0.2s",
  },
  container: { maxWidth: 1100, margin: "0 auto", padding: "48px 24px" },
  heroText: { textAlign: "center", marginBottom: 48 },
  h1: {
    fontSize: 40,
    fontWeight: 800,
    margin: 0,
    letterSpacing: "-1px",
    background: "linear-gradient(90deg, #F9FAFB, #6B7280)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  sub: { color: "#9CA3AF", marginTop: 12, fontSize: 17 },
  plansGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
    gap: 20,
  },
  planCard: {
    padding: 24,
    borderRadius: 16,
    cursor: "pointer",
    position: "relative",
    transition: "all 0.25s ease",
  },
  badge: {
    position: "absolute",
    top: -12,
    right: 16,
    fontSize: 11,
    fontWeight: 700,
    color: "#fff",
    padding: "4px 12px",
    borderRadius: 20,
    letterSpacing: 0.5,
  },
  planName: { fontSize: 18, fontWeight: 700, marginBottom: 4 },
  planPrice: { fontSize: 24, fontWeight: 800, letterSpacing: "-0.5px" },
  planDuration: { fontSize: 12, color: "#6B7280", marginBottom: 12 },
  divider: { height: 1, background: "#1F2937", margin: "12px 0" },
  stat: { fontSize: 13, color: "#D1D5DB", marginBottom: 6, display: "flex", alignItems: "center", gap: 6 },
  statIcon: { fontSize: 14 },
  feature: { fontSize: 13, color: "#9CA3AF", marginBottom: 4 },
  btn: {
    color: "#fff",
    border: "none",
    borderRadius: 10,
    padding: "14px 32px",
    fontSize: 16,
    fontWeight: 700,
    cursor: "pointer",
    letterSpacing: "-0.3px",
    transition: "opacity 0.2s",
  },
  formContainer: { maxWidth: 680, margin: "0 auto", padding: "48px 24px" },
  formCard: {
    background: "#111827",
    border: "1px solid #1F2937",
    borderRadius: 20,
    padding: 40,
  },
  formTitle: { fontSize: 24, fontWeight: 800, margin: 0, letterSpacing: "-0.5px" },
  backBtn: {
    background: "transparent",
    border: "1px solid #374151",
    color: "#9CA3AF",
    borderRadius: 8,
    padding: "8px 16px",
    cursor: "pointer",
    fontSize: 14,
  },
  formGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 16,
  },
  field: {},
  fieldFull: { gridColumn: "1 / -1" },
  label: { display: "block", fontSize: 13, color: "#9CA3AF", marginBottom: 6, fontWeight: 500 },
  input: {
    width: "100%",
    background: "#0F172A",
    border: "1px solid #1F2937",
    borderRadius: 8,
    padding: "10px 14px",
    color: "#F9FAFB",
    fontSize: 14,
    outline: "none",
    boxSizing: "border-box",
  },
  errorBox: {
    background: "#FEF2F2",
    border: "1px solid #FCA5A5",
    color: "#DC2626",
    borderRadius: 8,
    padding: "12px 16px",
    marginBottom: 20,
    fontSize: 14,
  },
  infoBox: {
    background: "#0F172A",
    border: "1px solid #1F2937",
    borderRadius: 10,
    padding: 20,
    textAlign: "left",
  },
  infoRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  infoLabel: { fontSize: 13, color: "#6B7280" },
  infoValue: { fontSize: 13, color: "#10B981", fontFamily: "monospace" },
  nextStep: {
    textAlign: "left",
    background: "#0F172A",
    border: "1px solid #1F2937",
    borderRadius: 8,
    padding: "10px 16px",
    marginBottom: 8,
    fontSize: 14,
    color: "#D1D5DB",
  },
}
