import { Link, useLocation } from "react-router-dom";

const items = [
  { label: "Dashboard", to: "/dashboard", icon: "🏠" },

  {
    label: "Patients",
    to: "/patients",
    icon: "🧑‍⚕️",
    children: [
      { label: "All Patients", to: "/patients" },
      { label: "Clinical Notes", to: "/notes" },
      { label: "Orders", to: "/orders" },
    ],
  },

  {
    label: "AI Clinical",
    to: "/ai-clinical",
    icon: "🧠",
  },

  {
    label: "Pharmacy",
    to: "/pharmacy",
    icon: "💊",
    children: [
      { label: "FDA Drug Search", to: "/pharmacy" },
      { label: "Medications", to: "/pharmacy/medications" },
      { label: "Interactions", to: "/pharmacy/interactions" },
      { label: "Prescriptions", to: "/pharmacy/prescriptions" },
    ],
  },

  {
    label: "Specialties",
    to: "/specialties",
    icon: "🏥",
    children: [
      { label: "Cardiology", to: "/specialties/cardiology" },
      { label: "Radiology", to: "/specialties/radiology" },
    ],
  },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-72 min-h-screen bg-[#0B1120] text-white p-5">
      <h1 className="text-2xl font-bold mb-8">
        AI Hospital Alliance
      </h1>

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.label}>
            <Link
              to={item.to}
              className={`block p-3 rounded-xl transition ${
                location.pathname === item.to
                  ? "bg-cyan-600"
                  : "bg-white/5 hover:bg-white/10"
              }`}
            >
              <span className="mr-2">{item.icon}</span>
              {item.label}
            </Link>

            {item.children && (
              <div className="ml-6 mt-2 space-y-2">
                {item.children.map((child) => (
                  <Link
                    key={child.to}
                    to={child.to}
                    className="block text-sm text-gray-300 hover:text-white"
                  >
                    • {child.label}
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </aside>
  );
}
