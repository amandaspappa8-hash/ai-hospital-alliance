import { useState, useEffect, useCallback } from "react"
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  ActivityIndicator, RefreshControl, Alert, Image, Dimensions
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Typography, Spacing, Radius, statusColor } from "../../constants/theme"
import { getAppointments } from "../api/client"
import { t, getLang } from "../i18n"

const W = Dimensions.get("window").width
const DAYS_SHORT = ["Su","Mo","Tu","We","Th","Fr","Sa"]
const MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

const DOCTOR_PHOTOS = [
  "https://img.freepik.com/free-photo/woman-doctor-wearing-lab-coat-with-stethoscope-isolated_1303-29791.jpg",
  "https://img.freepik.com/free-photo/portrait-smiling-male-doctor_171337-1532.jpg",
  "https://img.freepik.com/free-photo/beautiful-young-female-doctor-looking-camera-office_1301-7807.jpg",
  "https://img.freepik.com/free-photo/doctor-with-his-arms-crossed-white-background_1368-5790.jpg",
]

const MOCK = [
  { id:1, doctor_name:"Cecily Welsh",    specialty:"Dentist",           time:"2:00 PM",  date:"2026-04-17", status:"scheduled", fee:120, photo:DOCTOR_PHOTOS[2] },
  { id:2, doctor_name:"Tony Ware",       specialty:"Endocrinologist",   time:"10:00 AM", date:"2026-04-17", status:"scheduled", fee:150, photo:DOCTOR_PHOTOS[1] },
  { id:3, doctor_name:"Richie Jimenez",  specialty:"Immunologist",      time:"11:30 AM", date:"2026-04-10", status:"completed", fee:90,  photo:DOCTOR_PHOTOS[0] },
  { id:4, doctor_name:"Anisa Whitehead", specialty:"General Practice",  time:"9:00 AM",  date:"2026-04-05", status:"completed", fee:80,  photo:DOCTOR_PHOTOS[3] },
]

