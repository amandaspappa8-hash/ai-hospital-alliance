import { useState } from "react"
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Alert, Switch, Image } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Typography, Spacing, Radius } from "../../constants/theme"
import { useAuth } from "../context/AuthContext"
import { t, setLang, getLang, LANGS } from "../i18n"

export default function ProfileScreen({ navigation }: any) {
  const { user, logout } = useAuth()
  const [lang, setLangState] = useState(getLang())
  const [notifs, setNotifs] = useState(true)
  const isRTL = lang === "ar"

  function switchLang(c: string) { setLang(c as any); setLangState(c as any) }
  function handleLogout() {
    Alert.alert(t("log_out"),
      lang==="ar" ? "هل أنت متأكد؟" : lang==="fr" ? "Voulez-vous vous déconnecter?" : "Are you sure?",
      [{ text: lang==="ar"?"إلغاء":lang==="fr"?"Annuler":"Cancel", style:"cancel" },
       { text: t("log_out"), style:"destructive", onPress: logout }])
  }

  const name  = user?.full_name ?? user?.username ?? "Robertson"
  const role  = user?.role ?? "Medical Staff"
  const email = user?.email ?? "user@carebot.ai"

  // Health stats — from user data or defaults
  const stats = {
    heartRate:  user?.heart_rate  ?? "97",
    spo2:       user?.spo2        ?? "98",
    bloodPress: user?.blood_press ?? "120/80",
    weight:     user?.weight      ?? "72",
    bmi:        user?.bmi         ?? "22.8",
    temp:       user?.temp        ?? "36.8",
  }

  return (
    <SafeAreaView style={s.safe}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom:90 }}>

        {/* Profile header — blue gradient */}
        <View style={s.pHeader}>
          <View style={s.avatarWrap}>
            <View style={s.avatar}>
              <Text style={s.avatarTxt}>{name.charAt(0).toUpperCase()}</Text>
            </View>
          </View>
          <Text style={s.pName}>{name}</Text>
          <View style={s.roleBadge}><Text style={s.roleTxt}>{role}</Text></View>
          <Text style={s.pEmail}>{email}</Text>

          {/* Stats bar */}
          <View style={[s.statsBar, isRTL && { flexDirection:"row-reverse" }]}>
            {[{n:"142",l:lang==="ar"?"موعد":"Appts"},{n:"38",l:lang==="ar"?"مريض":"Patients"},{n:"4.9",l:lang==="ar"?"تقييم":"Rating"}].map((it,i) => (
              <View key={i} style={{ flexDirection:"row", alignItems:"center" }}>
                {i > 0 && <View style={s.statDiv} />}
                <View style={s.statItem}>
                  <Text style={s.statNum}>{it.n}</Text>
                  <Text style={s.statLbl}>{it.l}</Text>
                </View>
              </View>))}
          </View>
        </View>

        <View style={s.body}>
          {/* ── HEALTH VITALS ── matching reference health overview */}
          <Text style={[s.secTitle, isRTL && s.rtl]}>
            {lang==="ar"?"المؤشرات الحيوية":lang==="fr"?"Signes Vitaux":"Health Vitals"}
          </Text>
          <View style={s.vitalsGrid}>
            <View style={[s.vitalCard, { borderTopColor:"#EF4444" }]}>
              <View style={[s.vitalIco, { backgroundColor:"#FEE2E2" }]}>
                <View style={{ width:14, height:14, borderRadius:7, borderWidth:2, borderColor:"#EF4444" }} />
              </View>
              <Text style={s.vitalVal}>{stats.heartRate}<Text style={s.vitalUnit}> bpm</Text></Text>
              <Text style={s.vitalLbl}>{lang==="ar"?"معدل القلب":"Heart Rate"}</Text>
            </View>
            <View style={[s.vitalCard, { borderTopColor:Colors.primary }]}>
              <View style={[s.vitalIco, { backgroundColor:Colors.primary2 }]}>
                <View style={{ width:14, height:14, borderRadius:7, borderWidth:2, borderColor:Colors.primary }} />
              </View>
              <Text style={s.vitalVal}>{stats.spo2}<Text style={s.vitalUnit}>%</Text></Text>
              <Text style={s.vitalLbl}>SpO2</Text>
            </View>
            <View style={[s.vitalCard, { borderTopColor:"#10B981" }]}>
              <View style={[s.vitalIco, { backgroundColor:"#D1FAE5" }]}>
                <View style={{ width:14, height:14, borderRadius:7, borderWidth:2, borderColor:"#10B981" }} />
              </View>
              <Text style={s.vitalVal}>{stats.bloodPress}</Text>
              <Text style={s.vitalLbl}>{lang==="ar"?"ضغط الدم":"Blood Press."}</Text>
            </View>
            <View style={[s.vitalCard, { borderTopColor:"#F59E0B" }]}>
              <View style={[s.vitalIco, { backgroundColor:"#FEF3C7" }]}>
                <View style={{ width:14, height:14, borderRadius:7, borderWidth:2, borderColor:"#F59E0B" }} />
              </View>
              <Text style={s.vitalVal}>{stats.temp}<Text style={s.vitalUnit}>°C</Text></Text>
              <Text style={s.vitalLbl}>{lang==="ar"?"الحرارة":"Temp"}</Text>
            </View>
          </View>

          {/* Plan card */}
          <View style={[s.planCard, isRTL && { flexDirection:"row-reverse" }]}>
            <View style={s.planIco}><View style={{ width:20, height:20, borderRadius:10, borderWidth:3, borderColor:"#FFF" }} /></View>
            <View style={{ flex:1 }}>
              <Text style={[s.planTitle, isRTL && s.rtl]}>{t("enterprise_plan")}</Text>
              <Text style={[s.planSub, isRTL && s.rtl]}>Full access · AI Hospital Alliance</Text>
            </View>
            <View style={s.proBadge}><Text style={s.proTxt}>PRO</Text></View>
          </View>

          {/* Language */}
          <Text style={[s.secTitle, isRTL && s.rtl]}>Language</Text>
          <View style={[s.langRow, isRTL && { flexDirection:"row-reverse" }]}>
            {LANGS.map(l => (
              <TouchableOpacity key={l.code} style={[s.langBtn, lang===l.code && s.langOn]} onPress={() => switchLang(l.code)}>
                <Text style={{ fontSize:20 }}>{l.flag}</Text>
                <Text style={[s.langTxt, lang===l.code && s.langTxtOn]}>{l.label}</Text>
              </TouchableOpacity>))}
          </View>

          {/* Account menu */}
          {[
            { title: t("account"), items:[
                lang==="ar"?"تعديل الملف":lang==="fr"?"Modifier profil":"Edit Profile",
                lang==="ar"?"تغيير كلمة المرور":lang==="fr"?"Changer mot de passe":"Change Password",
                lang==="ar"?"السجلات الطبية":lang==="fr"?"Dossiers médicaux":"Medical Records",
              ]},
            { title: t("settings"), items:[
                t("patient_notification"),
                lang==="ar"?"الخصوصية":lang==="fr"?"Confidentialité":"Privacy & Security",
                lang==="ar"?"حول التطبيق":lang==="fr"?"À propos":"About App",
              ]},
          ].map((sec, si) => (
            <View key={si}>
              <Text style={[s.secTitle, isRTL && s.rtl]}>{sec.title}</Text>
              <View style={s.menuCard}>
                {sec.items.map((item, ii) => (
                  <View key={ii} style={[s.menuRow, ii < sec.items.length-1 && s.menuBorder, isRTL && { flexDirection:"row-reverse" }]}>
                    <View style={s.menuIco}><View style={{ width:16, height:16, borderRadius:4, borderWidth:2, borderColor:Colors.primary }} /></View>
                    <Text style={[s.menuTxt, isRTL && s.rtl]}>{item}</Text>
                    {si===1&&ii===0
                      ? <Switch value={notifs} onValueChange={setNotifs} trackColor={{ false:Colors.neutral300, true:Colors.primary3 }} thumbColor={notifs?Colors.primary:"#FFF"} />
                      : <Text style={{ color:"#CCC", fontSize:18 }}>›</Text>}
                  </View>))}
              </View>
            </View>))}

          <TouchableOpacity
            style={{backgroundColor:"#2563EB",borderRadius:14,paddingVertical:14,alignItems:"center",marginBottom:12}}
            onPress={() => (navigation as any).navigate("AI")}
            activeOpacity={0.85}>
            <Text style={{color:"#fff",fontSize:15,fontWeight:"700"}}>🧠 AI Doctor</Text>
          </TouchableOpacity>

          <TouchableOpacity style={s.logoutBtn} onPress={handleLogout} activeOpacity={0.85}>
            <Text style={s.logoutTxt}>{t("log_out")}</Text>
          </TouchableOpacity>
          <Text style={s.ver}>CareBot v1.0.0 · AI Hospital Alliance</Text>
        </View>
      </ScrollView>
    </SafeAreaView>)
}

