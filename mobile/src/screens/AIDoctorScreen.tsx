import { useState, useRef } from "react"
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  TextInput, KeyboardAvoidingView, Platform, ActivityIndicator,
  Dimensions
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Typography, Spacing, Radius } from "../../constants/theme"
import { getLang } from "../i18n"
import AsyncStorage from "@react-native-async-storage/async-storage"
import { API_URL } from "../api/client"
import { claudeChat } from "../api/client"

const W = Dimensions.get("window").width

type Mode = "triage"|"lab"|"report"|"decision"
type Msg  = { role:"user"|"assistant"; text:string; time:string }

const MODES: { key: Mode; icon: string; label: Record<string,string>; color: string; sys: string }[] = [
  {
    key: "triage", icon: "🩺",
    label: { en:"Smart Triage", ar:"الفرز الذكي", fr:"Triage IA" },
    color: "#EFF6FF",
    sys: "You are an AI medical triage specialist. When a patient describes symptoms: 1) Ask clarifying questions about onset, severity, location, associated symptoms. 2) Assess urgency level: CRITICAL (call 911), URGENT (ER today), SEMI-URGENT (doctor within 24h), NON-URGENT (routine appointment). 3) Always recommend professional medical evaluation. Format responses clearly with urgency level highlighted.",
  },
  {
    key: "lab", icon: "🧬",
    label: { en:"Lab Interpreter", ar:"تفسير التحاليل", fr:"Interprète Labo" },
    color: "#F0FDF4",
    sys: "You are an AI lab result interpreter. When given lab values: 1) Identify each test and its reference range. 2) Flag abnormal values (HIGH/LOW/CRITICAL). 3) Explain what each result means in simple terms. 4) Suggest what conditions might be indicated. 5) Always recommend physician review. Format: structured table-like response with clear categories.",
  },
  {
    key: "report", icon: "📋",
    label: { en:"Report Generator", ar:"توليد التقارير", fr:"Générateur Rapports" },
    color: "#FEF3C7",
    sys: "You are an AI medical report generator. Generate structured medical reports based on provided information. Include: Patient Summary, Chief Complaint, Assessment, Findings, Recommendations, Follow-up plan. Use professional medical terminology while keeping it readable. Add appropriate disclaimers.",
  },
  {
    key: "decision", icon: "🧠",
    label: { en:"Decision Support", ar:"دعم القرار الطبي", fr:"Aide à la Décision" },
    color: "#F5F3FF",
    sys: "You are an AI clinical decision support system for medical professionals. Provide evidence-based guidance on: differential diagnosis, treatment options, drug interactions, clinical guidelines, risk stratification. Always cite considerations and emphasize that final clinical decisions rest with the treating physician. Be concise and clinically relevant.",
  },
]

