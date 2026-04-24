import { useState, useRef, useEffect } from "react"
import { getUser } from "@/lib/auth-storage"

type Message = { role: "user" | "assistant"; content: string; time: string }

const SUGGESTIONS = [
  "ما هي أعراض الجلطة القلبية؟",
  "كيف أقرأ نتائج CBC؟",
  "ما الفرق بين Troponin I و T؟",
  "متى يحتاج المريض للـ ICU؟",
  "ما هي جرعة الأسبرين في الطوارئ؟",
]

export default function MedicalChatbot() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "مرحباً! أنا مساعدك الطبي الذكي. يمكنني مساعدتك في تفسير نتائج التحاليل، الأشعة، التشخيصات، والأسئلة الطبية.", time: new Date().toLocaleTimeString() }
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [unread, setUnread] = useState(0)
  const bottomRef = useRef<HTMLDivElement>(null)
  const user = getUser()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  async function send(text?: string) {
    const msg = text ?? input.trim()
    if (!msg || loading) return
    setInput("")
    setLoading(true)

    const userMsg: Message = { role: "user", content: msg, time: new Date().toLocaleTimeString() }
    setMessages(prev => [...prev, userMsg])

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 600,
          system: `You are an expert medical AI assistant integrated in AI Hospital Alliance platform.
You help doctors and nurses with:
- Interpreting lab results and imaging
- Clinical decision support
- Drug dosages and interactions
- Medical terminology explanations
- Treatment guidelines

Always be concise, accurate, and professional. Respond in the same language as the user (Arabic or English).
Include relevant clinical context when appropriate. Add ⚠️ for critical warnings.`,
          messages: [
            ...messages.filter(m => m.role !== "assistant" || messages.indexOf(m) > 0)
              .slice(-6)
              .map(m => ({ role: m.role, content: m.content })),
            { role: "user", content: msg }
          ]
        })
      })
      const data = await res.json()
      const reply = data.content?.[0]?.text ?? "عذراً، لم أتمكن من المعالجة."
      setMessages(prev => [...prev, { role: "assistant", content: reply, time: new Date().toLocaleTimeString() }])
      if (!open) setUnread(u => u + 1)
    } catch {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "⚠️ تعذر الاتصال بـ Claude AI. تأكد من الاتصال بالإنترنت.",
        time: new Date().toLocaleTimeString()
      }])
    } finally {
      setLoading(false)
    }
  }

  function handleOpen() { setOpen(true); setUnread(0) }

  return (
    <>
      {/* Floating button */}
      <div style={{
        position: "fixed", bottom: 24, right: 24, zIndex: 9999,
      }}>
        {!open && (
          <button onClick={handleOpen} style={{
            width: 56, height: 56, borderRadius: "50%", border: "none",
            background: "linear-gradient(135deg,#7c3aed,#2563eb)",
            color: "white", fontSize: 24, cursor: "pointer",
            boxShadow: "0 4px 20px rgba(124,58,237,0.5)",
            display: "flex", alignItems: "center", justifyContent: "center",
            transition: "transform 0.2s",
          }}
            onMouseEnter={e => e.currentTarget.style.transform = "scale(1.1)"}
            onMouseLeave={e => e.currentTarget.style.transform = "scale(1)"}
          >
            🧠
            {unread > 0 && (
              <div style={{
                position: "absolute", top: -4, right: -4,
                width: 20, height: 20, borderRadius: "50%",
                background: "#ef4444", color: "white",
                fontSize: 11, fontWeight: 900,
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>{unread}</div>
            )}
          </button>
        )}

        {/* Chat window */}
        {open && (
          <div style={{
            width: 380, height: 560,
            background: "linear-gradient(135deg,#0f172a,#1a2540)",
            border: "1px solid rgba(124,58,237,0.4)",
            borderRadius: 20, display: "flex", flexDirection: "column",
            boxShadow: "0 20px 60px rgba(0,0,0,0.6)",
            overflow: "hidden",
          }}>
            {/* Header */}
            <div style={{
              padding: "14px 16px", display: "flex", alignItems: "center", gap: 10,
              background: "linear-gradient(135deg,#7c3aed22,#2563eb22)",
              borderBottom: "1px solid rgba(124,58,237,0.2)",
            }}>
              <div style={{ width: 36, height: 36, borderRadius: 10, background: "linear-gradient(135deg,#7c3aed,#2563eb)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18 }}>🧠</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 800, color: "white", fontSize: 13 }}>Medical AI Assistant</div>
                <div style={{ fontSize: 11, color: "#4ade80", display: "flex", alignItems: "center", gap: 4 }}>
                  <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#4ade80" }} />
                  Claude Sonnet · Online
                </div>
              </div>
              <button onClick={() => setOpen(false)} style={{ width: 28, height: 28, borderRadius: 8, border: "none", background: "rgba(255,255,255,0.06)", color: "#64748b", cursor: "pointer", fontSize: 16 }}>×</button>
            </div>

            {/* Messages */}
            <div style={{ flex: 1, overflowY: "auto", padding: 14, display: "flex", flexDirection: "column", gap: 10 }}>
              {messages.map((m, i) => (
                <div key={i} style={{ display: "flex", flexDirection: m.role === "user" ? "row-reverse" : "row", gap: 8, alignItems: "flex-start" }}>
                  <div style={{
                    width: 28, height: 28, borderRadius: 8, flexShrink: 0,
                    background: m.role === "user" ? "linear-gradient(135deg,#2563eb,#7c3aed)" : "linear-gradient(135deg,#059669,#10b981)",
                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13,
                  }}>
                    {m.role === "user" ? "👤" : "🧠"}
                  </div>
                  <div style={{ maxWidth: "75%" }}>
                    <div style={{
                      padding: "10px 13px", borderRadius: m.role === "user" ? "16px 4px 16px 16px" : "4px 16px 16px 16px",
                      background: m.role === "user" ? "linear-gradient(135deg,#2563eb,#7c3aed)" : "rgba(255,255,255,0.06)",
                      color: "white", fontSize: 13, lineHeight: 1.6,
                      border: m.role === "assistant" ? "1px solid rgba(255,255,255,0.08)" : "none",
                    }}>
                      {m.content}
                    </div>
                    <div style={{ fontSize: 10, color: "#475569", marginTop: 3, textAlign: m.role === "user" ? "right" : "left" }}>{m.time}</div>
                  </div>
                </div>
              ))}

              {loading && (
                <div style={{ display: "flex", gap: 8, alignItems: "flex-start" }}>
                  <div style={{ width: 28, height: 28, borderRadius: 8, background: "linear-gradient(135deg,#059669,#10b981)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13 }}>🧠</div>
                  <div style={{ padding: "10px 14px", borderRadius: "4px 16px 16px 16px", background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.08)" }}>
                    <div style={{ display: "flex", gap: 4 }}>
                      {[0,1,2].map(i => (
                        <div key={i} style={{ width: 7, height: 7, borderRadius: "50%", background: "#7c3aed", animation: `bounce 1s ${i*0.2}s infinite` }} />
                      ))}
                    </div>
                    <style>{`@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }`}</style>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            {/* Suggestions */}
            {messages.length <= 1 && (
              <div style={{ padding: "0 12px 8px", display: "flex", gap: 6, flexWrap: "wrap" }}>
                {SUGGESTIONS.slice(0, 3).map(s => (
                  <button key={s} onClick={() => send(s)} style={{
                    padding: "4px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600,
                    background: "rgba(124,58,237,0.1)", color: "#a78bfa",
                    border: "1px solid rgba(124,58,237,0.25)", cursor: "pointer",
                  }}>{s}</button>
                ))}
              </div>
            )}

            {/* Input */}
            <div style={{ padding: "10px 14px", borderTop: "1px solid rgba(255,255,255,0.06)", display: "flex", gap: 8 }}>
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && !e.shiftKey && send()}
                placeholder="اكتب سؤالك الطبي..."
                style={{
                  flex: 1, padding: "10px 14px", borderRadius: 12, fontSize: 13,
                  background: "rgba(255,255,255,0.06)", border: "1px solid rgba(124,58,237,0.3)",
                  color: "white", outline: "none",
                }}
              />
              <button onClick={() => send()} disabled={loading || !input.trim()} style={{
                width: 40, height: 40, borderRadius: 12, border: "none",
                background: loading || !input.trim() ? "rgba(124,58,237,0.2)" : "linear-gradient(135deg,#7c3aed,#2563eb)",
                color: "white", cursor: loading || !input.trim() ? "not-allowed" : "pointer", fontSize: 16,
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>↑</button>
            </div>
          </div>
        )}
      </div>
    </>
  )
}