export default function AppointmentScreen() {
  const lang = getLang(); const isRTL = lang === "ar"
  const [appts, setAppts]       = useState<any[]>(MOCK)
  const [loading, setLoading]   = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [selDate, setSelDate]   = useState(17)
  const [month, setMonth]       = useState(3) // April
  const [year, setYear]         = useState(2026)
  const [tab, setTab]           = useState<"upcoming"|"history">("upcoming")

  async function load() {
    try { const d = await getAppointments(); if (Array.isArray(d) && d.length > 0) setAppts(d) } catch {}
    setLoading(false)
  }
  useEffect(() => { load() }, [])
  const onRefresh = useCallback(async () => { setRefreshing(true); await load(); setRefreshing(false) }, [])

  // Build calendar
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const calCells = [...Array(firstDay).fill(null), ...Array.from({ length: daysInMonth }, (_, i) => i + 1)]

  // Dots — days that have appointments
  const apptDays = new Set(appts.map(a => {
    const d = new Date(a.date); return d.getMonth() === month ? d.getDate() : -1
  }))

  const upcoming = appts.filter(a => a.status === "scheduled")
  const history  = appts.filter(a => a.status !== "scheduled")
  const shown    = tab === "upcoming" ? upcoming : history

  return (
    <SafeAreaView style={s.safe}>
      {/* Header */}
      <View style={s.header}>
        <View style={[s.headerRow, isRTL && { flexDirection:"row-reverse" }]}>
          <Text style={[s.title, isRTL && s.rtl]}>{t("appointments_title")}</Text>
          <View style={s.countBadge}>
            <Text style={s.countTxt}>{upcoming.length} {t("scheduled_today")}</Text>
          </View>
        </View>
      </View>

      <ScrollView showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 90 }}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primary} />}>

        {/* ── CALENDAR ── matching reference image */}
        <View style={s.calCard}>
          {/* Month nav */}
          <View style={[s.calNav, isRTL && { flexDirection:"row-reverse" }]}>
            <TouchableOpacity style={s.calNavBtn} onPress={() => { if (month > 0) setMonth(m => m-1); else { setMonth(11); setYear(y => y-1) } }}>
              <Text style={s.calNavTxt}>‹</Text>
            </TouchableOpacity>
            <Text style={s.calMonthTxt}>{MONTHS[month]} {year}</Text>
            <TouchableOpacity style={s.calNavBtn} onPress={() => { if (month < 11) setMonth(m => m+1); else { setMonth(0); setYear(y => y+1) } }}>
              <Text style={s.calNavTxt}>›</Text>
            </TouchableOpacity>
          </View>

          {/* Day headers */}
          <View style={s.calDow}>
            {DAYS_SHORT.map(d => <Text key={d} style={s.calDowTxt}>{d}</Text>)}
          </View>

          {/* Day grid */}
          <View style={s.calGrid}>
            {calCells.map((d, i) => {
              if (!d) return <View key={i} style={s.calCell} />
              const isToday   = d === 17 && month === 3
              const isSel     = d === selDate && month === 3
              const hasDot    = apptDays.has(d)
              return (
                <TouchableOpacity key={i} style={[s.calCell, isSel && s.calCellSel, isToday && !isSel && s.calCellToday]} onPress={() => setSelDate(d)}>
                  <Text style={[s.calDayTxt, isSel && s.calDayTxtSel, isToday && !isSel && s.calDayTxtToday]}>{d}</Text>
                  {hasDot && <View style={[s.calDot, { backgroundColor: isSel ? "#fff" : Colors.primary }]} />}
                </TouchableOpacity>)
            })}
          </View>
        </View>

        {/* ── UPCOMING / HISTORY TABS ── */}
        <View style={s.tabs}>
          {(["upcoming","history"] as const).map(tb => (
            <TouchableOpacity key={tb} style={[s.tabBtn, tab === tb && s.tabBtnOn]} onPress={() => setTab(tb)}>
              <Text style={[s.tabTxt, tab === tb && s.tabTxtOn]}>
                {tb === "upcoming" ? `Upcoming ${upcoming.length > 0 ? upcoming.length : ""}` : "History"}
              </Text>
            </TouchableOpacity>))}
        </View>

        {/* ── APPOINTMENT LIST ── matching reference */}
        {loading ? <ActivityIndicator color={Colors.primary} style={{ paddingVertical:20 }} /> :
          shown.length === 0 ? (
            <View style={s.empty}>
              <Text style={s.emptyTxt}>No {tab} appointments</Text>
            </View>
          ) : shown.map((a, i) => {
            const dt = new Date(a.date)
            const photo = a.photo ?? DOCTOR_PHOTOS[i % DOCTOR_PHOTOS.length]
            const sc = statusColor(a.status)
            return (
              <TouchableOpacity key={i} style={s.apptCard} activeOpacity={0.85}>
                {/* Date column */}
                <View style={s.apptDateCol}>
                  <Text style={s.apptDay}>{dt.getDate()}</Text>
                  <Text style={s.apptMonth}>{MONTHS[dt.getMonth()].slice(0,3).toUpperCase()}</Text>
                </View>

                {/* Doctor photo */}
                <Image source={{ uri: photo }} style={s.apptPhoto} resizeMode="cover" />

                {/* Info */}
                <View style={[{ flex:1, minWidth:0 }, isRTL && { alignItems:"flex-end" }]}>
                  <Text style={[s.apptDr, isRTL && s.rtl]} numberOfLines={1}>{a.doctor_name}</Text>
                  <Text style={[s.apptSpec, isRTL && s.rtl]} numberOfLines={1}>{a.specialty}</Text>
                  <Text style={[s.apptTime, isRTL && s.rtl]}>{a.time} · ${a.fee}</Text>
                </View>

                {/* Status + action */}
                <View style={{ alignItems:"flex-end", gap:6 }}>
                  <View style={[s.sBadge, { backgroundColor: sc.bg }]}>
                    <Text style={[s.sTxt, { color: sc.text }]}>{a.status}</Text>
                  </View>
                  {a.status === "scheduled" && (
                    <TouchableOpacity style={s.payBtn} onPress={() => Alert.alert("Payment","Coming soon")}>
                      <Text style={s.payTxt}>{t("pay_now")}</Text>
                    </TouchableOpacity>)}
                </View>
              </TouchableOpacity>)
          })}
      </ScrollView>
    </SafeAreaView>)
}