export default function AIDoctorScreen() {
  const lang = getLang(); const isRTL = lang === "ar"
  const [mode, setMode]       = useState<Mode>("triage")
  const [msgs, setMsgs]       = useState<Msg[]>([])
  const [input, setInput]     = useState("")
  const [loading, setLoading] = useState(false)
  const ref = useRef<ScrollView>(null)

  const currentMode = MODES.find(m => m.key === mode)!

  function now() { const d = new Date(); return `${d.getHours()}:${String(d.getMinutes()).padStart(2,"0")}` }

  function getWelcome() {
    if (mode === "triage")
      return lang==="ar" ? "مرحباً! أنا نظام الفرز الذكي.\n\nصِف أعراضك بالتفصيل وسأساعدك في تقييم مستوى الإلحاح الطبي." : "Hello! I'm the AI Triage System.\n\nDescribe your symptoms in detail and I'll help assess the urgency level."
    if (mode === "lab")
      return lang==="ar" ? "أرسل نتائج تحاليلك وسأشرحها لك بالتفصيل مع تحديد القيم غير الطبيعية." : "Send your lab results and I'll interpret them, highlighting abnormal values and explaining what they mean."
    if (mode === "report")
      return lang==="ar" ? "أرسل معلومات المريض وسأولّد تقريراً طبياً احترافياً." : "Send patient information and I'll generate a professional medical report."
    return lang==="ar" ? "أنا نظام دعم القرار الطبي. كيف يمكنني مساعدتك اليوم؟" : "I'm your Clinical Decision Support system. How can I assist you today?"
  }

  async function send() {
    const msg = input.trim()
    if (!msg || loading) return
    setInput("")

    const um: Msg = { role:"user", text:msg, time:now() }
    const allMsgs = msgs.length === 0
      ? [{ role:"assistant" as const, text:getWelcome(), time:now() }, um]
      : [...msgs, um]
    setMsgs(allMsgs)
    setLoading(true)
    setTimeout(() => ref.current?.scrollToEnd({ animated:true }), 100)

    try {
      const data = await claudeChat(msg, currentMode.key, lang, allMsgs.slice(-12).map(m => ({ role:m.role, content:m.text })))
      setMsgs(p => [...p, { role:"assistant", text:data.response ?? data.message ?? "Processing...", time:now() }])
    } catch {
      setMsgs(p => [...p, { role:"assistant", text:lang==="ar"?"عذراً، حدث خطأ. حاول مرة أخرى.":"Connection error. Please try again.", time:now() }])
    }
    setLoading(false)
    setTimeout(() => ref.current?.scrollToEnd({ animated:true }), 100)
  }

  function startMode(m: Mode) {
    setMode(m)
    setMsgs([])
    setInput("")
    const welcome = MODES.find(x => x.key === m)
    if (welcome) {
      const wm: Msg = { role:"assistant", text:getWelcomeForMode(m), time:now() }
      setMsgs([wm])
    }
  }

  function getWelcomeForMode(m: Mode) {
    if (m === "triage")   return lang==="ar" ? "مرحباً! صِف أعراضك وسأساعدك في تقييم مستوى الإلحاح الطبي." : "Hello! Describe your symptoms and I'll assess urgency level."
    if (m === "lab")      return lang==="ar" ? "أرسل نتائج تحاليلك للتفسير الفوري." : "Send your lab results for instant interpretation."
    if (m === "report")   return lang==="ar" ? "أرسل بيانات المريض لتوليد تقرير طبي." : "Send patient data to generate a medical report."
    return lang==="ar" ? "كيف يمكنني مساعدتك في دعم القرار الطبي؟" : "How can I assist with clinical decision support?"
  }

  const QUICK: Record<Mode, string[]> = {
    triage:   ["أشعر بألم في الصدر", "I have chest pain", "Douleur thoracique"],
    lab:      ["HbA1c: 8.2, Glucose: 180, Creatinine: 1.4", "CBC: WBC 12.5, RBC 4.2, Hgb 11.8", "Lipid panel: LDL 180, HDL 38, TG 250"],
    report:   ["Patient: 45M, DM Type 2, HTN. Complaint: Fatigue", "Post-op follow-up: Appendectomy 3 days ago", "Chronic case: Asthma, last attack 2 weeks ago"],
    decision: ["Differential for SOB + leg swelling in 60F", "Drug interaction: Warfarin + Aspirin + Metformin", "Risk stratification for acute MI"],
  }

  return (
    <SafeAreaView style={s.safe}>
      {/* Header */}
      <View style={[s.header, { backgroundColor: currentMode.color }]}>
        <Text style={[s.headerTitle, isRTL && s.rtl]}>
          {currentMode.icon} {lang==="ar"?"مساعد طبي AI":lang==="fr"?"Assistant Médical IA":"AI Medical Assistant"}
        </Text>
        <Text style={[s.headerSub, isRTL && s.rtl]}>
          {lang==="ar"?"مدعوم بـ Claude Sonnet":"Powered by Claude Sonnet"}
        </Text>
      </View>

      {/* Mode selector */}
      <View style={s.modeBar}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap:8 }}>
          {MODES.map(m => (
            <TouchableOpacity key={m.key}
              style={[s.modeBtn, mode===m.key && { ...s.modeBtnOn, backgroundColor:m.color, borderColor:Colors.primary }]}
              onPress={() => startMode(m.key)}>
              <Text style={s.modeIcon}>{m.icon}</Text>
              <Text style={[s.modeTxt, mode===m.key && s.modeTxtOn]}>
                {m.label[lang] ?? m.label.en}
              </Text>
            </TouchableOpacity>))}
        </ScrollView>
      </View>

      <KeyboardAvoidingView style={{ flex:1 }} behavior={Platform.OS==="ios"?"padding":undefined}>
        {/* Messages */}
        <ScrollView ref={ref} style={s.msgs} showsVerticalScrollIndicator={false}
          contentContainerStyle={{ padding:14, gap:10 }}
          onContentSizeChange={() => ref.current?.scrollToEnd({ animated:true })}>

          {/* Welcome if no messages */}
          {msgs.length === 0 && (
            <View style={s.welcomeBox}>
              <Text style={{ fontSize:40, textAlign:"center", marginBottom:12 }}>{currentMode.icon}</Text>
              <Text style={[s.welcomeTitle, isRTL && s.rtl]}>{currentMode.label[lang] ?? currentMode.label.en}</Text>
              <Text style={[s.welcomeSub, isRTL && s.rtl]}>{getWelcomeForMode(mode)}</Text>
            </View>)}

          {msgs.map((m, i) => (
            <View key={i} style={[s.mWrap, m.role==="user" ? s.mWrapU : s.mWrapB]}>
              {m.role === "assistant" && (
                <View style={[s.mAvatar, { backgroundColor:currentMode.color }]}>
                  <Text style={{ fontSize:14 }}>{currentMode.icon}</Text>
                </View>)}
              <View style={[s.bubble, m.role==="user" ? s.bubU : s.bubB, { maxWidth:"82%" }]}>
                <Text style={[s.bubTxt, m.role==="user" ? s.bubTxtU : s.bubTxtB, isRTL && s.rtl]}>{m.text}</Text>
                <Text style={[s.bubTime, m.role==="user" && { textAlign:"right" }]}>{m.time}</Text>
              </View>
            </View>))}

          {loading && (
            <View style={s.mWrapB}>
              <View style={[s.mAvatar, { backgroundColor:currentMode.color }]}>
                <Text style={{ fontSize:14 }}>{currentMode.icon}</Text>
              </View>
              <View style={[s.bubble, s.bubB, { paddingVertical:14, paddingHorizontal:20 }]}>
                <ActivityIndicator size="small" color={Colors.primary} />
              </View>
            </View>)}
        </ScrollView>

        {/* Quick prompts */}
        <View style={s.quickBar}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap:8 }}>
            {QUICK[mode].map((q, i) => (
              <TouchableOpacity key={i} style={s.quickBtn} onPress={() => { setInput(q) }}>
                <Text style={[s.quickTxt, isRTL && s.rtl]} numberOfLines={1}>{q}</Text>
              </TouchableOpacity>))}
          </ScrollView>
        </View>

        {/* Input */}
        <View style={[s.inputRow, isRTL && { flexDirection:"row-reverse" }]}>
          <TextInput style={[s.input, isRTL && s.rtl]} value={input} onChangeText={setInput}
            placeholder={lang==="ar"?"اكتب هنا...":lang==="fr"?"Tapez ici...":"Type here..."}
            placeholderTextColor="#AAA" multiline maxLength={800}
            onSubmitEditing={send} returnKeyType="send" />
          <TouchableOpacity style={[s.sendBtn, (!input.trim()||loading) && { backgroundColor:Colors.neutral300 }]}
            onPress={send} disabled={!input.trim()||loading} activeOpacity={0.85}>
            <View style={{ width:0, height:0, borderTopWidth:6, borderBottomWidth:6, borderLeftWidth:9, borderTopColor:"transparent", borderBottomColor:"transparent", borderLeftColor:"#FFF", marginLeft:2 }} />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}

