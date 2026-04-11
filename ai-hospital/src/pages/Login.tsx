import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();

  const [username, setUsername] = useState("doctor1");
  const [password, setPassword] = useState("1234");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/jwt-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const text = await res.text();
      let data: any = {};

      try {
        data = JSON.parse(text);
      } catch {
        throw new Error(`Non-JSON response: ${text}`);
      }

      if (!res.ok) {
        throw new Error(data?.detail || data?.error || `HTTP ${res.status}`);
      }

      if (!data.access_token || !data.user) {
        throw new Error(data?.error || "Invalid login response");
      }

      login(data.access_token, data.user);
      nav("/dashboard");
    } catch (e: any) {
      setError(e.message || "Login failed");
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        background: "#f1f5f9",
      }}
    >
      <div
        style={{
          background: "white",
          padding: 30,
          borderRadius: 16,
          width: 360,
          boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
        }}
      >
        <h2 style={{ marginTop: 0 }}>AI Hospital Login</h2>

        <label>Username</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 8,
            marginBottom: 14,
            borderRadius: 10,
            border: "1px solid #cbd5e1",
            boxSizing: "border-box",
          }}
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 8,
            marginBottom: 14,
            borderRadius: 10,
            border: "1px solid #cbd5e1",
            boxSizing: "border-box",
          }}
        />

        {error && (
          <div
            style={{
              background: "#fef2f2",
              color: "#b91c1c",
              padding: 10,
              borderRadius: 10,
              marginBottom: 14,
              whiteSpace: "pre-wrap",
            }}
          >
            {error}
          </div>
        )}

        <button
          onClick={handleLogin}
          style={{
            marginTop: 6,
            width: "100%",
            padding: 12,
            background: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: 10,
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </div>
    </div>
  );
}