const s = StyleSheet.create({
  safe:      { flex:1, backgroundColor:"#F8F8F8" },
  rtl:       { textAlign:"right" },
  header:    { backgroundColor:"#FFF", paddingHorizontal:20, paddingTop:12, paddingBottom:14, borderBottomWidth:1, borderBottomColor:"#F0F0F0" },
  headerRow: { flexDirection:"row", justifyContent:"space-between", alignItems:"center" },
  title:     { fontSize:22, fontWeight:"800", color:"#111", letterSpacing:-0.4 },
  countBadge:{ backgroundColor:Colors.primary2, borderRadius:20, paddingHorizontal:12, paddingVertical:5 },
  countTxt:  { fontSize:11, fontWeight:"700", color:Colors.primary },
  calCard:   { backgroundColor:"#FFF", borderRadius:20, margin:16, padding:16, borderWidth:1, borderColor:"#EEEEEE" },
  calNav:    { flexDirection:"row", justifyContent:"space-between", alignItems:"center", marginBottom:14 },
  calNavBtn: { width:32, height:32, borderRadius:16, backgroundColor:"#F5F5F5", alignItems:"center", justifyContent:"center" },
  calNavTxt: { fontSize:18, color:Colors.primary, fontWeight:"700" },
  calMonthTxt:{ fontSize:15, fontWeight:"800", color:"#111" },
  calDow:    { flexDirection:"row", marginBottom:8 },
  calDowTxt: { flex:1, textAlign:"center", fontSize:11, fontWeight:"700", color:"#AAA", letterSpacing:0.3 },
  calGrid:   { flexDirection:"row", flexWrap:"wrap" },
  calCell:   { width:"14.28%", aspectRatio:1, alignItems:"center", justifyContent:"center", borderRadius:8, marginBottom:2 },
  calCellSel:{ backgroundColor:Colors.primary },
  calCellToday:{ borderWidth:2, borderColor:Colors.primary },
  calDayTxt: { fontSize:13, fontWeight:"600", color:"#555" },
  calDayTxtSel:{ color:"#FFF", fontWeight:"800" },
  calDayTxtToday:{ color:Colors.primary, fontWeight:"800" },
  calDot:    { width:4, height:4, borderRadius:2, marginTop:1 },
  tabs:      { flexDirection:"row", marginHorizontal:16, marginBottom:12, backgroundColor:"#FFF", borderRadius:12, padding:4, borderWidth:1, borderColor:"#EEEEEE" },
  tabBtn:    { flex:1, paddingVertical:10, alignItems:"center", borderRadius:10 },
  tabBtnOn:  { backgroundColor:Colors.primary },
  tabTxt:    { fontSize:13, fontWeight:"700", color:"#AAA" },
  tabTxtOn:  { color:"#FFF" },
  apptCard:  { backgroundColor:"#FFF", borderRadius:16, marginHorizontal:16, marginBottom:10, padding:14, flexDirection:"row", alignItems:"center", gap:10, borderWidth:1, borderColor:"#EEEEEE" },
  apptDateCol:{ alignItems:"center", minWidth:38, backgroundColor:Colors.primary2, borderRadius:10, paddingVertical:8 },
  apptDay:   { fontSize:18, fontWeight:"900", color:Colors.primary, lineHeight:20 },
  apptMonth: { fontSize:9, fontWeight:"800", color:Colors.primary, letterSpacing:0.5 },
  apptPhoto: { width:48, height:48, borderRadius:24, borderWidth:2, borderColor:Colors.primary3 },
  apptDr:    { fontSize:13, fontWeight:"800", color:"#111", marginBottom:2 },
  apptSpec:  { fontSize:11, fontWeight:"600", color:Colors.primary, marginBottom:3 },
  apptTime:  { fontSize:11, color:"#888", fontWeight:"500" },
  sBadge:    { borderRadius:20, paddingHorizontal:8, paddingVertical:3 },
  sTxt:      { fontSize:9, fontWeight:"800", textTransform:"capitalize" },
  payBtn:    { backgroundColor:Colors.primary, borderRadius:8, paddingHorizontal:10, paddingVertical:5 },
  payTxt:    { fontSize:10, fontWeight:"800", color:"#FFF" },
  empty:     { alignItems:"center", paddingVertical:40 },
  emptyTxt:  { fontSize:14, color:"#AAA", fontWeight:"600" },
})
