import type { ReactNode } from "react"

type Props = {
  icon: ReactNode
  bg?: string
  color?: string
  size?: number
}

export default function SectionIconBadge({
  icon,
  bg = "rgba(255,255,255,0.45)",
  color = "#334155",
  size = 46,
}: Props) {
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: 16,
        background: bg,
        color,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0,
      }}
    >
      {icon}
    </div>
  )
}
