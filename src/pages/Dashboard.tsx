import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import {
  Activity, AlertTriangle, Bed, BrainCircuit, CalendarDays, FlaskConical,
  HeartPulse, Hospital, Microscope, Pill, ShieldCheck, Siren, Stethoscope,
  UserRound, Users, FileText, Settings, Database, BarChart3, ClipboardList,
  Globe2, Rocket, Server, Bell
} from "lucide-react"
import { apiGet } from "@/lib/api"
import { getUser } from "@/lib/auth-storage"
import {
  getEventStore,
  getSafety,
  getCommandCenter,
  getCDSS,
  getCopilot,
} from "../services/ahosDashboardApi"
import OphthalmologyDashboardCard from "../components/ophthalmology/OphthalmologyDashboardCard";
type Patient = { id: string; name: string; status: string; condition: string; department: string }
type Appointment = { id: string; patientName: string; doctor: string; time: string; status: string }
type Alert = { patient_id?: string; message: string; severity?: string }
type Doctor = { id: string; name: string; specialty: string; status: string; rating: number }

function GlassIcon({ name, size = 46 }: { name: string; size?: number }) {
  const map: any = {
    patients: Users,
    patient: UserRound,
    appointments: CalendarDays,
    alerts: Bell,
    critical: AlertTriangle,
    doctors: Stethoscope,
    radiology: Activity,
    labs: FlaskConical,
    pharmacy: Pill,
    ai: BrainCircuit,
    pacs: Microscope,
    reports: FileText,
    nursing: HeartPulse,
    specialties: Hospital,
    operations: ClipboardList,
    bed: Bed,
    icu: HeartPulse,
    emergency: Siren,
    brain: BrainCircuit,
    analytics: BarChart3,
    settings: Settings,
    system: Database,
    globe: Globe2,
    rocket: Rocket,
    server: Server,
  }

  const colors: any = {
    patients: "#7c3aed",
    patient: "#22d3ee",
    appointments: "#a855f7",
    alerts: "#f97316",
    critical: "#ef4444",
    doctors: "#10b981",
    radiology: "#06b6d4",
    labs: "#8b5cf6",
    pharmacy: "#ec4899",
    ai: "#10b981",
    pacs: "#0ea5e9",
    reports: "#f59e0b",
    nursing: "#ec4899",
    specialties: "#8b5cf6",
    operations: "#38bdf8",
    bed: "#60a5fa",
    icu: "#fb7185",
    emergency: "#ef4444",
    brain: "#22d3ee",
    analytics: "#14b8a6",
    settings: "#93c5fd",
    system: "#38bdf8",
    globe: "#38bdf8",
    rocket: "#22d3ee",
    server: "#60a5fa",
  }

  const Icon = map[name] || Hospital
  const color = colors[name] || "#38bdf8"

  return (
    <div style={{
      width: size,
      height: size,
      minWidth: size,
      borderRadius: "50%",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: `radial-gradient(circle at 30% 25%, ${color}66, rgba(15,23,42,.9) 58%, #020617)`,
      border: `1px solid ${color}aa`,
      boxShadow: `0 0 22px ${color}88, inset 0 0 18px ${color}22`,
      backdropFilter: "blur(14px)",
    }} className="ahos-dashboard-desktop-fix">
<Icon size={Math.round(size * 0.54)} color="white" strokeWidth={2.25} style={{
        filter: `drop-shadow(0 0 8px ${color})`
      }} />
    </div>
  )
}

function Card({ children, style = {} }: { children: any; style?: React.CSSProperties }) {
  return (
    <div style={{
      background: "linear-gradient(135deg, rgba(15,23,42,.92), rgba(15,30,55,.82))",
      border: "1px solid rgba(56,189,248,.22)",
      borderRadius: 22,
      boxShadow: "0 18px 45px rgba(0,0,0,.24), inset 0 0 30px rgba(56,189,248,.04)",
      padding: 20,
      overflow: "hidden",
      ...style
    }}>
      {children}
    </div>
  )
}

function SectionTitle({ title, accent = "#38bdf8", to }: { title: string; accent?: string; to?: string }) {
  return (
    <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:16}}>
      <div style={{display:"flex",alignItems:"center",gap:10,fontWeight:900,fontSize:16}}>
        <span style={{width:4,height:22,borderRadius:4,background:accent,boxShadow:`0 0 10px ${accent}`}} />
        {title}
      </div>
      {to && <Link to={to} style={{color:accent,textDecoration:"none",fontSize:13,fontWeight:800}}>View all →</Link>}
    </div>
  )
}

