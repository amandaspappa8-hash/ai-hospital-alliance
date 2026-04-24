import { useState, useEffect, useCallback } from "react"
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  RefreshControl, ActivityIndicator, Dimensions, Image
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Typography, Spacing, Radius, statusColor } from "../../constants/theme"
import { useAuth } from "../context/AuthContext"
import { getDoctors, getAlerts } from "../api/client"
import { t, setLang, getLang, LANGS } from "../i18n"

const W = Dimensions.get("window").width
const CARD_W = W * 0.44

// Real doctor photos — professional medical photos from web
const DOCTOR_PHOTOS = [
  "https://img.freepik.com/free-photo/woman-doctor-wearing-lab-coat-with-stethoscope-isolated_1303-29791.jpg",
  "https://img.freepik.com/free-photo/portrait-smiling-male-doctor_171337-1532.jpg",
  "https://img.freepik.com/free-photo/beautiful-young-female-doctor-looking-camera-office_1301-7807.jpg",
  "https://img.freepik.com/free-photo/doctor-with-his-arms-crossed-white-background_1368-5790.jpg",
  "https://img.freepik.com/free-photo/pleased-young-female-doctor-wearing-medical-robe-stethoscope-around-neck-standing-with-closed-posture_409827-254.jpg",
]

// Fallback: generated avatar if photo fails
function DoctorAvatar({ initials, bg, size = 80 }: { initials: string; bg: string; size?: number }) {
  return (
    <View style={{
      width: size, height: size,
      borderRadius: size / 2,
      backgroundColor: "rgba(255,255,255,0.25)",
      alignItems: "center", justifyContent: "center",
      borderWidth: 2.5, borderColor: "rgba(255,255,255,0.5)",
    }}>
      <Text style={{ fontSize: size * 0.28, fontWeight: "900", color: "#fff" }}>{initials}</Text>
    </View>
  )
}

function FeatIcon({ type }: { type: string }) {
  const c = "#444"
  if (type === "symptom") return (
    <View style={{ width: 30, height: 30, alignItems: "center", justifyContent: "center" }}>
      <View style={{ width: 24, height: 24, borderRadius: 5, borderWidth: 1.8, borderColor: c, alignItems: "center", justifyContent: "center" }}>
        <View style={{ position: "absolute", top: -5, right: 2, width: 9, height: 9, borderRadius: 4.5, borderWidth: 1.8, borderColor: c, backgroundColor: "#F5F5F5" }} />
        <View style={{ width: 11, height: 1.5, backgroundColor: c, marginBottom: 3 }} />
        <View style={{ width: 11, height: 1.5, backgroundColor: c, marginBottom: 3 }} />
        <View style={{ width: 8, height: 1.5, backgroundColor: c }} />
      </View>
    </View>)
  if (type === "teleconsult") return (
    <View style={{ width: 30, height: 30, alignItems: "center", justifyContent: "center" }}>
      <View style={{ width: 22, height: 13, borderTopLeftRadius: 11, borderTopRightRadius: 11, borderWidth: 1.8, borderBottomWidth: 0, borderColor: c }} />
      <View style={{ flexDirection: "row", justifyContent: "space-between", width: 22, marginTop: -1 }}>
        <View style={{ width: 5, height: 7, borderRadius: 2, borderWidth: 1.8, borderColor: c }} />
        <View style={{ width: 5, height: 7, borderRadius: 2, borderWidth: 1.8, borderColor: c }} />
      </View>
    </View>)
  if (type === "insurance") return (
    <View style={{ width: 30, height: 30, alignItems: "center", justifyContent: "center" }}>
      <View style={{ width: 18, height: 22, borderTopLeftRadius: 9, borderTopRightRadius: 9, borderWidth: 1.8, borderColor: c, alignItems: "center", justifyContent: "center" }}>
        <View style={{ width: 8, height: 5, borderLeftWidth: 1.8, borderBottomWidth: 1.8, borderColor: c, transform: [{ rotate: "-45deg" }], marginTop: 3 }} />
      </View>
    </View>)
  if (type === "health") return (
    <View style={{ width: 30, height: 30, alignItems: "center", justifyContent: "center" }}>
      <View style={{ width: 22, height: 22, borderRadius: 11, borderWidth: 1.8, borderColor: c, alignItems: "center", justifyContent: "center" }}>
        <View style={{ width: 12, height: 1.8, backgroundColor: c }} />
        <View style={{ width: 1.8, height: 12, backgroundColor: c, position: "absolute" }} />
      </View>
    </View>)
  if (type === "medication") return (
    <View style={{ width: 30, height: 30, alignItems: "center", justifyContent: "center" }}>
      <View style={{ width: 20, height: 11, borderRadius: 5.5, borderWidth: 1.8, borderColor: c, transform: [{ rotate: "-30deg" }] }}>
        <View style={{ position: "absolute", left: "47%", top: -1, bottom: -1, width: 1.8, backgroundColor: c }} />
      </View>
    </View>)
  if (type === "scan") return (
    <View style={{ width: 30, height: 30, alignItems: "center", justifyContent: "center" }}>
      <View style={{ width: 22, height: 22, alignItems: "center", justifyContent: "center" }}>
        <View style={{ position: "absolute", top: 0, left: 0, width: 7, height: 7, borderTopWidth: 1.8, borderLeftWidth: 1.8, borderColor: c }} />
        <View style={{ position: "absolute", top: 0, right: 0, width: 7, height: 7, borderTopWidth: 1.8, borderRightWidth: 1.8, borderColor: c }} />
        <View style={{ position: "absolute", bottom: 0, left: 0, width: 7, height: 7, borderBottomWidth: 1.8, borderLeftWidth: 1.8, borderColor: c }} />
        <View style={{ position: "absolute", bottom: 0, right: 0, width: 7, height: 7, borderBottomWidth: 1.8, borderRightWidth: 1.8, borderColor: c }} />
        <View style={{ width: 13, height: 1.8, backgroundColor: c }} />
      </View>
    </View>)
  return <View style={{ width: 30, height: 30 }} />
}