const s = StyleSheet.create({
  safe:     { flex:1, backgroundColor:"#F8F8F8" },
  rtl:      { textAlign:"right" },
  pHeader:  { backgroundColor:Colors.primary, paddingTop:20, paddingBottom:28, paddingHorizontal:20, alignItems:"center" },
  avatarWrap:{ marginBottom:12 },
  avatar:   { width:80, height:80, borderRadius:40, backgroundColor:"rgba(255,255,255,0.25)", alignItems:"center", justifyContent:"center", borderWidth:3, borderColor:"rgba(255,255,255,0.4)" },
  avatarTxt:{ fontSize:30, fontWeight:"900", color:"#FFF" },
  pName:    { fontSize:20, fontWeight:"800", color:"#FFF", letterSpacing:-0.3, marginBottom:6 },
  roleBadge:{ backgroundColor:"rgba(255,255,255,0.2)", borderRadius:20, paddingHorizontal:14, paddingVertical:4, marginBottom:6 },
  roleTxt:  { fontSize:11, fontWeight:"700", color:"#FFF", textTransform:"capitalize" },
  pEmail:   { fontSize:12, color:"rgba(255,255,255,0.75)", fontWeight:"500" },
  statsBar: { flexDirection:"row", backgroundColor:"rgba(255,255,255,0.15)", borderRadius:14, paddingVertical:12, paddingHorizontal:20, marginTop:16 },
  statDiv:  { width:1, backgroundColor:"rgba(255,255,255,0.3)", marginHorizontal:8 },
  statItem: { flex:1, alignItems:"center" },
  statNum:  { fontSize:18, fontWeight:"900", color:"#FFF" },
  statLbl:  { fontSize:10, fontWeight:"600", color:"rgba(255,255,255,0.75)", marginTop:2 },
  body:     { padding:16 },
  secTitle: { fontSize:12, fontWeight:"800", color:"#AAA", letterSpacing:1, textTransform:"uppercase", marginBottom:10, marginTop:4 },
  // Vitals grid — 2x2
  vitalsGrid:{ flexDirection:"row", flexWrap:"wrap", gap:10, marginBottom:16 },
  vitalCard: { width:"47.5%", backgroundColor:"#FFF", borderRadius:14, padding:14, borderTopWidth:3, borderWidth:1, borderColor:"#EEEEEE" },
  vitalIco:  { width:32, height:32, borderRadius:16, alignItems:"center", justifyContent:"center", marginBottom:8 },
  vitalVal:  { fontSize:22, fontWeight:"900", color:"#111", letterSpacing:-0.5 },
  vitalUnit: { fontSize:12, fontWeight:"600", color:"#888" },
  vitalLbl:  { fontSize:11, color:"#888", fontWeight:"600", marginTop:4 },
  // Plan
  planCard:  { backgroundColor:Colors.primary, borderRadius:14, padding:14, flexDirection:"row", alignItems:"center", gap:12, marginBottom:16 },
  planIco:   { width:38, height:38, backgroundColor:"rgba(255,255,255,0.2)", borderRadius:19, alignItems:"center", justifyContent:"center" },
  planTitle: { fontSize:14, fontWeight:"800", color:"#FFF" },
  planSub:   { fontSize:11, color:"rgba(255,255,255,0.75)", marginTop:1 },
  proBadge:  { backgroundColor:"rgba(255,255,255,0.25)", borderRadius:6, paddingHorizontal:8, paddingVertical:3 },
  proTxt:    { fontSize:11, fontWeight:"900", color:"#FFF", letterSpacing:1 },
  // Language
  langRow:   { flexDirection:"row", gap:8, marginBottom:16 },
  langBtn:   { flex:1, backgroundColor:"#FFF", borderRadius:12, borderWidth:1.5, borderColor:"#E0E0E0", padding:12, alignItems:"center", gap:4 },
  langOn:    { borderColor:Colors.primary, backgroundColor:Colors.primary2 },
  langTxt:   { fontSize:11, fontWeight:"700", color:"#888" },
  langTxtOn: { color:Colors.primary },
  // Menu
  menuCard:  { backgroundColor:"#FFF", borderRadius:14, borderWidth:1, borderColor:"#EEEEEE", overflow:"hidden", marginBottom:16 },
  menuRow:   { flexDirection:"row", alignItems:"center", paddingHorizontal:14, paddingVertical:14, gap:12 },
  menuBorder:{ borderBottomWidth:1, borderBottomColor:"#F5F5F5" },
  menuIco:   { width:34, height:34, backgroundColor:Colors.primary2, borderRadius:10, alignItems:"center", justifyContent:"center" },
  menuTxt:   { flex:1, fontSize:14, fontWeight:"600", color:"#333" },
  logoutBtn: { backgroundColor:"#FEE2E2", borderRadius:14, borderWidth:1.5, borderColor:"#FECACA", paddingVertical:15, alignItems:"center", marginBottom:12 },
  logoutTxt: { fontSize:15, fontWeight:"800", color:Colors.danger },
  ver:       { textAlign:"center", fontSize:11, color:"#BBB", fontWeight:"500" },
})
