import { ReactNode } from "react"
import { NavLink } from "react-router-dom"
import {
  LayoutDashboard,
  Users,
  ClipboardList,
  FileText,
  Stethoscope,
  Brain,
  Activity,
} from "lucide-react"

export default function MedicalLayout({ children }: { children: ReactNode }) {
  return (
    <div style={{ display: "flex", height: "100vh", background: "#0b1220" }}>
      
      <div style={{
        width: 260,
        background: "#111827",
        borderRight: "1px solid #374151",
        padding: 20
      }}>
        <div style={{
          fontSize: 20,
          fontWeight: 700,
          marginBottom: 30
        }}>
          AI Hospital
        </div>

        <Nav icon={<LayoutDashboard size={18}/>} to="/dashboard" label="Dashboard"/>
        <Nav icon={<Brain size={18}/>} to="/ai-routing" label="AI Routing"/>
        <Nav icon={<Users size={18}/>} to="/patients" label="Patients"/>
        <Nav icon={<ClipboardList size={18}/>} to="/orders" label="Orders"/>
        <Nav icon={<FileText size={18}/>} to="/reports" label="Reports"/>
        <Nav icon={<Stethoscope size={18}/>} to="/appointments" label="Appointments"/>
        <Nav icon={<Activity size={18}/>} to="/notes" label="Notes"/>

      </div>

      <div style={{ flex: 1, overflow: "auto" }}>
        {children}
      </div>

    </div>
  )
}

function Nav({ icon, to, label }: any) {
  return (
    <NavLink
      to={to}
      style={({ isActive }) => ({
        display: "flex",
        alignItems: "center",
        gap: 10,
        padding: "12px",
        borderRadius: 10,
        marginBottom: 8,
        textDecoration: "none",
        color: isActive ? "#22c55e" : "#cbd5e1",
        background: isActive ? "#0b1220" : "transparent"
      })}
    >
      {icon}
      {label}
    </NavLink>
  )
}