const FEATS = [
  { k: "s", type: "symptom",    lbl: { en: "Symptom\nChecker",      ar: "فحص\nالأعراض",    fr: "Vérif.\nSymptômes"  } },
  { k: "t", type: "teleconsult",lbl: { en: "Telecon-\nsultation",   ar: "استشارة\nعن بُعد", fr: "Télé-\nconsult"     } },
  { k: "i", type: "insurance",  lbl: { en: "Insurance\nAssistance", ar: "مساعدة\nالتأمين",  fr: "Assistance\nAssur." } },
  { k: "h", type: "health",     lbl: { en: "Health\nMonitoring",    ar: "مراقبة\nالصحة",    fr: "Santé\nMoniteur"    } },
  { k: "m", type: "medication", lbl: { en: "Medication\nReminders", ar: "تذكير\nالأدوية",   fr: "Rappels\nMédic."    } },
  { k: "r", type: "scan",       lbl: { en: "Scan your\nReport",     ar: "مسح\nتقريرك",      fr: "Scanner\nRapport"   } },
]

const MOCK_DR = [
  { id: 1, name: "Leslie Alexander", specialty: "Headaches And Migraines", rating: 4.9, status: "available", bg: "#3B5BDB", photo: DOCTOR_PHOTOS[0] },
  { id: 2, name: "Dr. Emily Carter",  specialty: "Orthopedics",            rating: 4.8, status: "on_call",   bg: "#5C6BC0", photo: DOCTOR_PHOTOS[2] },
  { id: 3, name: "Dr. Ahmed Karimi",  specialty: "Emergency",              rating: 4.9, status: "available", bg: "#1565C0", photo: DOCTOR_PHOTOS[1] },
  { id: 4, name: "Dr. Sara Wilson",   specialty: "Cardiology",             rating: 4.7, status: "available", bg: "#2962FF", photo: DOCTOR_PHOTOS[4] },
]

