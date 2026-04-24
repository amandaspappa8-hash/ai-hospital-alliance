import { useState, useRef, useCallback } from "react"
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  TextInput, KeyboardAvoidingView, Platform, ActivityIndicator, Dimensions
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Typography, Spacing, Radius } from "../../constants/theme"
import { t, getLang } from "../i18n"
import { API_URL } from "../api/client"
import AsyncStorage from "@react-native-async-storage/async-storage"

const W = Dimensions.get("window").width

type Msg = { role:"user"|"assistant"; text:string; time:string; type?:"triage"|"report"|"normal" }

const QUICK_ACTIONS = [
  { key:"triage",  icon:"🩺", label:{ en:"AI Triage",       ar:"الفرز الذكي",    fr:"Triage IA"      }},
  { key:"lab",     icon:"🧬", label:{ en:"Lab Results",      ar:"تفسير التحاليل", fr:"Résultats Labo" }},
  { key:"report",  icon:"📋", label:{ en:"Generate Report",  ar:"توليد تقرير",    fr:"Générer Rapport"}},
  { key:"rx",      icon:"💊", label:{ en:"Medications",      ar:"الأدوية",        fr:"Médicaments"    }},
]

const SUGGESTED = ["q1","q2","q3","q4"]

export default function ChatbotScreen() {
  const lang = getLang(); const isRTL = lang === "ar"
  const [msgs, setMsgs] = useState<Msg[]>([{
    role:"assistant",
    text: lang==="ar"
      ? "مرحباً! أنا CareBot، مساعدك الطبي الذكي المدعوم بـ Claude Sonnet.\n\nيمكنني مساعدتك في:\n• فرز الأعراض (AI Triage)\n• تفسير نتائج التحاليل\n• توليد التقارير الطبية\n• دعم القرار الطبي\n\nكيف يمكنني مساعدتك اليوم؟"
      : lang==="fr"
      ? "Bonjour! Je suis CareBot, votre assistant médical IA.\n\nJe peux vous aider avec:\n• Triage IA des symptômes\n• Interpréter les résultats de laboratoire\n• Générer des rapports médicaux\n• Support de décision médicale"
      : "Hello! I'm CareBot, your AI medical assistant powered by Claude Sonnet.\n\nI can help you with:\n• AI Symptom Triage\n• Interpreting lab results\n• Generating medical reports\n• Medical decision support\n\nHow can I help you today?",
    time: now(),
  }])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [activeAction, setActiveAction] = useState<string|null>(null)
  const ref = useRef<ScrollView>(null)

  function now() { const d = new Date(); return `${d.getHours()}:${String(d.getMinutes()).padStart(2,"0")}` }

  const send = useCallback(async (text?: string, actionKey?: string) => {
    const msg = text ?? input.trim()
    if (!msg || loading) return
    setInput("")
    if (actionKey) setActiveAction(actionKey)

    const um: Msg = { role:"user", text:msg, time:now() }
    const nm = [...msgs, um]
    setMsgs(nm)
    setLoading(true)
    setTimeout(() => ref.current?.scrollToEnd({ animated:true }), 100)

    try {
      const token = await AsyncStorage.getItem("aiha_token")
      const systemPrompt = actionKey === "triage"
        ? "You are an AI medical triage assistant. Assess symptoms, ask follow-up questions, and provide urgency level (Critical/Urgent/Non-urgent). Always recommend seeing a doctor."
        : actionKey === "lab"
        ? "You are a medical lab interpreter. Explain lab results in simple terms, highlight abnormal values, and suggest next steps."
        : actionKey === "report"
        ? "You are a medical report generator. Create structured medical reports based on patient information provided."
        : "You are CareBot, an AI medical assistant. Provide helpful medical information while always recommending professional consultation."

      const res = await fetch(`${API_URL}/chatbot/chat`, {
        method:"POST",
        headers:{ "Content-Type":"application/json", ...(token?{Authorization:`Bearer ${token}`}:{}) },
        body: JSON.stringify({
          message: msg,
          language: lang,
          system: systemPrompt,
          history: nm.slice(-10).map(m => ({ role:m.role, content:m.text })),
        }),
      })
      const data = await res.json()
      const reply = data.response ?? data.message ?? data.reply ?? "I'm here to help. Could you provide more details?"
      setMsgs(p => [...p, { role:"assistant", text:reply, time:now(), type:actionKey as any }])
    } catch {
      setMsgs(p => [...p, {
        role:"assistant",
        text: lang==="ar" ? "عذراً، حدث خطأ. يرجى المحاولة مرة أخرى." : "Sorry, there was a connection error. Please try again.",
        time: now(),
      }])
    } finally {
      setLoading(false)
      setActiveAction(null)
      setTimeout(() => ref.current?.scrollToEnd({ animated:true }), 100)
    }
  }, [input, msgs, loading, lang])

  return (
    <SafeAreaView style={s.safe}>
      {/* Header */}
      <View style={s.header}>
        <View style={s.headerLeft}>
          <View style={s.botAvatar}>
            <View style={{ width:20, height:16, backgroundColor:"rgba(255,255,255,0.9)", borderRadius:4, alignItems:"center", justifyContent:"center" }}>
              <View style={{ flexDirection:"row", gap:3 }}>
                <View style={{ width:3, height:3, borderRadius:1.5, backgroundColor:Colors.primary }} />
                <View style={{ width:3, height:3, borderRadius:1.5, backgroundColor:Colors.primary }} />
              </View>
            </View>
          </View>
          <View>
            <Text style={s.headerTitle}>{t("chatbot_title")}</Text>
            <View style={{ flexDirection:"row", alignItems:"center", gap:5 }}>
              <View style={{ width:6, height:6, borderRadius:3, backgroundColor:"#4ADE80" }} />
              <Text style={s.headerSub}>{t("chatbot_online")}</Text>
            </View>
          </View>
        </View>
        <TouchableOpacity style={s.clearBtn} onPress={() => setMsgs([])}>
          <Text style={s.clearTxt}>Clear</Text>
        </TouchableOpacity>
      </View>

      {/* Quick Actions — AI features */}
      <View style={s.quickActions}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap:8 }}>
          {QUICK_ACTIONS.map(a => (
            <TouchableOpacity key={a.key}
              style={[s.qaBtn, activeAction === a.key && s.qaBtnOn]}
              onPress={() => send(`Help me with: ${(a.label as any)[lang] ?? (a.label as any).en}`, a.key)}>
              <Text style={s.qaIcon}>{a.icon}</Text>
              <Text style={[s.qaTxt, activeAction === a.key && s.qaTxtOn]}>
                {(a.label as any)[lang] ?? (a.label as any).en}
              </Text>
            </TouchableOpacity>))}
        </ScrollView>
      </View>

      <KeyboardAvoidingView style={{ flex:1 }} behavior={Platform.OS==="ios"?"padding":undefined}>
        {/* Messages */}
        <ScrollView ref={ref} style={s.msgs} showsVerticalScrollIndicator={false}
          contentContainerStyle={{ padding:14, gap:10 }}
          onContentSizeChange={() => ref.current?.scrollToEnd({ animated:true })}>
          {msgs.map((m, i) => (
            <View key={i} style={[s.mWrap, m.role==="user" ? s.mWrapU : s.mWrapB]}>
              {m.role==="assistant" && (
                <View style={s.mAvatar}>
                  <View style={{ width:12, height:10, backgroundColor:Colors.primary, borderRadius:5, borderBottomLeftRadius:2 }} />
                </View>)}
              <View style={[s.bubble, m.role==="user" ? s.bubU : s.bubB, { maxWidth:"80%" }]}>
                <Text style={[s.bubTxt, m.role==="user" ? s.bubTxtU : s.bubTxtB, isRTL && s.rtl]}>
                  {m.text}
                </Text>
                <Text style={[s.bubTime, m.role==="user" && { textAlign:"right" }]}>{m.time}</Text>
              </View>
            </View>))}
          {loading && (
            <View style={s.mWrapB}>
              <View style={s.mAvatar}>
                <View style={{ width:12, height:10, backgroundColor:Colors.primary, borderRadius:5, borderBottomLeftRadius:2 }} />
              </View>
              <View style={[s.bubble, s.bubB, { paddingVertical:14, paddingHorizontal:20 }]}>
                <ActivityIndicator size="small" color={Colors.primary} />
              </View>
            </View>)}
        </ScrollView>

        {/* Suggested questions */}
        {msgs.length < 3 && (
          <View style={s.sugWrap}>
            <Text style={[s.sugLabel, isRTL && s.rtl]}>{t("suggested")}</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap:8 }}>
              {SUGGESTED.map(k => (
                <TouchableOpacity key={k} style={s.sugBtn} onPress={() => send(t(k))}>
                  <Text style={[s.sugTxt, isRTL && s.rtl]}>{t(k)}</Text>
                </TouchableOpacity>))}
            </ScrollView>
          </View>)}

        {/* Input */}
        <View style={[s.inputRow, isRTL && { flexDirection:"row-reverse" }]}>
          <TextInput style={[s.input, isRTL && s.rtl]} value={input} onChangeText={setInput}
            placeholder={t("type_here")} placeholderTextColor="#AAA"
            multiline maxLength={500}
            onSubmitEditing={() => send()} returnKeyType="send" />
          <TouchableOpacity style={[s.sendBtn, (!input.trim()||loading) && { backgroundColor:Colors.neutral300 }]}
            onPress={() => send()} disabled={!input.trim()||loading} activeOpacity={0.85}>
            <View style={{ width:0, height:0, borderTopWidth:6, borderBottomWidth:6, borderLeftWidth:9, borderTopColor:"transparent", borderBottomColor:"transparent", borderLeftColor:"#FFF", marginLeft:2 }} />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>)
}

