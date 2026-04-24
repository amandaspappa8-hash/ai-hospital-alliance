import { useState, useEffect } from "react"
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  Dimensions, ActivityIndicator, Alert
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Typography, Spacing, Radius } from "../../constants/theme"
import { useAuth } from "../context/AuthContext"
import { getLang } from "../i18n"
import AsyncStorage from "@react-native-async-storage/async-storage"
import { API_URL } from "../api/client"

const W = Dimensions.get("window").width

type RecordFile = {
  id: string; type: "xray"|"mri"|"ct"|"lab"|"report"|"other"
  name: string; date: string; size: string; count?: number
  ai_analyzed?: boolean; doctor?: string
}

const FILE_ICONS: Record<string, string> = {
  xray:"🩻", mri:"🧠", ct:"📷", lab:"🧬", report:"📋", other:"📁"
}
const FILE_COLORS: Record<string, string> = {
  xray:"#EFF6FF", mri:"#F5F3FF", ct:"#FFF7ED", lab:"#F0FDF4", report:"#FEF3C7", other:"#F5F5F5"
}
const FILE_STROKE: Record<string, string> = {
  xray:Colors.primary, mri:"#7C3AED", ct:"#EA580C", lab:Colors.success, report:Colors.warning, other:"#888"
}

const MOCK_FILES: RecordFile[] = [
  { id:"1", type:"xray",   name:"X-Ray",             date:"2026-03-15", size:"20.3 MB", count:12, ai_analyzed:true,  doctor:"Dr. Leslie" },
  { id:"2", type:"mri",    name:"MRI Brain",          date:"2026-02-20", size:"85.6 MB", count:48, ai_analyzed:true,  doctor:"Dr. Wade Warren" },
  { id:"3", type:"ct",     name:"CT Scan Chest",      date:"2026-01-10", size:"62.1 MB", count:32, ai_analyzed:false, doctor:"Dr. Jane Cooper" },
  { id:"4", type:"lab",    name:"Blood Test Reports", date:"2026-03-28", size:"17.5 MB", count:5,  ai_analyzed:true,  doctor:"Dr. Adam Max" },
  { id:"5", type:"lab",    name:"All Blood Tests",    date:"2026-02-14", size:"25.6 MB", count:8,  ai_analyzed:true,  doctor:"Lab Center" },
  { id:"6", type:"report", name:"AI Diagnostic Report",date:"2026-04-01",size:"3.2 MB",  count:1,  ai_analyzed:true,  doctor:"CareBot AI" },
  { id:"7", type:"other",  name:"Other Reports",      date:"2026-01-30", size:"11.8 MB", count:6,  ai_analyzed:false, doctor:"Various" },
]

