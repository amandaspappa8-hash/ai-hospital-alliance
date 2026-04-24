import { useState, useEffect, useCallback } from "react"
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, TextInput, ActivityIndicator, RefreshControl, Image, Dimensions } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Typography, Spacing, Radius, statusColor } from "../../constants/theme"
import { getDoctors } from "../api/client"
import { t, getLang } from "../i18n"

const W = Dimensions.get("window").width

const DOCTOR_PHOTOS = [
  "https://img.freepik.com/free-photo/woman-doctor-wearing-lab-coat-with-stethoscope-isolated_1303-29791.jpg",
  "https://img.freepik.com/free-photo/portrait-smiling-male-doctor_171337-1532.jpg",
  "https://img.freepik.com/free-photo/beautiful-young-female-doctor-looking-camera-office_1301-7807.jpg",
  "https://img.freepik.com/free-photo/doctor-with-his-arms-crossed-white-background_1368-5790.jpg",
  "https://img.freepik.com/free-photo/pleased-young-female-doctor-wearing-medical-robe-stethoscope-around-neck-standing-with-closed-posture_409827-254.jpg",
  "https://img.freepik.com/free-photo/medium-shot-smiley-doctor-with-crossed-arms_23-2149351574.jpg",
]

const SPECS = ["All","Cardiology","Neurology","Orthopedics","General","Dentistry","Psychology"]

const MOCK = [
  { id:1, name:"Leslie Alexander", specialty:"Headaches & Migraines", status:"available", rating:4.9, patients:250, experience:12, photo:DOCTOR_PHOTOS[0] },
  { id:2, name:"Adam Max",         specialty:"Psychology",            status:"available", rating:4.9, patients:180, experience:8,  photo:DOCTOR_PHOTOS[1] },
  { id:3, name:"Cecily Welsh",     specialty:"Dentistry",             status:"on_call",   rating:4.8, patients:310, experience:15, photo:DOCTOR_PHOTOS[2] },
  { id:4, name:"Jane Cooper",      specialty:"Cardiology",            status:"available", rating:4.9, patients:420, experience:18, photo:DOCTOR_PHOTOS[3] },
  { id:5, name:"Wade Warren",      specialty:"Neurology",             status:"in_surgery",rating:4.7, patients:290, experience:14, photo:DOCTOR_PHOTOS[1] },
  { id:6, name:"Sarah Wilson",     specialty:"Orthopedics",           status:"offline",   rating:4.6, patients:200, experience:10, photo:DOCTOR_PHOTOS[4] },
]

export default function DoctorsScreen() {
  const lang = getLang(); const isRTL = lang === "ar"
  const [search,  setSearch]  = useState("")
  const [filter,  setFilter]  = useState("All")
  const [doctors, setDoctors] = useState<any[]>(MOCK)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  async function load() {
    try {
      const d = await getDoctors()
      if (Array.isArray(d) && d.length > 0) {
        setDoctors(d.map((doc: any, i: number) => ({
          ...doc, photo: doc.photo_url ?? doc.avatar ?? DOCTOR_PHOTOS[i % DOCTOR_PHOTOS.length],
        })))
      }
    } catch {}
    setLoading(false)
  }
  useEffect(() => { load() }, [])
  const onRefresh = useCallback(async () => { setRefreshing(true); await load(); setRefreshing(false) }, [])

  const filtered = doctors.filter(d => {
    const nm = (d.name ?? d.full_name ?? "").toLowerCase()
    const sp = (d.specialty ?? d.specialization ?? "").toLowerCase()
    return (nm.includes(search.toLowerCase()) || sp.includes(search.toLowerCase()))
      && (filter === "All" || sp.includes(filter.toLowerCase()))
  })

  return (
    <SafeAreaView style={s.safe}>
      {/* Header */}
      <View style={s.header}>
        <Text style={[s.title, isRTL && s.rtl]}>{t("find_doctor")}</Text>
        <Text style={[s.sub,   isRTL && s.rtl]}>{filtered.length} {t("specialists")}</Text>
        <View style={[s.searchBox, isRTL && { flexDirection: "row-reverse" }]}>
          <View style={{ width: 16, height: 16, borderRadius: 8, borderWidth: 2, borderColor: "#AAA", marginRight: 8 }} />
          <TextInput style={[s.searchInp, isRTL && s.rtl]} value={search} onChangeText={setSearch}
            placeholder={t("search_doctor")} placeholderTextColor="#AAA" />
          {search.length > 0 && <TouchableOpacity onPress={() => setSearch("")}><Text style={{ fontSize: 20, color: "#AAA" }}>×</Text></TouchableOpacity>}
        </View>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginBottom: 4 }}>
          {SPECS.map(sp => (
            <TouchableOpacity key={sp} style={[s.chip, filter === sp && s.chipOn]} onPress={() => setFilter(sp)}>
              <Text style={[s.chipTxt, filter === sp && s.chipTxtOn]}>{sp}</Text>
            </TouchableOpacity>))}
        </ScrollView>
      </View>

      {loading ? <ActivityIndicator color={Colors.primary} style={{ flex: 1 }} /> : (
        <ScrollView style={{ flex: 1 }} showsVerticalScrollIndicator={false}
          contentContainerStyle={{ padding: 16, paddingBottom: 90 }}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primary} />}>
          {filtered.map((doc, i) => {
            const sc  = statusColor(doc.status ?? "available")
            const nm  = doc.name ?? doc.full_name ?? "Doctor"
            const photo = doc.photo ?? DOCTOR_PHOTOS[i % DOCTOR_PHOTOS.length]
            return (
              <TouchableOpacity key={doc.id ?? i} style={s.card} activeOpacity={0.85}>
                <View style={[s.cardRow, isRTL && { flexDirection: "row-reverse" }]}>
                  {/* Real photo */}
                  <View style={s.photoWrap}>
                    <Image source={{ uri: photo }} style={s.photo} resizeMode="cover" />
                    <View style={[s.statusDot, { backgroundColor: sc.text }]} />
                  </View>
                  {/* Info */}
                  <View style={[{ flex: 1, minWidth: 0 }, isRTL && { alignItems: "flex-end" }]}>
                    <Text style={[s.docName, isRTL && s.rtl]} numberOfLines={1}>Dr. {nm}</Text>
                    <Text style={[s.docSpec, isRTL && s.rtl]} numberOfLines={1}>{doc.specialty ?? doc.specialization}</Text>
                    <View style={[s.metaRow, isRTL && { flexDirection: "row-reverse" }]}>
                      <Text style={s.rating}>★ {(doc.rating ?? 4.8).toFixed(1)}</Text>
                      <View style={s.dot} />
                      <Text style={s.metaTxt}>{doc.patients ?? 200}+ {lang === "ar" ? "مريض" : "pts"}</Text>
                      <View style={s.dot} />
                      <Text style={s.metaTxt}>{doc.experience ?? 10}{lang === "ar" ? "سنة" : "yr"}</Text>
                    </View>
                    <View style={[s.badge, { backgroundColor: sc.bg }]}>
                      <Text style={[s.badgeTxt, { color: sc.text }]}>{t(doc.status ?? "available")}</Text>
                    </View>
                  </View>
                </View>
                {/* Action buttons */}
                <View style={[s.actions, isRTL && { flexDirection: "row-reverse" }]}>
                  <TouchableOpacity style={s.bookBtn}><Text style={s.bookTxt}>{t("book_now")}</Text></TouchableOpacity>
                  <TouchableOpacity style={s.vidBtn}><Text style={s.vidTxt}>{t("video_call")}</Text></TouchableOpacity>
                </View>
              </TouchableOpacity>)
          })}
        </ScrollView>
      )}
    </SafeAreaView>
  )
}

