import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  Pill,
  FlaskConical,
  Bot,
  ShieldPlus,
  LogOut,
  ClipboardPlus,
  ClipboardList,
} from "lucide-react";
import { useAuth } from "../auth/AuthContext";

const baseLinkStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: "12px",
  padding: "12px 14px",
  borderRadius: "14px",
  textDecoration: "none",
  fontWeight: 700,
  marginBottom: "10px",
  transition: "0.2s ease",
};

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <aside
      style={{
        width: 280,
        background: "linear-gradient(180deg, #0f172a, #111827 60%, #1e293b)",
        color: "white",
        padding: 20,
        boxShadow: "0 0 24px rgba(0,0,0,0.15)",
      }}
    >
      <div
        style={{
          padding: 16,
          borderRadius: 18,
          background: "rgba(255,255,255,0.06)",
          marginBottom: 24,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <ShieldPlus size={24} />
          <div>
            <div style={{ fontSize: 20, fontWeight: 800 }}>AI Hospital</div>
            <div style={{ fontSize: 13, color: "#94a3b8" }}>Epic-style Workspace</div>
          </div>
        </div>
      </div>

      {user && (
        <div
          style={{
            marginBottom: 20,
            padding: 14,
            borderRadius: 14,
            background: "rgba(255,255,255,0.06)",
          }}
        >
          <div style={{ fontWeight: 800 }}>{user.username}</div>
          <div style={{ color: "#93c5fd", marginTop: 4 }}>Role: {user.role}</div>
          <div style={{ color: "#94a3b8", marginTop: 4 }}>
            Hospital: {user.hospital_id}
          </div>
        </div>
      )}

      <div style={{ fontSize: 12, color: "#94a3b8", marginBottom: 12 }}>
        CLINICAL MODULES
      </div>

      <NavLink
        to="/dashboard"
        style={({ isActive }) => ({
          ...baseLinkStyle,
          background: isActive ? "#2563eb" : "transparent",
          color: isActive ? "white" : "#dbe7ff",
        })}
      >
        <LayoutDashboard size={18} />
        Dashboard
      </NavLink>

      <NavLink
        to="/patients"
        style={({ isActive }) => ({
          ...baseLinkStyle,
          background: isActive ? "#2563eb" : "transparent",
          color: isActive ? "white" : "#dbe7ff",
        })}
      >
        <Users size={18} />
        Patients
      </NavLink>

      <NavLink
        to="/doctor-orders"
        style={({ isActive }) => ({
          ...baseLinkStyle,
          background: isActive ? "#2563eb" : "transparent",
          color: isActive ? "white" : "#dbe7ff",
        })}
      >
        <ClipboardList size={18} />
        Doctor Orders
      </NavLink>

      <NavLink
        to="/pharmacy"
        style={({ isActive }) => ({
          ...baseLinkStyle,
          background: isActive ? "#2563eb" : "transparent",
          color: isActive ? "white" : "#dbe7ff",
        })}
      >
        <Pill size={18} />
        Pharmacy
      </NavLink>

      <NavLink
        to="/nurse"
        style={({ isActive }) => ({
          ...baseLinkStyle,
          background: isActive ? "#2563eb" : "transparent",
          color: isActive ? "white" : "#dbe7ff",
        })}
      >
        <ClipboardPlus size={18} />
        Nurse Workflow
      </NavLink>

      <NavLink
        to="/labs"
        style={({ isActive }) => ({
          ...baseLinkStyle,
          background: isActive ? "#2563eb" : "transparent",
          color: isActive ? "white" : "#dbe7ff",
        })}
      >
        <FlaskConical size={18} />
        Labs
      </NavLink>

      <NavLink
        to="/ai"
        style={({ isActive }) => ({
          ...baseLinkStyle,
          background: isActive ? "#2563eb" : "transparent",
          color: isActive ? "white" : "#dbe7ff",
        })}
      >
        <Bot size={18} />
        AI Assistant
      </NavLink>

      <button
        onClick={handleLogout}
        style={{
          marginTop: 20,
          width: "100%",
          padding: "12px 14px",
          borderRadius: 14,
          border: "none",
          background: "#7f1d1d",
          color: "white",
          fontWeight: 700,
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 10,
        }}
      >
        <LogOut size={16} />
        Logout
      </button>
    </aside>
  );
}