export default function HomeScreen() {
  const { user } = useAuth()
  const [lang, setLangState] = useState(getLang())
  const [doctors, setDoctors] = useState<any[]>([])
  const [alerts,  setAlerts]  = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const isRTL = lang === "ar"

  async function load() {
    try {
      const [d, a] = await Promise.all([getDoctors(), getAlerts()])
      if (Array.isArray(d) && d.length > 0) {
        // Attach photos to API doctors
        setDoctors(d.slice(0, 4).map((doc: any, i: number) => ({
          ...doc,
          photo: doc.photo_url ?? doc.avatar ?? DOCTOR_PHOTOS[i % DOCTOR_PHOTOS.length],
          bg: ["#3B5BDB","#5C6BC0","#1565C0","#2962FF"][i % 4],
        })))
      }
      if (Array.isArray(a) && a.length > 0) setAlerts(a.slice(0, 2))
    } catch {}
    setLoading(false)
  }

  useEffect(() => { load() }, [])
  const onRefresh = useCallback(async () => { setRefreshing(true); await load(); setRefreshing(false) }, [])
  function switchLang(c: string) { setLang(c as any); setLangState(c as any) }

  const name  = user?.full_name ?? user?.username ?? "Robertson"
  const shown = doctors.length > 0 ? doctors : MOCK_DR

  return (
    <SafeAreaView style={s.safe}>
      {/* HEADER */}
      <View style={s.header}>
        <View style={[s.hRow, isRTL && { flexDirection: "row-reverse" }]}>
          <View style={{ flex: 1 }}>
            <Text style={[s.h1, isRTL && s.rtl]}>Hello,</Text>
            <Text style={[s.h2, isRTL && s.rtl]}>{name}!</Text>
          </View>
          <TouchableOpacity style={s.bell}>
            <View style={s.bellDot} />
            <View style={{ alignItems: "center" }}>
              <View style={{ width: 15, height: 13, borderTopLeftRadius: 8, borderTopRightRadius: 8, borderWidth: 2, borderBottomWidth: 0, borderColor: "#333" }} />
              <View style={{ width: 19, height: 2.5, backgroundColor: "#333", borderRadius: 1, marginTop: -0.5 }} />
              <View style={{ width: 7, height: 4, borderBottomLeftRadius: 3.5, borderBottomRightRadius: 3.5, borderWidth: 2, borderTopWidth: 0, borderColor: "#333", marginTop: 0.5 }} />
            </View>
          </TouchableOpacity>
        </View>
        <View style={[s.langRow, isRTL && { flexDirection: "row-reverse" }]}>
          {LANGS.map(l => (
            <TouchableOpacity key={l.code} style={[s.langBtn, lang === l.code && s.langOn]} onPress={() => switchLang(l.code)}>
              <Text style={[s.langTxt, lang === l.code && s.langTxtOn]}>{l.flag} {l.code.toUpperCase()}</Text>
            </TouchableOpacity>))}
        </View>
      </View>

      <ScrollView style={s.scroll} showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 100 }}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primary} />}>

        {/* BANNER */}
        <TouchableOpacity style={s.banner} activeOpacity={0.9}>
          <View style={s.banIco}>
            <View style={{ width: 32, height: 28, backgroundColor: "rgba(255,255,255,0.25)", borderRadius: 8, alignItems: "center", justifyContent: "center" }}>
              <View style={{ width: 20, height: 14, backgroundColor: "rgba(255,255,255,0.95)", borderRadius: 4, alignItems: "center", justifyContent: "center" }}>
                <View style={{ flexDirection: "row", gap: 4 }}>
                  <View style={{ width: 4, height: 4, borderRadius: 2, backgroundColor: Colors.primary }} />
                  <View style={{ width: 4, height: 4, borderRadius: 2, backgroundColor: Colors.primary }} />
                </View>
              </View>
            </View>
          </View>
          <View style={{ flex: 1, paddingLeft: 4 }}>
            <Text style={[s.banTitle, isRTL && s.rtl]} numberOfLines={2}>{t("discover_ai")}</Text>
            <Text style={[s.banSub,   isRTL && s.rtl]} numberOfLines={1}>{t("discover_sub")}</Text>
          </View>
          <View style={s.banBtn}>
            <Text style={{ color: "#fff", fontSize: 20, fontWeight: "700", letterSpacing: -3 }}>{"»"}</Text>
          </View>
        </TouchableOpacity>

        {/* OUR FEATURES */}
        <View style={[s.sh, isRTL && { flexDirection: "row-reverse" }]}>
          <Text style={[s.shTitle, isRTL && s.rtl]}>{t("our_features")}</Text>
        </View>
        <View style={s.featGrid}>
          {FEATS.map(f => (
            <TouchableOpacity key={f.k} style={s.featCard} activeOpacity={0.75}>
              <FeatIcon type={f.type} />
              <Text style={[s.featLbl, isRTL && s.rtl]} numberOfLines={2}>
                {(f.lbl as any)[lang] ?? (f.lbl as any).en}
              </Text>
            </TouchableOpacity>))}
        </View>

        {/* APPOINTMENT SCHEDULING */}
        <View style={[s.sh, isRTL && { flexDirection: "row-reverse" }]}>
          <Text style={[s.shTitle, isRTL && s.rtl]}>{t("appointment_scheduling")}</Text>
          <TouchableOpacity><Text style={s.seeAll}>{t("see_all")}</Text></TouchableOpacity>
        </View>

        {loading ? <ActivityIndicator color={Colors.primary} style={{ paddingVertical: 20 }} /> : (
          <ScrollView horizontal showsHorizontalScrollIndicator={false}
            contentContainerStyle={{ paddingHorizontal: 20, gap: 12 }}
            style={{ marginBottom: 20 }}>
            {shown.map((doc, i) => {
              const bg  = doc.bg ?? Colors.primary
              const nm  = doc.name ?? doc.full_name ?? "Doctor"
              const sc  = statusColor(doc.status ?? "available")
              const ini = nm.split(" ").map((w: string) => w[0]).join("").slice(0, 2).toUpperCase()
              const photo = doc.photo ?? DOCTOR_PHOTOS[i % DOCTOR_PHOTOS.length]
              return (
                <TouchableOpacity key={doc.id ?? i} style={[s.docCard, { backgroundColor: bg, width: CARD_W }]} activeOpacity={0.88}>
                  {/* Bookmark icon */}
                  <TouchableOpacity style={s.bookmark}>
                    <View style={{ width: 13, height: 17, borderWidth: 1.5, borderColor: "rgba(255,255,255,0.7)", borderRadius: 3 }} />
                  </TouchableOpacity>

                  {/* Doctor photo — real image from web */}
                  <View style={s.photoWrap}>
                    <Image
                      source={{ uri: photo }}
                      style={s.photo}
                      resizeMode="cover"
                      defaultSource={{ uri: `https://ui-avatars.com/api/?name=${encodeURIComponent(nm)}&background=ffffff&color=${bg.replace("#","")}&size=200&bold=true&font-size=0.4` }}
                    />
                    {/* Status indicator */}
                    <View style={[s.statusDot, { backgroundColor: sc.text }]} />
                  </View>

                  <Text style={[s.docName, isRTL && s.rtl]} numberOfLines={1}>{nm}</Text>
                  <Text style={[s.docSpec, isRTL && s.rtl]} numberOfLines={2}>{doc.specialty ?? doc.specialization}</Text>
                  <View style={{ flexDirection: "row", alignItems: "center", gap: 3, marginTop: 5 }}>
                    <Text style={{ color: "#FFD700", fontSize: 12 }}>★</Text>
                    <Text style={{ color: "#fff", fontSize: 12, fontWeight: "700" }}>{(doc.rating ?? 4.9).toFixed(1)}</Text>
                  </View>
                </TouchableOpacity>
              )
            })}
          </ScrollView>
        )}

        {/* Alerts */}
        {alerts.length > 0 && alerts.map((a, i) => {
          const sc = statusColor(a.severity ?? "active")
          return (
            <TouchableOpacity key={i} style={s.alertCard}>
              <View style={{ width: 9, height: 9, borderRadius: 5, backgroundColor: a.severity === "critical" ? Colors.danger : Colors.warning, marginTop: 3 }} />
              <View style={{ flex: 1 }}>
                <Text style={[{ fontSize: 13, fontWeight: "700", color: "#111" }, isRTL && s.rtl]} numberOfLines={1}>{a.patient_name ?? "Patient"}</Text>
                <Text style={[{ fontSize: 11, color: "#888", marginTop: 2, lineHeight: 16 }, isRTL && s.rtl]} numberOfLines={2}>{a.message ?? a.description}</Text>
              </View>
              <View style={{ borderRadius: 12, paddingHorizontal: 8, paddingVertical: 3, backgroundColor: sc.bg }}>
                <Text style={{ fontSize: 10, fontWeight: "700", color: sc.text }}>{t(a.severity ?? "active")}</Text>
              </View>
            </TouchableOpacity>)
        })}

      </ScrollView>
    </SafeAreaView>
  )
}