const s = StyleSheet.create({
  safe:    { flex:1, backgroundColor:"#F8F8F8" },
  rtl:     { textAlign:"right" },
  header:  { paddingHorizontal:16, paddingVertical:14, borderBottomWidth:1, borderBottomColor:"#EEEEEE" },
  headerTitle:{ fontSize:17, fontWeight:"800", color:"#111" },
  headerSub:  { fontSize:11, color:"#888", fontWeight:"500", marginTop:2 },
  modeBar: { backgroundColor:"#FFF", paddingVertical:10, paddingHorizontal:14, borderBottomWidth:1, borderBottomColor:"#F0F0F0" },
  modeBtn: { flexDirection:"row", alignItems:"center", gap:6, paddingHorizontal:12, paddingVertical:9, borderRadius:20, borderWidth:1.5, borderColor:"#E0E0E0", backgroundColor:"#F8F8F8" },
  modeBtnOn:  { borderWidth:1.5 },
  modeIcon:   { fontSize:16 },
  modeTxt:    { fontSize:11, fontWeight:"700", color:"#666" },
  modeTxtOn:  { color:Colors.primary },
  msgs:    { flex:1, backgroundColor:"#F5F5F5" },
  welcomeBox: { backgroundColor:"#FFF", borderRadius:20, padding:24, margin:8, alignItems:"center", borderWidth:1, borderColor:"#EEEEEE" },
  welcomeTitle:{ fontSize:18, fontWeight:"800", color:"#111", marginBottom:8, textAlign:"center" },
  welcomeSub:  { fontSize:13, color:"#888", textAlign:"center", lineHeight:20, fontWeight:"500" },
  mWrap:   { flexDirection:"row", alignItems:"flex-end", gap:8 },
  mWrapB:  { justifyContent:"flex-start" },
  mWrapU:  { justifyContent:"flex-end" },
  mAvatar: { width:32, height:32, borderRadius:16, alignItems:"center", justifyContent:"center", flexShrink:0 },
  bubble:  { borderRadius:18, paddingHorizontal:14, paddingVertical:10 },
  bubB:    { backgroundColor:"#FFF", borderBottomLeftRadius:4, borderWidth:1, borderColor:"#EEEEEE" },
  bubU:    { backgroundColor:Colors.primary, borderBottomRightRadius:4 },
  bubTxt:  { fontSize:13, lineHeight:20 },
  bubTxtB: { color:"#111" },
  bubTxtU: { color:"#FFF" },
  bubTime: { fontSize:9, marginTop:5, color:"#AAA", fontWeight:"500" },
  quickBar:{ backgroundColor:"#FFF", paddingVertical:8, paddingHorizontal:14, borderTopWidth:1, borderTopColor:"#F0F0F0" },
  quickBtn:{ paddingHorizontal:12, paddingVertical:7, borderRadius:20, borderWidth:1.5, borderColor:Colors.primary3, backgroundColor:Colors.primary2, maxWidth:200 },
  quickTxt:{ fontSize:11, fontWeight:"700", color:Colors.primary },
  inputRow:{ backgroundColor:"#FFF", borderTopWidth:1, borderTopColor:"#F0F0F0", paddingHorizontal:14, paddingVertical:10, flexDirection:"row", alignItems:"flex-end", gap:10 },
  input:   { flex:1, borderWidth:1.5, borderColor:"#E0E0E0", borderRadius:22, paddingHorizontal:16, paddingVertical:10, fontSize:13, color:"#111", maxHeight:120, fontWeight:"500" },
  sendBtn: { width:44, height:44, backgroundColor:Colors.primary, borderRadius:22, alignItems:"center", justifyContent:"center", flexShrink:0 },
})