export default function MedicalRecordsScreen() {
  const { user } = useAuth()
  const lang = getLang(); const isRTL = lang === "ar"
  const [files, setFiles]     = useState<RecordFile[]>(MOCK_FILES)
  const [loading, setLoading] = useState(true)
  const [selFile, setSelFile] = useState<RecordFile|null>(null)
  const [view, setView]       = useState<"grid"|"list">("grid")
  const [aiLoading, setAiLoading] = useState(false)
  const [aiResult, setAiResult]   = useState<string|null>(null)

  useEffect(() => {
    loadFiles()
  }, [])

  async function loadFiles() {
    try {
      const token = await AsyncStorage.getItem("aiha_token")
      const res = await fetch(`${API_URL}/medical-records`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const data = await res.json()
      if (Array.isArray(data) && data.length > 0) setFiles(data)
    } catch {}
    setLoading(false)
  }

  async function analyzeWithAI(file: RecordFile) {
    setSelFile(file)
    setAiLoading(true)
    setAiResult(null)
    try {
      const token = await AsyncStorage.getItem("aiha_token")
      const res = await fetch(`${API_URL}/chatbot/chat`, {
        method: "POST",
        headers: { "Content-Type":"application/json", Authorization:`Bearer ${token}` },
        body: JSON.stringify({
          message: `Analyze this medical file: ${file.name} (Type: ${file.type}, Date: ${file.date}, Doctor: ${file.doctor}). Provide a brief AI analysis summary including: key findings, normal/abnormal indicators, and recommended follow-up actions.`,
          language: lang,
          system: "You are an AI medical analyst. Analyze medical records and provide structured, concise reports. Always note that AI analysis is supplementary and professional medical review is required.",
        })
      })
      const data = await res.json()
      setAiResult(data.response ?? data.message ?? "Analysis complete. Please consult your doctor for detailed interpretation.")
    } catch {
      setAiResult(lang==="ar"
        ? "تعذّر الاتصال بنظام التحليل. يرجى المحاولة لاحقاً."
        : "Could not connect to AI analysis. Please try again.")
    }
    setAiLoading(false)
  }

  if (selFile) {
    return (
      <SafeAreaView style={s.safe}>
        <View style={s.fileHeader}>
          <TouchableOpacity onPress={() => { setSelFile(null); setAiResult(null) }} style={s.backBtn}>
            <Text style={s.backTxt}>← {lang==="ar"?"رجوع":lang==="fr"?"Retour":"Back"}</Text>
          </TouchableOpacity>
          <Text style={s.fileHeaderTitle} numberOfLines={1}>{selFile.name}</Text>
        </View>
        <ScrollView style={{ flex:1 }} contentContainerStyle={{ padding:16, paddingBottom:90 }}>
          {/* File info card */}
          <View style={s.fileInfoCard}>
            <View style={[s.fileIconLg, { backgroundColor: FILE_COLORS[selFile.type] }]}>
              <Text style={{ fontSize:36 }}>{FILE_ICONS[selFile.type]}</Text>
            </View>
            <View style={s.fileInfoRows}>
              {[
                { l: lang==="ar"?"النوع":"Type",    v: selFile.type.toUpperCase() },
                { l: lang==="ar"?"الحجم":"Size",    v: selFile.size },
                { l: lang==="ar"?"التاريخ":"Date",  v: selFile.date },
                { l: lang==="ar"?"الطبيب":"Doctor", v: selFile.doctor ?? "—" },
                { l: lang==="ar"?"الملفات":"Files", v: `${selFile.count ?? 1} files` },
              ].map((row,i) => (
                <View key={i} style={[s.infoRow, i>0 && { borderTopWidth:1, borderTopColor:"#F5F5F5" }]}>
                  <Text style={s.infoL}>{row.l}</Text>
                  <Text style={s.infoV}>{row.v}</Text>
                </View>))}
            </View>
          </View>

          {/* AI Analysis section */}
          <View style={s.aiSection}>
            <View style={[s.aiHeader, isRTL && { flexDirection:"row-reverse" }]}>
              <View style={{ flexDirection:"row", alignItems:"center", gap:8 }}>
                <View style={s.aiDot}/>
                <Text style={s.aiTitle}>
                  {lang==="ar"?"تحليل الذكاء الاصطناعي":lang==="fr"?"Analyse IA":"AI Analysis"}
                </Text>
              </View>
              {selFile.ai_analyzed && (
                <View style={s.analyzedBadge}>
                  <Text style={s.analyzedTxt}>✓ {lang==="ar"?"محلَّل":"Analyzed"}</Text>
                </View>)}
            </View>

            {aiLoading ? (
              <View style={s.aiLoading}>
                <ActivityIndicator color={Colors.primary} />
                <Text style={s.aiLoadingTxt}>
                  {lang==="ar"?"جارٍ تحليل الملف...":lang==="fr"?"Analyse en cours...":"Analyzing file with AI..."}
                </Text>
              </View>
            ) : aiResult ? (
              <View style={s.aiResultBox}>
                <Text style={[s.aiResultTxt, isRTL && s.rtl]}>{aiResult}</Text>
                <View style={s.aiDisclaimer}>
                  <Text style={s.aiDisclaimerTxt}>
                    {lang==="ar"
                      ? "⚠️ هذا تحليل AI للمساعدة فقط. استشر طبيبك للتشخيص النهائي."
                      : "⚠️ AI analysis is supplementary. Always consult your doctor for final diagnosis."}
                  </Text>
                </View>
              </View>
            ) : (
              <Text style={[s.aiPrompt, isRTL && s.rtl]}>
                {lang==="ar"
                  ? "اضغط على التحليل الذكي للحصول على تقرير فوري بالذكاء الاصطناعي"
                  : "Press AI Analysis to get an instant AI-powered report for this file"}
              </Text>)}

            <TouchableOpacity style={[s.analyzeBtn, aiLoading && { opacity:0.6 }]}
              onPress={() => analyzeWithAI(selFile)} disabled={aiLoading} activeOpacity={0.85}>
              <Text style={s.analyzeBtnTxt}>
                🧠 {lang==="ar"?"تحليل بالذكاء الاصطناعي":lang==="fr"?"Analyser avec IA":"Analyze with AI"}
              </Text>
            </TouchableOpacity>
          </View>

          {/* Action buttons */}
          <View style={[s.fileActions, isRTL && { flexDirection:"row-reverse" }]}>
            <TouchableOpacity style={s.actionBtnOutline}>
              <Text style={s.actionBtnOutlineTxt}>
                📤 {lang==="ar"?"مشاركة":lang==="fr"?"Partager":"Share"}
              </Text>
            </TouchableOpacity>
            <TouchableOpacity style={s.actionBtnSolid}>
              <Text style={s.actionBtnSolidTxt}>
                👁 {lang==="ar"?"عرض الملف":lang==="fr"?"Voir fichier":"View File"}
              </Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </SafeAreaView>
    )
  }

  return (
    <SafeAreaView style={s.safe}>
      {/* Header */}
      <View style={s.header}>
        <View style={[s.headerRow, isRTL && { flexDirection:"row-reverse" }]}>
          <View>
            <Text style={[s.title, isRTL && s.rtl]}>
              {lang==="ar"?"السجلات الطبية":lang==="fr"?"Dossiers Médicaux":"Medical Records"}
            </Text>
            <Text style={[s.sub, isRTL && s.rtl]}>
              {files.length} {lang==="ar"?"ملف":lang==="fr"?"fichiers":"files"}
            </Text>
          </View>
          <View style={[s.viewToggle, isRTL && { flexDirection:"row-reverse" }]}>
            <TouchableOpacity style={[s.viewBtn, view==="grid" && s.viewBtnOn]} onPress={() => setView("grid")}>
              <Text style={[s.viewBtnTxt, view==="grid" && s.viewBtnTxtOn]}>▦</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[s.viewBtn, view==="list" && s.viewBtnOn]} onPress={() => setView("list")}>
              <Text style={[s.viewBtnTxt, view==="list" && s.viewBtnTxtOn]}>☰</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* AI Summary stats */}
        <View style={[s.aiStats, isRTL && { flexDirection:"row-reverse" }]}>
          <View style={s.aiStatItem}>
            <Text style={s.aiStatNum}>{files.filter(f=>f.ai_analyzed).length}</Text>
            <Text style={s.aiStatLbl}>{lang==="ar"?"محلَّل بـ AI":"AI Analyzed"}</Text>
          </View>
          <View style={s.aiStatDiv}/>
          <View style={s.aiStatItem}>
            <Text style={s.aiStatNum}>{files.filter(f=>f.type==="lab").length}</Text>
            <Text style={s.aiStatLbl}>{lang==="ar"?"تحاليل":"Lab Tests"}</Text>
          </View>
          <View style={s.aiStatDiv}/>
          <View style={s.aiStatItem}>
            <Text style={s.aiStatNum}>{files.filter(f=>["xray","mri","ct"].includes(f.type)).length}</Text>
            <Text style={s.aiStatLbl}>{lang==="ar"?"أشعة":"Imaging"}</Text>
          </View>
          <View style={s.aiStatDiv}/>
          <View style={s.aiStatItem}>
            <Text style={s.aiStatNum}>{files.filter(f=>f.type==="report").length}</Text>
            <Text style={s.aiStatLbl}>{lang==="ar"?"تقارير":"Reports"}</Text>
          </View>
        </View>
      </View>

      {loading ? <ActivityIndicator color={Colors.primary} style={{ flex:1 }} /> : (
        <ScrollView showsVerticalScrollIndicator={false}
          contentContainerStyle={{ padding:16, paddingBottom:90 }}>

          {view === "grid" ? (
            <View style={s.grid}>
              {files.map((f, i) => (
                <TouchableOpacity key={f.id} style={[s.gridCard, { backgroundColor: FILE_COLORS[f.type] }]}
                  onPress={() => analyzeWithAI(f)} activeOpacity={0.85}>
                  {f.ai_analyzed && (
                    <View style={s.aiBadge}><Text style={s.aiBadgeTxt}>AI ✓</Text></View>)}
                  <View style={s.gridMenuDots}><Text style={{ color:"#AAA", fontSize:16 }}>⋯</Text></View>
                  <Text style={{ fontSize:32, marginBottom:8 }}>{FILE_ICONS[f.type]}</Text>
                  <Text style={[s.gridFileName, isRTL && s.rtl]} numberOfLines={2}>{f.name}</Text>
                  <Text style={s.gridFileSub}>{f.count} {lang==="ar"?"ملف":"files"} · {f.size}</Text>
                  {f.doctor && <Text style={[s.gridFileDoc, isRTL && s.rtl]} numberOfLines={1}>{f.doctor}</Text>}
                </TouchableOpacity>))}
            </View>
          ) : (
            files.map((f, i) => (
              <TouchableOpacity key={f.id} style={s.listCard}
                onPress={() => analyzeWithAI(f)} activeOpacity={0.85}>
                <View style={[s.listIcon, { backgroundColor: FILE_COLORS[f.type] }]}>
                  <Text style={{ fontSize:22 }}>{FILE_ICONS[f.type]}</Text>
                </View>
                <View style={{ flex:1, minWidth:0 }}>
                  <View style={[s.listTop, isRTL && { flexDirection:"row-reverse" }]}>
                    <Text style={[s.listName, isRTL && s.rtl]} numberOfLines={1}>{f.name}</Text>
                    {f.ai_analyzed && <View style={s.aiBadgeSmall}><Text style={s.aiBadgeTxt}>AI ✓</Text></View>}
                  </View>
                  <Text style={[s.listSub, isRTL && s.rtl]}>{f.date} · {f.size} · {f.count} files</Text>
                  {f.doctor && <Text style={[s.listDoc, isRTL && s.rtl]} numberOfLines={1}>{f.doctor}</Text>}
                </View>
                <Text style={{ color:"#CCC", fontSize:18 }}>›</Text>
              </TouchableOpacity>))
          )}
        </ScrollView>
      )}
    </SafeAreaView>
  )
}