const s = StyleSheet.create({
  safe:    { flex: 1, backgroundColor: "#FFFFFF" },
  rtl:     { textAlign: "right" },
  header:  { backgroundColor: "#FFFFFF", paddingHorizontal: 20, paddingTop: 8, paddingBottom: 12, borderBottomWidth: 1, borderBottomColor: "#F2F2F2" },
  hRow:    { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 14 },
  h1:      { fontSize: 32, fontWeight: "400", color: "#111111", lineHeight: 36, letterSpacing: -0.5 },
  h2:      { fontSize: 32, fontWeight: "800", color: "#111111", lineHeight: 38, letterSpacing: -0.5 },
  bell:    { width: 44, height: 44, borderRadius: 22, borderWidth: 1, borderColor: "#DDD", backgroundColor: "#FFF", alignItems: "center", justifyContent: "center" },
  bellDot: { width: 9, height: 9, borderRadius: 5, backgroundColor: Colors.danger, position: "absolute", top: 8, right: 8, zIndex: 2, borderWidth: 2, borderColor: "#FFF" },
  langRow: { flexDirection: "row", gap: 6 },
  langBtn: { flex: 1, paddingVertical: 7, borderRadius: 8, borderWidth: 1.5, borderColor: "#E0E0E0", backgroundColor: "#FFF", alignItems: "center" },
  langOn:  { borderColor: Colors.primary, backgroundColor: Colors.primary2 },
  langTxt: { fontSize: 11, fontWeight: "700", color: "#888" },
  langTxtOn: { color: Colors.primary },
  scroll:  { flex: 1, backgroundColor: "#FFF" },
  banner:  { backgroundColor: Colors.primary, borderRadius: 18, marginHorizontal: 20, marginTop: 16, marginBottom: 24, paddingVertical: 14, paddingHorizontal: 16, flexDirection: "row", alignItems: "center", gap: 12 },
  banIco:  { width: 48, height: 48, backgroundColor: "rgba(255,255,255,0.15)", borderRadius: 14, alignItems: "center", justifyContent: "center" },
  banTitle:{ fontSize: 13, fontWeight: "700", color: "#FFF", lineHeight: 18 },
  banSub:  { fontSize: 11, color: "rgba(255,255,255,0.75)", marginTop: 2 },
  banBtn:  { width: 36, height: 36, borderRadius: 18, backgroundColor: "rgba(255,255,255,0.25)", alignItems: "center", justifyContent: "center" },
  sh:      { flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingHorizontal: 20, marginBottom: 12 },
  shTitle: { fontSize: 18, fontWeight: "800", color: "#111", letterSpacing: -0.4 },
  seeAll:  { fontSize: 13, fontWeight: "600", color: Colors.primary },
  featGrid:{ flexDirection: "row", flexWrap: "wrap", paddingHorizontal: 16, gap: 10, marginBottom: 24 },
  featCard:{ width: (W - 32 - 20) / 3, backgroundColor: "#F5F5F5", borderRadius: 14, paddingVertical: 16, paddingHorizontal: 6, alignItems: "center", gap: 8 },
  featLbl: { fontSize: 10.5, fontWeight: "600", color: "#444", textAlign: "center", lineHeight: 15 },
  // Doctor card — photo takes top half
  docCard:  { borderRadius: 20, overflow: "hidden", minHeight: 220, justifyContent: "flex-end", position: "relative" },
  bookmark: { position: "absolute", top: 12, right: 12, zIndex: 10 },
  photoWrap:{ position: "absolute", top: 0, left: 0, right: 0, height: "58%", overflow: "hidden" },
  photo:    { width: "100%", height: "100%", opacity: 0.9 },
  statusDot:{ width: 12, height: 12, borderRadius: 6, position: "absolute", bottom: 6, right: 8, borderWidth: 2, borderColor: "rgba(255,255,255,0.9)" },
  // Text sits on colored bottom half
  docName:  { fontSize: 13, fontWeight: "800", color: "#FFF", marginBottom: 3, paddingHorizontal: 12, paddingTop: 10 },
  docSpec:  { fontSize: 11, color: "rgba(255,255,255,0.82)", fontWeight: "500", lineHeight: 15, paddingHorizontal: 12, marginBottom: 2 },
  alertCard:{ backgroundColor: "#FFF", borderRadius: 12, borderWidth: 1, borderColor: "#EEE", padding: 14, flexDirection: "row", alignItems: "flex-start", gap: 10, marginHorizontal: 20, marginBottom: 10 },
})