const s = StyleSheet.create({
  safe:      { flex: 1, backgroundColor: "#FAFAFA" },
  rtl:       { textAlign: "right" },
  header:    { backgroundColor: "#FFF", paddingHorizontal: 16, paddingTop: 12, paddingBottom: 10, borderBottomWidth: 1, borderBottomColor: "#F0F0F0" },
  title:     { fontSize: 22, fontWeight: "800", color: "#111", letterSpacing: -0.4, marginBottom: 3 },
  sub:       { fontSize: 12, color: "#888", fontWeight: "500", marginBottom: 12 },
  searchBox: { flexDirection: "row", alignItems: "center", backgroundColor: "#F5F5F5", borderRadius: 12, paddingHorizontal: 14, height: 46, marginBottom: 10 },
  searchInp: { flex: 1, fontSize: 13, color: "#111", fontWeight: "500" },
  chip:      { paddingHorizontal: 14, paddingVertical: 7, borderRadius: 20, borderWidth: 1.5, borderColor: "#E0E0E0", backgroundColor: "#FFF", marginRight: 8 },
  chipOn:    { borderColor: Colors.primary, backgroundColor: Colors.primary2 },
  chipTxt:   { fontSize: 11, fontWeight: "700", color: "#888" },
  chipTxtOn: { color: Colors.primary },
  card:      { backgroundColor: "#FFF", borderRadius: 16, borderWidth: 1, borderColor: "#EEEEEE", padding: 14, marginBottom: 10 },
  cardRow:   { flexDirection: "row", alignItems: "center", gap: 14, marginBottom: 12 },
  photoWrap: { position: "relative" },
  photo:     { width: 70, height: 70, borderRadius: 35, borderWidth: 2.5, borderColor: Colors.primary3 },
  statusDot: { width: 13, height: 13, borderRadius: 7, position: "absolute", bottom: 1, right: 1, borderWidth: 2.5, borderColor: "#FFF" },
  docName:   { fontSize: 15, fontWeight: "800", color: "#111", marginBottom: 3 },
  docSpec:   { fontSize: 12, fontWeight: "600", color: Colors.primary, marginBottom: 6 },
  metaRow:   { flexDirection: "row", alignItems: "center", gap: 5, flexWrap: "wrap", marginBottom: 8 },
  rating:    { fontSize: 11, fontWeight: "700", color: "#F59E0B" },
  dot:       { width: 3, height: 3, borderRadius: 1.5, backgroundColor: "#CCC" },
  metaTxt:   { fontSize: 11, color: "#888", fontWeight: "500" },
  badge:     { borderRadius: 20, paddingHorizontal: 10, paddingVertical: 3, alignSelf: "flex-start" },
  badgeTxt:  { fontSize: 10, fontWeight: "800" },
  actions:   { flexDirection: "row", gap: 10 },
  bookBtn:   { flex: 1, backgroundColor: Colors.primary, borderRadius: 10, paddingVertical: 11, alignItems: "center" },
  bookTxt:   { fontSize: 12, fontWeight: "800", color: "#FFF", letterSpacing: 0.3 },
  vidBtn:    { flex: 1, borderWidth: 1.5, borderColor: Colors.primary, borderRadius: 10, paddingVertical: 11, alignItems: "center" },
  vidTxt:    { fontSize: 12, fontWeight: "800", color: Colors.primary, letterSpacing: 0.3 },
})