const s = StyleSheet.create({
  safe:   { flex:1, backgroundColor:"#F8F8F8" },
  rtl:    { textAlign:"right" },
  header: { backgroundColor:Colors.primary, paddingHorizontal:16, paddingVertical:12, flexDirection:"row", alignItems:"center", justifyContent:"space-between" },
  headerLeft:  { flexDirection:"row", alignItems:"center", gap:10 },
  botAvatar:   { width:40, height:40, backgroundColor:"rgba(255,255,255,0.2)", borderRadius:20, alignItems:"center", justifyContent:"center" },
  headerTitle: { fontSize:15, fontWeight:"800", color:"#FFF" },
  headerSub:   { fontSize:10, color:"rgba(255,255,255,0.8)", fontWeight:"500" },
  clearBtn:    { backgroundColor:"rgba(255,255,255,0.15)", borderRadius:10, paddingHorizontal:12, paddingVertical:6 },
  clearTxt:    { fontSize:11, fontWeight:"700", color:"#FFF" },
  // Quick action bar
  quickActions:{ backgroundColor:"#FFF", paddingVertical:10, paddingHorizontal:14, borderBottomWidth:1, borderBottomColor:"#F0F0F0" },
  qaBtn:       { flexDirection:"row", alignItems:"center", gap:6, paddingHorizontal:12, paddingVertical:8, borderRadius:20, borderWidth:1.5, borderColor:"#E0E0E0", backgroundColor:"#FAFAFA" },
  qaBtnOn:     { borderColor:Colors.primary, backgroundColor:Colors.primary2 },
  qaIcon:      { fontSize:14 },
  qaTxt:       { fontSize:11, fontWeight:"700", color:"#666" },
  qaTxtOn:     { color:Colors.primary },
  // Messages
  msgs:    { flex:1, backgroundColor:"#F5F5F5" },
  mWrap:   { flexDirection:"row", alignItems:"flex-end", gap:8 },
  mWrapB:  { justifyContent:"flex-start" },
  mWrapU:  { justifyContent:"flex-end" },
  mAvatar: { width:28, height:28, borderRadius:14, backgroundColor:Colors.primary2, alignItems:"center", justifyContent:"center", flexShrink:0 },
  bubble:  { borderRadius:18, paddingHorizontal:14, paddingVertical:10 },
  bubB:    { backgroundColor:"#FFF", borderBottomLeftRadius:4, borderWidth:1, borderColor:"#EEEEEE" },
  bubU:    { backgroundColor:Colors.primary, borderBottomRightRadius:4 },
  bubTxt:  { fontSize:13, lineHeight:20 },
  bubTxtB: { color:"#111" },
  bubTxtU: { color:"#FFF" },
  bubTime: { fontSize:9, marginTop:5, color:"#AAA", fontWeight:"500" },
  // Suggested
  sugWrap:  { backgroundColor:"#FFF", borderTopWidth:1, borderTopColor:"#F0F0F0", paddingVertical:10, paddingHorizontal:14 },
  sugLabel: { fontSize:10, fontWeight:"800", color:"#AAA", letterSpacing:0.5, marginBottom:8, textTransform:"uppercase" },
  sugBtn:   { paddingHorizontal:12, paddingVertical:7, borderRadius:20, borderWidth:1.5, borderColor:Colors.primary3, backgroundColor:Colors.primary2 },
  sugTxt:   { fontSize:11, fontWeight:"700", color:Colors.primary, lineHeight:16 },
  // Input
  inputRow: { backgroundColor:"#FFF", borderTopWidth:1, borderTopColor:"#F0F0F0", paddingHorizontal:14, paddingVertical:10, flexDirection:"row", alignItems:"flex-end", gap:10 },
  input:    { flex:1, borderWidth:1.5, borderColor:"#E0E0E0", borderRadius:22, paddingHorizontal:16, paddingVertical:10, fontSize:13, color:"#111", maxHeight:100, fontWeight:"500" },
  sendBtn:  { width:44, height:44, backgroundColor:Colors.primary, borderRadius:22, alignItems:"center", justifyContent:"center", flexShrink:0 },
})