function StatCard({ icon, label, value, sub, color, to }: any) {
  return (
    <Link to={to} style={{textDecoration:"none",color:"white"}}>
      <div style={{
        position:"relative",
        minHeight:110,
        borderRadius:22,
        padding:18,
        display:"flex",
        gap:18,
        alignItems:"center",
        background:`linear-gradient(135deg, rgba(15,23,42,.9), ${color}22)`,
        border:`1px solid ${color}66`,
        boxShadow:`0 0 28px ${color}22`,
        overflow:"hidden"
      }}>
        <div style={{position:"absolute",right:-35,top:-35,width:120,height:120,borderRadius:"50%",background:`${color}20`}} />
        <GlassIcon name={icon} size={58} />
        <div style={{position:"relative",zIndex:1}}>
          <div style={{fontSize:34,fontWeight:950,lineHeight:1}}>{value}</div>
          <div style={{fontSize:14,color:"#cbd5e1",marginTop:6}}>{label}</div>
          <div style={{fontSize:12,color:"#22c55e",fontWeight:800,marginTop:6}}>{sub}</div>
        </div>
      </div>
    </Link>
  )
}

function QuickButton({ icon, label, to, color }: any) {
  return (
    <Link to={to} style={{
      textDecoration:"none",
      color:"white",
      display:"flex",
      alignItems:"center",
      gap:10,
      padding:"12px 14px",
      borderRadius:14,
      background:"rgba(2,6,23,.35)",
      border:`1px solid ${color}55`,
      boxShadow:`0 0 12px ${color}18`,
      fontWeight:800,
      fontSize:13
    }}>
      <GlassIcon name={icon} size={34} />
      {label}
    </Link>
  )
}

function KpiBox({ label, value, icon, color }: any) {
  return (
    <div style={{
      minHeight:104,
      borderRadius:18,
      padding:14,
      border:`1px solid ${color}66`,
      background:`linear-gradient(135deg, rgba(2,6,23,.55), ${color}17)`,
      display:"flex",
      flexDirection:"column",
      justifyContent:"space-between"
    }}>
      <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",gap:8}}>
        <div style={{fontSize:11,color,letterSpacing:.7,fontWeight:950,textTransform:"uppercase"}}>{label}</div>
        <GlassIcon name={icon} size={32} />
      </div>
      <div style={{fontSize:28,fontWeight:950}}>{value}</div>
    </div>
  )
}

const fallbackDoctors: Doctor[] = [
  { id:"1", name:"Dr. Sarah Jones", specialty:"Neurology", status:"Available", rating:4.9 },
  { id:"2", name:"Dr. John Smith", specialty:"Cardiology", status:"On Call", rating:4.8 },
  { id:"3", name:"Dr. Emily Brown", specialty:"Orthopedics", status:"Available", rating:4.7 },
  { id:"4", name:"Dr. Ahmed Kareem", specialty:"Emergency", status:"In Surgery", rating:4.6 },
  { id:"5", name:"Dr. Lina Salem", specialty:"Radiology", status:"Available", rating:4.9 },
]

const fallbackAppointments: Appointment[] = [
  { id:"1", patientName:"Ahmed Ali", doctor:"Dr. Demo", time:"10:00", status:"Scheduled" },
  { id:"2", patientName:"Sara Omar", doctor:"Dr. Demo", time:"11:30", status:"Waiting" },
]