const CARD_W = (W - 32 - 12) / 2
const s = StyleSheet.create({
  safe:      { flex:1, backgroundColor:"#F8F8F8" },
  rtl:       { textAlign:"right" },
  header:    { backgroundColor:"#FFF", paddingHorizontal:16, paddingTop:12, paddingBottom:12, borderBottomWidth:1, borderBottomColor:"#F0F0F0" },
  headerRow: { flexDirection:"row", justifyContent:"space-between", alignItems:"flex-start", marginBottom:12 },
  title:     { fontSize:22, fontWeight:"800", color:"#111", letterSpacing:-0.4 },
  sub:       { fontSize:12, color:"#888", fontWeight:"500", marginTop:2 },
  viewToggle:{ flexDirection:"row", backgroundColor:"#F5F5F5", borderRadius:10, padding:3 },
  viewBtn:   { width:32, height:28, borderRadius:8, alignItems:"center", justifyContent:"center" },
  viewBtnOn: { backgroundColor:"#FFF" },
  viewBtnTxt:{ fontSize:14, color:"#AAA" },
  viewBtnTxtOn:{ color:Colors.primary },
  aiStats:   { flexDirection:"row", backgroundColor:Colors.primary2, borderRadius:12, paddingVertical:10 },
  aiStatItem:{ flex:1, alignItems:"center" },
  aiStatNum: { fontSize:18, fontWeight:"900", color:Colors.primary },
  aiStatLbl: { fontSize:9, fontWeight:"700", color:Colors.primary, marginTop:2, textAlign:"center" },
  aiStatDiv: { width:1, backgroundColor:Colors.primary3 },
  // Grid
  grid:      { flexDirection:"row", flexWrap:"wrap", gap:12 },
  gridCard:  { width:CARD_W, borderRadius:16, padding:14, position:"relative", minHeight:140 },
  aiBadge:   { position:"absolute", top:10, left:10, backgroundColor:Colors.primary, borderRadius:8, paddingHorizontal:7, paddingVertical:3 },
  aiBadgeSmall:{ backgroundColor:Colors.primary, borderRadius:6, paddingHorizontal:6, paddingVertical:2 },
  aiBadgeTxt:{ fontSize:9, fontWeight:"800", color:"#FFF" },
  gridMenuDots:{ position:"absolute", top:10, right:10 },
  gridFileName:{ fontSize:13, fontWeight:"800", color:"#111", lineHeight:18, marginBottom:4 },
  gridFileSub:{ fontSize:10, color:"#888", fontWeight:"600", marginBottom:3 },
  gridFileDoc:{ fontSize:10, color:Colors.primary, fontWeight:"600" },
  // List
  listCard:  { backgroundColor:"#FFF", borderRadius:14, padding:14, flexDirection:"row", alignItems:"center", gap:12, marginBottom:8, borderWidth:1, borderColor:"#EEEEEE" },
  listIcon:  { width:48, height:48, borderRadius:12, alignItems:"center", justifyContent:"center" },
  listTop:   { flexDirection:"row", alignItems:"center", gap:8, marginBottom:3 },
  listName:  { fontSize:14, fontWeight:"800", color:"#111", flex:1 },
  listSub:   { fontSize:11, color:"#888", fontWeight:"500", marginBottom:2 },
  listDoc:   { fontSize:11, color:Colors.primary, fontWeight:"600" },
  // File detail view
  fileHeader:{ backgroundColor:Colors.primary, paddingHorizontal:16, paddingVertical:14, flexDirection:"row", alignItems:"center", gap:12 },
  backBtn:   { backgroundColor:"rgba(255,255,255,0.2)", borderRadius:10, paddingHorizontal:12, paddingVertical:6 },
  backTxt:   { fontSize:12, fontWeight:"700", color:"#FFF" },
  fileHeaderTitle:{ flex:1, fontSize:16, fontWeight:"800", color:"#FFF" },
  fileInfoCard:{ backgroundColor:"#FFF", borderRadius:16, padding:16, marginBottom:14, borderWidth:1, borderColor:"#EEEEEE" },
  fileIconLg:{ width:70, height:70, borderRadius:18, alignItems:"center", justifyContent:"center", alignSelf:"center", marginBottom:14 },
  fileInfoRows:{ gap:0 },
  infoRow:   { flexDirection:"row", justifyContent:"space-between", paddingVertical:10 },
  infoL:     { fontSize:12, color:"#AAA", fontWeight:"600" },
  infoV:     { fontSize:12, color:"#111", fontWeight:"700" },
  aiSection: { backgroundColor:"#FFF", borderRadius:16, padding:16, marginBottom:14, borderWidth:1, borderColor:"#EEEEEE" },
  aiHeader:  { flexDirection:"row", justifyContent:"space-between", alignItems:"center", marginBottom:12 },
  aiDot:     { width:8, height:8, borderRadius:4, backgroundColor:Colors.primary },
  aiTitle:   { fontSize:15, fontWeight:"800", color:"#111" },
  analyzedBadge:{ backgroundColor:Colors.success1, borderRadius:20, paddingHorizontal:10, paddingVertical:4 },
  analyzedTxt:  { fontSize:10, fontWeight:"800", color:Colors.success },
  aiLoading:    { alignItems:"center", paddingVertical:20, gap:10 },
  aiLoadingTxt: { fontSize:12, color:"#888", fontWeight:"600" },
  aiResultBox:  { backgroundColor:"#F8F8F8", borderRadius:12, padding:14, marginBottom:12 },
  aiResultTxt:  { fontSize:13, color:"#333", lineHeight:20, fontWeight:"500" },
  aiDisclaimer: { marginTop:10, paddingTop:10, borderTopWidth:1, borderTopColor:"#EEE" },
  aiDisclaimerTxt:{ fontSize:10, color:Colors.warning, fontWeight:"600", lineHeight:15 },
  aiPrompt:  { fontSize:12, color:"#AAA", textAlign:"center", paddingVertical:16, lineHeight:18 },
  analyzeBtn:{ backgroundColor:Colors.primary, borderRadius:14, paddingVertical:14, alignItems:"center" },
  analyzeBtnTxt:{ fontSize:14, fontWeight:"800", color:"#FFF", letterSpacing:0.3 },
  fileActions:{ flexDirection:"row", gap:10 },
  actionBtnOutline:{ flex:1, borderWidth:1.5, borderColor:Colors.primary, borderRadius:12, paddingVertical:13, alignItems:"center" },
  actionBtnOutlineTxt:{ fontSize:12, fontWeight:"700", color:Colors.primary },
  actionBtnSolid:{ flex:1, backgroundColor:Colors.primary, borderRadius:12, paddingVertical:13, alignItems:"center" },
  actionBtnSolidTxt:{ fontSize:12, fontWeight:"700", color:"#FFF" },
})