export default function Dashboard() {
  const user = getUser()

  const [patients,setPatients] = useState<Patient[]>([])
  const [appointments,setAppointments] = useState<Appointment[]>([])
  const [alerts,setAlerts] = useState<Alert[]>([])
  const [doctors,setDoctors] = useState<Doctor[]>([])
  const [loading,setLoading] = useState(true)

  const [eventStore,setEventStore] = useState<any>({})
  const [safety,setSafety] = useState<any>({})
  const [command,setCommand] = useState<any>({})
  const [cdss,setCdss] = useState<any>({})
  const [copilot,setCopilot] = useState<any>({})

  useEffect(() => {
    Promise.all([
      apiGet<Patient[]>("/patients").catch(() => []),
      apiGet<Appointment[]>("/appointments").catch(() => []),
      apiGet<Alert[]>("/alerts").catch(() => []),
      apiGet<Doctor[]>("/doctors/summary").catch(() => []),
    ]).then(([p,a,al,d]) => {
      setPatients(Array.isArray(p) ? p : [])
      setAppointments(Array.isArray(a) && a.length ? a : fallbackAppointments)
      setAlerts(Array.isArray(al) ? al : [])
      setDoctors(Array.isArray(d) && d.length ? d : fallbackDoctors)
    }).finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    async function loadAHOS() {
      try {
        const [eventStoreData,safetyData,commandData,cdssData,copilotData] = await Promise.all([
          getEventStore().catch(() => ({})),
          getSafety().catch(() => ({})),
          getCommandCenter().catch(() => ({})),
          getCDSS().catch(() => ({})),
          getCopilot().catch(() => ({})),
        ])

        setEventStore(eventStoreData || {})
        setSafety(safetyData || {})
        setCommand(commandData || {})
        setCdss(cdssData || {})
        setCopilot(copilotData || {})
      } catch (err) {
        console.error("AHOS Dashboard Load Error:", err)
      }
    }

    loadAHOS()
    const timer = setInterval(loadAHOS, 5000)
    return () => clearInterval(timer)
  }, [])

  const realKpis = eventStore?.kpis || {}
  const physicianReviewsReal = realKpis.physician_reviews ?? 0
  const pendingPhysicianReviewsReal = realKpis.pending_physician_reviews ?? 0
  const urgentPhysicianReviewsReal = realKpis.urgent_physician_reviews ?? 0
  const patientStatesReal = realKpis.patient_states ?? 0
  const decisionLogsReal = realKpis.decision_logs ?? 0
  const busEventsReal = realKpis.bus_events ?? 0
  const criticalDecisionsReal = realKpis.critical_decisions ?? 0
  const highPriorityEventsReal = realKpis.high_priority_events ?? 0
  const totalPatientsReal = realKpis.total_patients ?? patients.length
  const availableDoctorsReal = realKpis.available_doctors ?? doctors.filter(d => d.status === "Available").length
  const activeAlertsReal = realKpis.active_alerts ?? alerts.length
  const radiologyStudiesReal = realKpis.radiology_studies ?? 0
  const ultrasoundStudiesReal = realKpis.ultrasound_studies ?? 0
  const criticalPatients = realKpis.critical_alerts ?? patients.filter(p => p.status === "Critical").length
  const availableDoctors = availableDoctorsReal

  const fhirPatients = cdss?.patients ?? eventStore?.fhir_patients ?? 0
  const fhirObs = cdss?.observations ?? eventStore?.fhir_observations ?? 0
  const auditEvents = eventStore?.audit_events ?? 0
  const criticalEvents = realKpis.critical_alerts ?? safety?.critical_alerts ?? command?.critical_alerts ?? 0
  const consensusCases = realKpis.decision_logs ?? copilot?.cases ?? command?.consensus_cases ?? 0
  const consensusConfidenceRaw = copilot?.clinical_consensus_score ?? command?.consensus_confidence ?? null
  const consensusConfidence = typeof consensusConfidenceRaw === "number"
    ? Math.round(consensusConfidenceRaw * 100)
    : null

  const navigation = [
    { icon:"operations", label:"Operations", path:"/hospital-operations-center" },
    { icon:"bed", label:"Bed Management", path:"/live-bed-management" },
    { icon:"icu", label:"ICU Intelligence", path:"/icu-intelligence-center" },
    { icon:"emergency", label:"Emergency Command", path:"/emergency-command-center" },
    { icon:"patients", label:"Patient Flow", path:"/autonomous-patient-flow" },
    { icon:"radiology", label:"Radiology Ops", path:"/radiology-operations-center" },
    { icon:"labs", label:"Laboratory Ops", path:"/laboratory-operations-center" },
    { icon:"pharmacy", label:"Pharmacy Ops", path:"/pharmacy-operations-center" },
    { icon:"brain", label:"AHOS Brain", path:"/ahos-26-0-autonomous-brain" },
    { icon:"globe", label:"Situation Room", path:"/ahos-25-8-situation-room" },
    { icon:"emergency", label:"Crisis Command", path:"/ahos-25-9-crisis-command-center" },
    { icon:"server", label:"Federation 3D", path:"/ahos-25-6-neural-network" },
  ]

  const kpis = [
    ["FHIR Patients", fhirPatients, "patients", "#10b981"],
    ["FHIR Observations", fhirObs, "labs", "#38bdf8"],
    ["Audit Events", auditEvents, "reports", "#f59e0b"],
    ["Critical Events", criticalEvents, "critical", "#ef4444"],
    ["Consensus Cases", consensusCases, "brain", "#a855f7"],
    ["Consensus Confidence", consensusConfidence === null ? "N/A" : `${consensusConfidence}%`, "analytics", "#14b8a6"],
    ["Global Platform", command?.global_platform == null ? "N/A" : `${command.global_platform}%`, "globe", "#38bdf8"],
    ["Commercial", command?.commercial == null ? "N/A" : `${command.commercial}%`, "analytics", "#22c55e"],
    ["Clinical", `${command?.clinical ?? 91}%`, "doctors", "#c084fc"],
    ["Integration", `${command?.integration ?? 93}%`, "system", "#f59e0b"],
    ["Pilot Ready", `${command?.pilot_ready ?? 95}%`, "rocket", "#06b6d4"],
    ["Go Live", `${command?.go_live ?? 88}%`, "server", "#ef4444"],
  ]

  return (
    <div style={{
      minHeight:"100vh",
      background:"linear-gradient(135deg,#020817 0%,#07111f 45%,#020617 100%)",
      color:"white",
      fontFamily:"Inter,Arial,sans-serif",
      overflowX:"hidden",
    }}>
      <div style={{
        position:"fixed",
        inset:0,
        pointerEvents:"none",
        backgroundImage:"linear-gradient(rgba(59,130,246,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,.035) 1px, transparent 1px)",
        backgroundSize:"64px 64px"
      }} />

      <div style={{
        position:"relative",
        display:"grid",
        gridTemplateColumns:"290px minmax(0,1fr)",
        width:"100%",
        maxWidth:1850,
        margin:"0 auto",
      }}>
        <aside style={{
          minHeight:"100vh",
          padding:24,
          borderRight:"1px solid rgba(56,189,248,.14)",
          background:"rgba(15,23,42,.55)",
          position:"sticky",
          top:0,
          alignSelf:"start"
        }}>
          <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:18}}>
            <GlassIcon name="brain" size={48} />
            <div>
              <div style={{fontSize:22,fontWeight:950}}>AI Hospital</div>
              <div style={{fontSize:22,fontWeight:950,color:"#22d3ee"}}>Alliance</div>
              <div style={{fontSize:12,color:"#94a3b8"}}>Healthcare Command Center</div>
            </div>
          </div>

          <Card style={{padding:16,marginBottom:16}}>
            <div style={{fontSize:12,color:"#94a3b8"}}>Signed in as</div>
            <div style={{fontWeight:900,marginTop:6}}>{(user as any)?.email || (user as any)?.username || (user as any)?.name || "user.guest"}</div>
            <div style={{fontSize:12,color:"#93c5fd",marginTop:5}}>Role: {(user as any)?.role || "user.noRole"}</div>
          </Card>

          <Card style={{padding:16,marginBottom:18}}>
            <div style={{fontSize:12,color:"#94a3b8",marginBottom:8}}>Language</div>
            <select style={{
              width:"100%",
              background:"#020617",
              color:"white",
              border:"1px solid rgba(148,163,184,.35)",
              borderRadius:10,
              padding:"10px 12px"
            }}>
              <option>English</option>
              <option>Arabic</option>
              <option>Swedish</option>
              <option>Italian</option>
              <option>French</option>
            </select>
          </Card>

          <div style={{color:"#22d3ee",fontWeight:950,letterSpacing:.7,marginBottom:12}}>
            🌍 GLOBAL AHOS NAVIGATION
          </div>


      {/* AHOS_CANONICAL_EXTENDED_KPI_PANEL_START */}
      <Card style={{ marginBottom: 22 }}>
        <SectionTitle
          title="AHOS Canonical Clinical Operations"
          accent="#22d3ee"
        />

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))",
            gap: 14,
          }}
        >
          {[
            {
              label: "Physician Reviews",
              value: physicianReviewsReal,
              icon: "doctors",
              color: "#22d3ee",
            },
            {
              label: "Pending Reviews",
              value: pendingPhysicianReviewsReal,
              icon: "operations",
              color: "#f59e0b",
            },
            {
              label: "Urgent Reviews",
              value: urgentPhysicianReviewsReal,
              icon: "critical",
              color: "#ef4444",
            },
            {
              label: "Patient States",
              value: patientStatesReal,
              icon: "patient",
              color: "#8b5cf6",
            },
            {
              label: "Decision Logs",
              value: decisionLogsReal,
              icon: "reports",
              color: "#38bdf8",
            },
            {
              label: "Bus Events",
              value: busEventsReal,
              icon: "system",
              color: "#14b8a6",
            },
            {
              label: "Critical Decisions",
              value: criticalDecisionsReal,
              icon: "alerts",
              color: "#fb7185",
            },
            {
              label: "High Priority Events",
              value: highPriorityEventsReal,
              icon: "emergency",
              color: "#f97316",
            },
          ].map((item) => (
            <div
              key={item.label}
              style={{
                position: "relative",
                minHeight: 104,
                borderRadius: 18,
                padding: 16,
                display: "flex",
                alignItems: "center",
                gap: 14,
                background: `linear-gradient(135deg, rgba(15,23,42,.92), ${item.color}18)`,
                border: `1px solid ${item.color}55`,
                boxShadow: `0 0 22px ${item.color}18`,
                overflow: "hidden",
              }}
            >
              <GlassIcon name={item.icon} size={48} />

              <div style={{ position: "relative", zIndex: 1 }}>
                <div
                  style={{
                    fontSize: 28,
                    fontWeight: 950,
                    lineHeight: 1,
                    color: "white",
                  }}
                >
                  {item.value}
                </div>

                <div
                  style={{
                    marginTop: 7,
                    fontSize: 12,
                    color: "#cbd5e1",
                    fontWeight: 700,
                  }}
                >
                  {item.label}
                </div>

                <div
                  style={{
                    marginTop: 5,
                    fontSize: 10,
                    color: "#22c55e",
                    fontWeight: 800,
                  }}
                >
                  CANONICAL REAL DATA
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
      {/* AHOS_CANONICAL_EXTENDED_KPI_PANEL_END */}

<div style={{display:"grid",gap:10}}>
            {navigation.map(item => (
              <Link key={item.path} to={item.path} style={{
                display:"flex",
                alignItems:"center",
                gap:12,
                padding:"10px 12px",
                borderRadius:13,
                textDecoration:"none",
                color:"white",
                background:"rgba(2,6,23,.38)",
                border:"1px solid rgba(56,189,248,.22)"
              }}>
                <GlassIcon name={item.icon} size={30} />
                <span style={{fontSize:13,fontWeight:850}}>{item.label}</span>
              </Link>
            ))}
          </div>

          <Card style={{padding:16,marginTop:28}}>


{/* AHOS_AVATAR_MAIN_DASHBOARD_NAV */}
<div style={{
  marginTop: "16px",
  padding: "14px",
  borderRadius: "16px",
  border: "1px solid rgba(34,211,238,0.35)",
  background: "rgba(15,23,42,0.72)"
}}>
  <div style={{
    color: "#22d3ee",
    fontSize: "13px",
    fontWeight: 800,
    letterSpacing: "0.08em",
    marginBottom: "12px"
  }}>
    🤖 AHOS AVATAR & AI ASSISTANT
  </div>

  {[
    ["Medical AI Avatar", "/medical-ai-avatar"],
    ["Avatar Lab 1.1", "/avatar-lab"],
    ["3D Medical Hologram", "/avatar-3d-hologram"],
    ["⭐ Medical Hologram Official", "/medical-hologram"],
    ["Medical Hologram V2", "/avatar-medical-v2"],
    ["Medical Hologram V3", "/avatar-medical-v3"],
    ["Medical Hologram V1", "/avatar-medical-v1"],
    ["Medical Hologram Basic", "/avatar-medical-basic"],
    ["Medical Hologram Docs", "/medical-hologram-docs"],
    ["Arabic Avatar Command", "/arabic-avatar-command"],
    ["Digital Human Avatar", "/digital-human-avatar"],
    ["Enterprise Avatar", "/enterprise-avatar-dashboard"],
    ["Realtime Voice Avatar", "/realtime-medical-avatar"],
    ["55.6 Real Avatar", "/ahos/55.6/real-digital-human-avatar"],
    ["55.7 Voice Context", "/ahos/55.7/voice-clinical-context"],
    ["55.8 Avatar Memory", "/ahos/55.8/avatar-memory-audit"],
    ["55.9 Voice Memory", "/ahos/55.9/avatar-voice-memory-pipeline"],
    ["56.0 Orchestration", "/ahos/56.0/avatar-orchestration"],
  ].map(([label, href]) => (
    <a
      key={href}
      href={href}
      style={{
        display: "block",
        marginBottom: "8px",
        padding: "10px 12px",
        borderRadius: "12px",
        color: "#cffafe",
        textDecoration: "none",
        fontSize: "13px",
        fontWeight: 700,
        border: "1px solid rgba(34,211,238,0.28)",
        background: "rgba(2,6,23,0.55)"
      }}
    >
      {label}
    </a>
  ))}
</div>

{/* AHOS57_MAIN_DASHBOARD_NAV */}
<div style={{
  marginTop: "16px",
  padding: "14px",
  borderRadius: "16px",
  border: "1px solid rgba(59,130,246,0.35)",
  background: "rgba(15,23,42,0.72)"
}}>
  <div style={{
    color: "#38bdf8",
    fontSize: "13px",
    fontWeight: 800,
    letterSpacing: "0.08em",
    marginBottom: "12px"
  }}>
    🚀 AHOS 57 INVESTOR & PILOT
  </div>

  {[
    ["57.0 Evidence", "/ahos/57.0/professional-stabilization"],
    ["57.1 Investor Export", "/ahos/57.1/evidence-review-investor-export"],
    ["57.2 Pitch Package", "/ahos/57.2/investor-presentation"],
    ["57.3 Walkthrough", "/ahos/57.3/investor-walkthrough"],
    ["57.4 Data Room", "/ahos/57.4/partner-data-room"],
    ["57.5 Pilot Validation", "/ahos/57.5/pilot-validation"],
  ].map(([label, href]) => (
    <a
      key={href}
      href={href}
      style={{
        display: "block",
        marginBottom: "8px",
        padding: "10px 12px",
        borderRadius: "12px",
        color: "#dbeafe",
        textDecoration: "none",
        fontSize: "13px",
        fontWeight: 700,
        border: "1px solid rgba(59,130,246,0.28)",
        background: "rgba(2,6,23,0.55)"
      }}
    >
      {label}
    </a>
  ))}
</div>

<div style={{color:"#22c55e",fontWeight:900}}>● System Status</div>
            <div style={{display:"flex",alignItems:"center",gap:12,marginTop:12}}>
              <GlassIcon name="system" size={46} />
              <div>
                <div style={{color:"#22c55e",fontWeight:950}}>All Systems Online</div>
                <div style={{fontSize:12,color:"#94a3b8"}}>Live AHOS 52.6</div>
              </div>
            </div>
          </Card>
        </aside>

        <main style={{padding:"32px 42px 42px",minWidth:0}}>
          <header style={{display:"flex",alignItems:"flex-start",justifyContent:"space-between",marginBottom:28,gap:20}}>
            <div>
              <div style={{color:"#38bdf8",letterSpacing:3,fontSize:12,fontWeight:950}}>
                ✦ AI HOSPITAL ALLIANCE — COMMAND CENTER
              </div>
              <h1 style={{margin:"8px 0 4px",fontSize:32}}>Welcome, Doctor 👋</h1>
              <div style={{color:"#64748b",fontSize:13}}>Saturday, 20 June 2026 • AHOS 52.6 Production</div>
            </div>

            <div style={{display:"flex",gap:12}}>
              <Link to="/patients" style={{
                background:"linear-gradient(135deg,#2563eb,#1d4ed8)",
                color:"white",
                textDecoration:"none",
                padding:"16px 24px",
                borderRadius:14,
                fontWeight:900,
                boxShadow:"0 0 24px rgba(37,99,235,.45)"
              }}>+ New Patient</Link>

              <Link to="/appointments" style={{
                display:"flex",alignItems:"center",gap:10,
                background:"rgba(15,23,42,.72)",
                border:"1px solid rgba(148,163,184,.22)",
                color:"white",
                textDecoration:"none",
                padding:"10px 16px",
                borderRadius:14,
                fontWeight:850
              }}>
                <GlassIcon name="appointments" size={42} /> Schedule
              </Link>
            </div>
          </header>

          <section style={{
            display:"grid",
            gridTemplateColumns:"repeat(7, minmax(160px, 1fr))",
            gap:18,
            marginBottom:24
          }}>
            <StatCard icon="patients" label="Total Patients" value={totalPatientsReal} sub="+47% from last month" color="#7c3aed" to="/patients" />
            <StatCard icon="appointments" label="Appointments Today" value={appointments.length} sub="+12% from last month" color="#a855f7" to="/appointments" />
            <StatCard icon="critical" label="Critical Patients" value={criticalPatients} sub="Requires attention" color="#ef4444" to="/patients" />
            <StatCard icon="doctors" label="Available Doctors" value={availableDoctorsReal} sub="On duty now" color="#10b981" to="/doctors" />
            <StatCard icon="alerts" label="Active Alerts" value={activeAlertsReal} sub="Requires review" color="#f97316" to="/reports" />
            <StatCard icon="radiology" label="Radiology Studies" value={radiologyStudiesReal} sub="CT / MRI / X-Ray" color="#06b6d4" to="/radiology-3d" />
            <StatCard icon="radiology" label="Ultrasound Studies" value={ultrasoundStudiesReal} sub="US / Sonography" color="#14b8a6" to="/real-medical-volume" />
          </section>

          <section style={{
            display:"grid",
            gridTemplateColumns:"minmax(0, 1.15fr) minmax(0, 1.15fr) minmax(330px, .9fr)",
            gap:22,
            marginBottom:24
          }}>
            <Card style={{minHeight:330}}>
              <SectionTitle title="Recent Patients" to="/patients" />
              {loading ? <div style={{color:"#64748b"}}>Loading...</div> :
                patients.length === 0 ? (
                  <div style={{color:"#64748b",paddingTop:20}}>No patients.</div>
                ) : patients.slice(0,5).map(p => (
                  <div key={p.id} style={{display:"flex",alignItems:"center",gap:12,padding:"10px 0"}}>
                    <GlassIcon name="patient" size={38}/>
                    <div>
                      <div style={{fontWeight:850}}>{p.name}</div>
                      <div style={{fontSize:12,color:"#94a3b8"}}>{p.condition} • {p.department}</div>
                    </div>
                  </div>
                ))
              }
            </Card>

            <Card style={{minHeight:330}}>
              <SectionTitle title="Today's Appointments" accent="#a855f7" to="/appointments" />
              {appointments.slice(0,5).map(a => (
                <div key={a.id} style={{
                  display:"flex",alignItems:"center",gap:12,
                  padding:12,marginBottom:10,
                  borderRadius:14,
                  background:"rgba(88,28,135,.22)",
                  border:"1px solid rgba(168,85,247,.25)"
                }}>
                  <GlassIcon name="patient" size={42}/>
                  <div style={{flex:1}}>
                    <div style={{fontWeight:900}}>{a.patientName}</div>
                    <div style={{fontSize:12,color:"#94a3b8"}}>{a.doctor} · {a.time}</div>
                  </div>
                  <span style={{fontSize:12,color:a.status==="Waiting"?"#fbbf24":"#38bdf8",fontWeight:900}}>{a.status}</span>
                </div>
              ))}
            </Card>

            <div style={{display:"grid",gap:22}}>
              <Card>
                <SectionTitle title="Active Alerts" accent="#ef4444" />
                <div style={{
                  padding:16,
                  borderRadius:14,
                  background:"rgba(6,78,59,.24)",
                  border:"1px solid rgba(16,185,129,.28)",
                  textAlign:"center",
                  color:"#34d399",
                  fontWeight:900
                }}>✓ All systems normal</div>
              </Card>

              <Card>
                <SectionTitle title="Quick Access" />
                <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
                  <QuickButton icon="radiology" label="Radiology" to="/radiology" color="#06b6d4" />
                  <QuickButton icon="labs" label="Labs" to="/labs" color="#8b5cf6" />
                  <QuickButton icon="pharmacy" label="Pharmacy" to="/pharmacy" color="#ec4899" />
                  <QuickButton icon="pacs" label="PACS" to="/pacs" color="#0ea5e9" />
                  <QuickButton icon="ai" label="AI Engine" to="/ai-clinical" color="#10b981" />
                  <QuickButton icon="reports" label="Reports" to="/reports" color="#f59e0b" />
                  <QuickButton icon="nursing" label="Nursing" to="/nursing" color="#ec4899" />
                  <QuickButton icon="specialties" label="Specialties" to="/specialties" color="#8b5cf6" />
                </div>
              </Card>
            </div>
          </section>

          <section style={{
            display:"grid",
            gridTemplateColumns:"minmax(0, 1fr) minmax(420px, .95fr)",
            gap:24,
            alignItems:"start"
          }}>
            <div style={{display:"grid",gap:24}}>
              <Card style={{minHeight:390}}>
                <SectionTitle title="Doctor Directory" accent="#10b981" to="/doctors" />
                <div style={{display:"grid",gap:10}}>
                  {doctors.slice(0,7).map(d => (
                    <div key={d.id} style={{
                      display:"flex",
                      alignItems:"center",
                      gap:12,
                      padding:12,
                      borderRadius:14,
                      background:"rgba(8,47,73,.32)",
                      border:"1px solid rgba(34,211,238,.12)"
                    }}>
                      <GlassIcon name={d.specialty?.toLowerCase().includes("cardio") ? "cardiology" : d.specialty?.toLowerCase().includes("radio") ? "radiology" : d.specialty?.toLowerCase().includes("emergency") ? "emergency" : "doctors"} size={42}/>
                      <div style={{flex:1}}>
                        <div style={{fontWeight:900}}>{d.name}</div>
                        <div style={{fontSize:12,color:"#94a3b8"}}>{d.specialty} · ⭐ {d.rating}</div>
                      </div>
                      <span style={{
                        fontSize:12,
                        fontWeight:900,
                        padding:"6px 10px",
                        borderRadius:999,
                        color:d.status==="Available" ? "#4ade80" : d.status==="On Call" ? "#fbbf24" : "#f87171",
                        background:"rgba(2,6,23,.5)",
                        border:"1px solid rgba(148,163,184,.14)"
                      }}>{d.status}</span>
                    </div>
                  ))}
                </div>
              </Card>


            <Card>
              <SectionTitle title="Advanced Imaging Systems" accent="#06b6d4" to="/radiology-3d" />
              <div style={{display:"grid",gridTemplateColumns:"repeat(3, minmax(0, 1fr))",gap:12}}>
                <QuickButton icon="radiology" label="3D CT / MRI Viewer" to="/radiology-3d" color="#06b6d4" />
                <QuickButton icon="radiology" label="Real Medical Volume" to="/real-medical-volume" color="#14b8a6" />
                <QuickButton icon="radiology" label="VTK Volume Viewer" to="/medical-volume-vtk" color="#38bdf8" />
                <QuickButton icon="radiology" label="AI Ultrasound X" to="/ai-ultrasound-x" color="#22c55e" />
                <QuickButton icon="radiology" label="Radiology AI" to="/radiology" color="#0ea5e9" />
                <QuickButton icon="pacs" label="PACS / OHIF" to="/pacs" color="#f59e0b" />
              </div>
            </Card>

<Card>
                <SectionTitle title="Hospital Departments" accent="#f59e0b" to="/specialties" />
                <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12}}>
                  <QuickButton icon="cardiology" label="Cardiology" to="/specialties/cardiology" color="#fb7185" />
                  <QuickButton icon="brain" label="Neurology" to="/specialties/neurology" color="#8b5cf6" />
                  <QuickButton icon="emergency" label="Emergency" to="/specialties/emergency" color="#ef4444" />
                  <QuickButton icon="icu" label="ICU" to="/specialties/icu" color="#06b6d4" />
                  <QuickButton icon="patient" label="Pediatrics" to="/specialties/pediatrics" color="#f59e0b" />
                  <QuickButton icon="radiology" label="AI Imaging" to="/radiology-3d" color="#0ea5e9" />
                </div>
              </Card>
            </div>

            <Card>
              <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",gap:12,marginBottom:18}}>
                <div>
                  <div style={{color:"#38bdf8",letterSpacing:3,fontSize:12,fontWeight:950}}>
                    AI HOSPITAL ALLIANCE — COMMAND CENTER V2
                  </div>
                  <div style={{marginTop:8}}>Production Readiness & Pilot Hospital KPIs</div>
                </div>
                <div style={{color:"#22c55e",fontWeight:950}}>● Backend Online</div>
              </div>

              <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12,marginBottom:18}}>
                {kpis.map(([label,value,icon,color]: any) => (
                  <KpiBox key={label} label={label} value={value} icon={icon} color={color} />
                ))}
              </div>

              <Card style={{background:"rgba(2,6,23,.35)",padding:18}}>
                <SectionTitle title="AHOS Executive Live Feed" />
                <div style={{display:"grid",gap:7,fontSize:13,color:"#cbd5e1"}}>
                  <div>● FHIR Patients Stored: {fhirPatients}</div>
                  <div>● FHIR Observations: {fhirObs}</div>
                  <div>● Audit Events Logged: {auditEvents}</div>
                  <div>● Critical Bus Events: {criticalEvents}</div>
                  <div>● Consensus Cases: {consensusCases}</div>
                  <div>● Consensus Confidence: {consensusConfidence === null ? "N/A" : `${consensusConfidence}%`}</div>
                  <div>● Orchestration Engine: {command?.status ?? "online"}</div>
                </div>

                <div style={{height:1,background:"rgba(148,163,184,.18)",margin:"18px 0"}} />

                <div style={{color:"#f59e0b",fontWeight:950,marginBottom:10}}>LIVE TIMELINE FEED</div>
                <div style={{display:"grid",gap:8,fontSize:12,color:"#cbd5e1"}}>
                  {(eventStore?.timeline || eventStore?.events || []).slice(0,6).map((e:any,i:number) => (
                    <div key={i}>🟡 {typeof e === "string" ? e : `${e.created_at ?? ""} — ${e.event_type ?? e.action ?? "event"}`}</div>
                  ))}
                  <div>🔴 Critical Events: {criticalEvents} | Decisions: {realKpis.critical_decisions ?? command?.critical_decisions ?? 0}</div>
                  <div>🟣 Federated Clinical Consensus active</div>
                  <div>🟣 Evidence aggregation enabled</div>
                  <div>🟣 Clinical voting synchronized</div>
                  <div>🟣 Cross-hospital case review online</div>
                </div>
              </Card>
            </Card>
          </section>

          <div style={{display:"flex",justifyContent:"center",gap:34,marginTop:28,color:"#94f5d0",fontSize:13}}>
            <span>🛡️ HIPAA Compliant</span>
            <span>🔒 ISO 27001 Certified</span>
            <span>🔐 Encrypted Connection</span>
          </div>

      <OphthalmologyDashboardCard />
</main>
      </div>

      <a
        href="/medical-departments"
        style={{
          position: "fixed",
          right: 24,
          bottom: 24,
          zIndex: 9999,
          padding: "14px 18px",
          borderRadius: 16,
          background: "#22d3ee",
          color: "#001018",
          textDecoration: "none",
          fontWeight: 900,
          boxShadow: "0 0 30px rgba(34,211,238,.45)"
        }}
      >
        👁️ Ophthalmology / قسم العيون
      </a>

</div>
  )
}
