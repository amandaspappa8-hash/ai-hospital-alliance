import { useState, useRef, useCallback } from "react"
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  TextInput, KeyboardAvoidingView, Platform, ActivityIndicator,
  Dimensions, Alert
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Spacing, Radius, Typography } from "../../constants/theme"
import { getLang } from "../i18n"
import AsyncStorage from "@react-native-async-storage/async-storage"
import { API_URL } from "../api/client"

const W = Dimensions.get("window").width

type Tab = "search"|"interactions"|"rx"|"formulary"
type Msg = { role:"user"|"assistant"; text:string; time:string }

// ── FDA Open API base ─────────────────────────────────
const FDA_API = "https://api.fda.gov/drug"

// ── Drug interaction severity colors ──────────────────
const SEV_COLORS: Record<string,{bg:string;text:string;label:string}> = {
  major:    { bg:"#FEE2E2", text:"#B91C1C", label:"Major" },
  moderate: { bg:"#FEF3C7", text:"#92400E", label:"Moderate" },
  minor:    { bg:"#DCFCE7", text:"#15803D", label:"Minor" },
  unknown:  { bg:"#F1F5F9", text:"#475569", label:"Unknown" },
}

// ── Mock drug data (FDA-style) ─────────────────────────
const MOCK_DRUGS = [
  { name:"Metformin", brand:"Glucophage", class:"Biguanide", dose:"500–2000mg/day", form:"Tablet", indication:"Type 2 Diabetes", fda_approved:true, schedule:"Rx", warnings:["Lactic acidosis risk","Hold before contrast"] },
  { name:"Warfarin",  brand:"Coumadin",   class:"Anticoagulant", dose:"2–10mg/day", form:"Tablet", indication:"DVT/PE, A-Fib", fda_approved:true, schedule:"Rx", warnings:["Bleeding risk","Multiple interactions","INR monitoring required"] },
  { name:"Aspirin",   brand:"Bayer",      class:"NSAID/Antiplatelet", dose:"81–325mg/day", form:"Tablet", indication:"ACS, Pain, Antiplatelet", fda_approved:true, schedule:"OTC", warnings:["GI bleeding","Avoid in children (Reye's)"] },
  { name:"Lisinopril",brand:"Zestril",    class:"ACE Inhibitor", dose:"5–40mg/day", form:"Tablet", indication:"HTN, Heart Failure, CKD", fda_approved:true, schedule:"Rx", warnings:["Angioedema","Avoid in pregnancy","Hyperkalemia"] },
  { name:"Amoxicillin",brand:"Amoxil",   class:"Penicillin", dose:"250–500mg q8h", form:"Capsule", indication:"Bacterial infections", fda_approved:true, schedule:"Rx", warnings:["Allergy check required","C. diff risk"] },
  { name:"Omeprazole",brand:"Prilosec",   class:"PPI", dose:"20–40mg/day", form:"Capsule", indication:"GERD, PUD, H.pylori", fda_approved:true, schedule:"OTC/Rx", warnings:["Long-term: Mg/B12 deficiency","C. diff risk"] },
  { name:"Atorvastatin",brand:"Lipitor",  class:"Statin", dose:"10–80mg/day", form:"Tablet", indication:"Hyperlipidemia, CVD prevention", fda_approved:true, schedule:"Rx", warnings:["Myopathy/rhabdomyolysis","Liver function monitoring"] },
  { name:"Ibuprofen", brand:"Advil",      class:"NSAID", dose:"200–800mg q6h", form:"Tablet", indication:"Pain, Fever, Inflammation", fda_approved:true, schedule:"OTC", warnings:["GI bleeding","Renal toxicity","Avoid in heart failure"] },
]

const INTERACTIONS = [
  { d1:"Warfarin", d2:"Aspirin",    sev:"major",    effect:"Increased bleeding risk. INR may become supratherapeutic.", action:"Avoid combination. If necessary, monitor INR closely and use lowest aspirin dose." },
  { d1:"Warfarin", d2:"Metformin",  sev:"moderate", effect:"Warfarin may increase metformin levels slightly.", action:"Monitor blood glucose and INR more frequently." },
  { d1:"Aspirin",  d2:"Ibuprofen",  sev:"moderate", effect:"Ibuprofen may reduce cardioprotective effect of aspirin.", action:"Take aspirin 30 min before or 8h after ibuprofen." },
  { d1:"Lisinopril",d2:"Ibuprofen", sev:"moderate", effect:"NSAIDs reduce antihypertensive efficacy and increase nephrotoxicity.", action:"Avoid chronic use. Monitor blood pressure and renal function." },
  { d1:"Atorvastatin",d2:"Amoxicillin",sev:"minor", effect:"No significant pharmacokinetic interaction.", action:"No dose adjustment required. Safe to coadminister." },
]

const RX_TEMPLATES = [
  { id:1, name:"Hypertension Protocol",   drugs:["Lisinopril 10mg QD","Amlodipine 5mg QD","Hydrochlorothiazide 12.5mg QD"] },
  { id:2, name:"Diabetes Type 2 Starter", drugs:["Metformin 500mg BID","Empagliflozin 10mg QD","Atorvastatin 20mg QHS"] },
  { id:3, name:"Post-MI Protocol",        drugs:["Aspirin 81mg QD","Clopidogrel 75mg QD","Metoprolol 25mg BID","Atorvastatin 40mg QHS"] },
  { id:4, name:"Community-Acquired Pneumonia",drugs:["Amoxicillin 1g TID x7d","Azithromycin 500mg QD x5d"] },
]

export default function PharmacyScreen() {
  const lang = getLang()
  const isRTL = lang === "ar"
  const [tab, setTab] = useState<Tab>("search")
  const [search, setSearch] = useState("")
  const [selDrug, setSelDrug] = useState<any|null>(null)
  const [drug1, setDrug1] = useState("")
  const [drug2, setDrug2] = useState("")
  const [intResult, setIntResult] = useState<any|null>(null)
  const [aiMsgs, setAiMsgs] = useState<Msg[]>([{
    role:"assistant",
    text: lang==="ar"
      ? "مرحباً! أنا مساعد الصيدلة الذكي.\n\nيمكنني مساعدتك في:\n• البحث عن الأدوية ومعلوماتها\n• التحقق من التفاعلات الدوائية\n• مراجعة الجرعات والموانع\n• الاستفسار عن بيانات FDA\n• كتابة وصفات طبية"
      : "Hello! I'm your AI Pharmacy Assistant.\n\nI can help with:\n• Drug information & dosing\n• Drug interaction checking\n• FDA approvals & warnings\n• Contraindications\n• Prescription writing",
    time: now()
  }])
  const [aiInput, setAiInput] = useState("")
  const [aiLoading, setAiLoading] = useState(false)
  const [fdaLoading, setFdaLoading] = useState(false)
  const [fdaData, setFdaData] = useState<any|null>(null)
  const scrollRef = useRef<ScrollView>(null)

  function now() {
    const d = new Date()
    return `${d.getHours()}:${String(d.getMinutes()).padStart(2,"0")}`
  }

  const filtered = MOCK_DRUGS.filter(d =>
    d.name.toLowerCase().includes(search.toLowerCase()) ||
    d.brand.toLowerCase().includes(search.toLowerCase()) ||
    d.class.toLowerCase().includes(search.toLowerCase()) ||
    d.indication.toLowerCase().includes(search.toLowerCase())
  )

  // Search FDA Open API
  async function searchFDA(drugName: string) {
    setFdaLoading(true)
    setFdaData(null)
    try {
      const res = await fetch(
        `${FDA_API}/label.json?search=openfda.generic_name:"${encodeURIComponent(drugName)}"&limit=1`
      )
      const data = await res.json()
      if (data.results?.[0]) {
        setFdaData(data.results[0])
      }
    } catch {
      // FDA API unavailable — use mock
    }
    setFdaLoading(false)
  }

  // Check drug interaction
  function checkInteraction() {
    if (!drug1.trim() || !drug2.trim()) {
      Alert.alert("", "Please enter two drug names")
      return
    }
    const found = INTERACTIONS.find(i =>
      (i.d1.toLowerCase().includes(drug1.toLowerCase()) && i.d2.toLowerCase().includes(drug2.toLowerCase())) ||
      (i.d1.toLowerCase().includes(drug2.toLowerCase()) && i.d2.toLowerCase().includes(drug1.toLowerCase()))
    )
    if (found) {
      setIntResult(found)
    } else {
      setIntResult({ sev:"unknown", d1:drug1, d2:drug2, effect:"No known interaction found in local database.", action:"Consult full drug interaction database (Lexicomp/Micromedex) and clinical pharmacist." })
    }
  }

  // AI Pharmacy Chat
  const aiChat = useCallback(async (text?: string) => {
    const msg = text ?? aiInput.trim()
    if (!msg || aiLoading) return
    setAiInput("")
    const um: Msg = { role:"user", text:msg, time:now() }
    const newMsgs = [...aiMsgs, um]
    setAiMsgs(newMsgs)
    setAiLoading(true)
    setTimeout(() => scrollRef.current?.scrollToEnd({ animated:true }), 100)

    try {
      const token = await AsyncStorage.getItem("aiha_token")
      const res = await fetch(`${API_URL}/chatbot/chat`, {
        method:"POST",
        headers:{ "Content-Type":"application/json", ...(token ? { Authorization:`Bearer ${token}` } : {}) },
        body: JSON.stringify({
          message: msg,
          language: lang,
          system: `You are an expert AI pharmacy assistant with knowledge of:
- FDA drug database and approval status
- Drug interactions (major/moderate/minor)
- Dosing guidelines for adults, pediatrics, renally impaired
- Pharmacokinetics and pharmacodynamics
- Drug contraindications and warnings
- International drug formularies and pharmacopeias (USP, BP, EP)
- Controlled substance schedules

When answering:
1. Always specify drug class, mechanism, standard dosing
2. Flag BLACK BOX warnings prominently
3. List major interactions
4. Note FDA approval status
5. Include monitoring parameters
6. Always recommend consulting a licensed pharmacist for patient-specific decisions

Format responses clearly with sections when appropriate.`,
          history: newMsgs.slice(-10).map(m => ({ role:m.role, content:m.text })),
        }),
      })
      const data = await res.json()
      setAiMsgs(p => [...p, { role:"assistant", text:data.response ?? data.message ?? "Please try again.", time:now() }])
    } catch {
      setAiMsgs(p => [...p, { role:"assistant", text:lang==="ar"?"عذراً، تعذّر الاتصال. حاول مرة أخرى.":"Connection error. Please try again.", time:now() }])
    }
    setAiLoading(false)
    setTimeout(() => scrollRef.current?.scrollToEnd({ animated:true }), 100)
  }, [aiInput, aiMsgs, aiLoading, lang])

  const QUICK_PROMPTS = [
    "Warfarin dose adjustment for INR 4.2",
    "Metformin contraindications in CKD",
    "Pediatric amoxicillin dosing 20kg child",
    "Statins in pregnancy safety",
    "Max acetaminophen dose per day",
    "Aspirin vs clopidogrel post-stent",
  ]

  // DRUG DETAIL VIEW
  if (selDrug) return (
    <SafeAreaView style={s.safe}>
      <View style={s.drugDetailHdr}>
        <TouchableOpacity style={s.backBtn} onPress={() => { setSelDrug(null); setFdaData(null) }}>
          <Text style={s.backTxt}>← Back</Text>
        </TouchableOpacity>
        <Text style={s.drugDetailTitle} numberOfLines={1}>{selDrug.name}</Text>
        <View style={[s.scheduleBadge, { backgroundColor: selDrug.schedule==="OTC" ? Colors.success1 : Colors.primary2 }]}>
          <Text style={[s.scheduleTxt, { color: selDrug.schedule==="OTC" ? Colors.success : Colors.primary }]}>{selDrug.schedule}</Text>
        </View>
      </View>
      <ScrollView style={{ flex:1 }} contentContainerStyle={{ padding:16, paddingBottom:90 }}>
        {/* Drug header card */}
        <View style={s.drugCard}>
          <View style={[s.drugCardRow, isRTL && { flexDirection:"row-reverse" }]}>
            <View style={s.drugIcoBig}>
              <View style={{ width:28, height:28, borderRadius:14, borderWidth:3, borderColor:Colors.primary, backgroundColor:Colors.primary2 }} />
              <View style={{ position:"absolute", width:20, height:8, borderRadius:4, borderWidth:2, borderColor:Colors.primary, transform:[{rotate:"30deg"}] }} />
            </View>
            <View style={{ flex:1 }}>
              <Text style={[s.drugName, isRTL && s.rtl]}>{selDrug.name}</Text>
              <Text style={[s.drugBrand, isRTL && s.rtl]}>Brand: {selDrug.brand}</Text>
              <Text style={[s.drugClass, isRTL && s.rtl]}>{selDrug.class}</Text>
            </View>
            {selDrug.fda_approved && (
              <View style={s.fdaBadge}>
                <Text style={s.fdaTxt}>FDA ✓</Text>
              </View>
            )}
          </View>

          {/* Info rows */}
          {[
            { l:"Indication",    v:selDrug.indication },
            { l:"Standard Dose", v:selDrug.dose },
            { l:"Dosage Form",   v:selDrug.form },
            { l:"Schedule",      v:selDrug.schedule },
          ].map((row, i) => (
            <View key={i} style={[s.infoRow, i>0 && { borderTopWidth:1, borderTopColor:"#F5F5F5" }]}>
              <Text style={s.infoL}>{row.l}</Text>
              <Text style={s.infoV}>{row.v}</Text>
            </View>
          ))}
        </View>

        {/* Warnings */}
        {selDrug.warnings.length > 0 && (
          <View style={s.warnCard}>
            <View style={[s.warnHdr, isRTL && { flexDirection:"row-reverse" }]}>
              <View style={s.warnDot} />
              <Text style={s.warnTitle}>⚠️ Warnings & Precautions</Text>
            </View>
            {selDrug.warnings.map((w: string, i: number) => (
              <View key={i} style={[s.warnItem, isRTL && { flexDirection:"row-reverse" }]}>
                <View style={s.warnBullet} />
                <Text style={[s.warnTxt, isRTL && s.rtl]}>{w}</Text>
              </View>
            ))}
          </View>
        )}

        {/* FDA Live Data */}
        <TouchableOpacity style={s.fdaBtn} onPress={() => searchFDA(selDrug.name)} activeOpacity={0.85}>
          <Text style={s.fdaBtnTxt}>
            {fdaLoading ? "Loading FDA data..." : "🏛 Fetch FDA Label Data"}
          </Text>
        </TouchableOpacity>
        {fdaLoading && <ActivityIndicator color={Colors.primary} style={{ marginVertical:12 }} />}
        {fdaData && (
          <View style={s.fdaCard}>
            <Text style={s.fdaCardTitle}>FDA Label Data</Text>
            {fdaData.indications_and_usage?.[0] && (
              <View style={s.fdaSection}>
                <Text style={s.fdaSectionTitle}>Indications</Text>
                <Text style={s.fdaSectionTxt} numberOfLines={4}>{fdaData.indications_and_usage[0].replace(/\n/g," ")}</Text>
              </View>
            )}
            {fdaData.warnings?.[0] && (
              <View style={[s.fdaSection, { backgroundColor:"#FEF2F2", borderRadius:8, padding:10, marginTop:8 }]}>
                <Text style={[s.fdaSectionTitle, { color:Colors.danger }]}>FDA Warnings</Text>
                <Text style={[s.fdaSectionTxt, { color:"#7F1D1D" }]} numberOfLines={4}>{fdaData.warnings[0].replace(/\n/g," ")}</Text>
              </View>
            )}
          </View>
        )}

        {/* AI Ask about this drug */}
        <TouchableOpacity style={s.aiAskBtn}
          onPress={() => {
            setSelDrug(null)
            setTab("search")
            setAiInput(`Tell me about ${selDrug.name}: dosing, interactions, and clinical pearls`)
            setTab("search")
            // Switch to AI tab after a beat
            setTimeout(() => setTab("search"), 100)
          }}
          activeOpacity={0.85}>
          <Text style={s.aiAskBtnTxt}>🧠 Ask AI about {selDrug.name}</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  )

  return (
    <SafeAreaView style={s.safe}>
      {/* Header */}
      <View style={s.header}>
        <View style={[s.hRow, isRTL && { flexDirection:"row-reverse" }]}>
          <View>
            <Text style={[s.title, isRTL && s.rtl]}>
              {lang==="ar"?"الصيدلية الذكية":lang==="fr"?"Pharmacie IA":"AI Pharmacy"}
            </Text>
            <Text style={[s.sub, isRTL && s.rtl]}>
              {lang==="ar"?"مرتبط بـ FDA وقاعدة بيانات الأدوية":"Connected to FDA · Drug Databases"}
            </Text>
          </View>
          <View style={s.fdaTag}>
            <Text style={s.fdaTagTxt}>🏛 FDA Live</Text>
          </View>
        </View>

        {/* Tabs */}
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop:12 }}>
          {([
            { key:"search",       label:lang==="ar"?"بحث الأدوية":"Drug Search" },
            { key:"interactions", label:lang==="ar"?"التفاعلات":"Interactions" },
            { key:"rx",           label:lang==="ar"?"وصفات جاهزة":"Rx Templates" },
            { key:"formulary",    label:lang==="ar"?"المساعد الذكي":"AI Assistant" },
          ] as {key:Tab;label:string}[]).map(tb => (
            <TouchableOpacity key={tb.key}
              style={[s.tabBtn, tab===tb.key && s.tabBtnOn]}
              onPress={() => setTab(tb.key)}>
              <Text style={[s.tabTxt, tab===tb.key && s.tabTxtOn]}>{tb.label}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* ── DRUG SEARCH TAB ── */}
      {tab === "search" && (
        <View style={{ flex:1 }}>
          <View style={[s.searchWrap, isRTL && { flexDirection:"row-reverse" }]}>
            <View style={s.searchIco}>
              <View style={{ width:13, height:13, borderRadius:7, borderWidth:2, borderColor:Colors.neutral400 }} />
              <View style={{ width:1.5, height:5, backgroundColor:Colors.neutral400, position:"absolute", bottom:0, right:2, transform:[{rotate:"45deg"}] }} />
            </View>
            <TextInput style={[s.searchInp, isRTL && s.rtl]}
              value={search} onChangeText={setSearch}
              placeholder={lang==="ar"?"ابحث عن دواء بالاسم أو التصنيف...":"Search drug name, class, indication..."}
              placeholderTextColor={Colors.neutral400}
            />
            {search.length > 0 && <TouchableOpacity onPress={() => setSearch("")}><Text style={{ fontSize:18, color:Colors.neutral400 }}>×</Text></TouchableOpacity>}
          </View>

          {/* Stats row */}
          <View style={[s.statsRow, isRTL && { flexDirection:"row-reverse" }]}>
            <View style={s.statPill}><Text style={s.statPillTxt}>{MOCK_DRUGS.filter(d=>d.schedule==="Rx").length} Rx drugs</Text></View>
            <View style={s.statPill}><Text style={s.statPillTxt}>{MOCK_DRUGS.filter(d=>d.schedule==="OTC").length} OTC drugs</Text></View>
            <View style={[s.statPill, { backgroundColor:Colors.success1 }]}><Text style={[s.statPillTxt, { color:Colors.success }]}>All FDA ✓</Text></View>
          </View>

          <ScrollView style={{ flex:1 }} showsVerticalScrollIndicator={false}
            contentContainerStyle={{ padding:16, paddingBottom:90 }}>
            {filtered.map((drug, i) => (
              <TouchableOpacity key={i} style={s.drugRow} onPress={() => { setSelDrug(drug); searchFDA(drug.name) }} activeOpacity={0.85}>
                <View style={[s.drugIco, isRTL && { marginRight:0, marginLeft:12 }]}>
                  <View style={{ width:16, height:16, borderRadius:8, borderWidth:2.5, borderColor:Colors.primary, backgroundColor:Colors.primary2 }} />
                  <View style={{ position:"absolute", width:12, height:5, borderRadius:3, borderWidth:2, borderColor:Colors.primary, transform:[{rotate:"30deg"}] }} />
                </View>
                <View style={[{ flex:1, minWidth:0 }, isRTL && { alignItems:"flex-end" }]}>
                  <View style={[s.drugRowTop, isRTL && { flexDirection:"row-reverse" }]}>
                    <Text style={[s.drugRowName, isRTL && s.rtl]} numberOfLines={1}>{drug.name}</Text>
                    <Text style={[s.drugRowBrand, isRTL && s.rtl]}>{drug.brand}</Text>
                  </View>
                  <Text style={[s.drugRowClass, isRTL && s.rtl]} numberOfLines={1}>{drug.class}</Text>
                  <Text style={[s.drugRowIndic, isRTL && s.rtl]} numberOfLines={1}>{drug.indication}</Text>
                </View>
                <View style={{ alignItems:"flex-end", gap:5 }}>
                  <View style={[s.schedBadge, { backgroundColor: drug.schedule==="OTC" ? Colors.success1 : Colors.primary2 }]}>
                    <Text style={[s.schedTxt, { color: drug.schedule==="OTC" ? Colors.success : Colors.primary }]}>{drug.schedule}</Text>
                  </View>
                  {drug.fda_approved && <View style={s.fdaSmall}><Text style={s.fdaSmallTxt}>FDA ✓</Text></View>}
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      )}

      {/* ── INTERACTIONS TAB ── */}
      {tab === "interactions" && (
        <ScrollView style={{ flex:1 }} contentContainerStyle={{ padding:16, paddingBottom:90 }}>
          <View style={s.intCard}>
            <Text style={[s.intTitle, isRTL && s.rtl]}>
              {lang==="ar"?"فحص التفاعلات الدوائية":"Drug Interaction Checker"}
            </Text>
            <Text style={[s.intSub, isRTL && s.rtl]}>
              {lang==="ar"?"أدخل اسمي الدواءين للتحقق من التفاعل بينهما":"Enter two drug names to check interaction"}
            </Text>
            <View style={[s.intInputs, isRTL && { flexDirection:"row-reverse" }]}>
              <TextInput style={[s.intInp, isRTL && s.rtl]} value={drug1} onChangeText={setDrug1} placeholder="Drug 1 (e.g. Warfarin)" placeholderTextColor="#AAA" />
              <View style={s.intVs}><Text style={s.intVsTxt}>⇌</Text></View>
              <TextInput style={[s.intInp, isRTL && s.rtl]} value={drug2} onChangeText={setDrug2} placeholder="Drug 2 (e.g. Aspirin)" placeholderTextColor="#AAA" />
            </View>
            <TouchableOpacity style={s.checkBtn} onPress={checkInteraction} activeOpacity={0.85}>
              <Text style={s.checkBtnTxt}>
                {lang==="ar"?"فحص التفاعل":"Check Interaction"}
              </Text>
            </TouchableOpacity>
          </View>

          {intResult && (
            <View style={[s.intResult, { borderLeftColor: SEV_COLORS[intResult.sev]?.text ?? "#888" }]}>
              <View style={[s.intResultHdr, isRTL && { flexDirection:"row-reverse" }]}>
                <Text style={[s.intResultDrugs, isRTL && s.rtl]}>{intResult.d1} + {intResult.d2}</Text>
                <View style={[s.sevBadge, { backgroundColor: SEV_COLORS[intResult.sev]?.bg }]}>
                  <Text style={[s.sevTxt, { color: SEV_COLORS[intResult.sev]?.text }]}>
                    {SEV_COLORS[intResult.sev]?.label ?? "Unknown"}
                  </Text>
                </View>
              </View>
              <Text style={[s.intEffectLbl, isRTL && s.rtl]}>Effect:</Text>
              <Text style={[s.intEffectTxt, isRTL && s.rtl]}>{intResult.effect}</Text>
              <Text style={[s.intEffectLbl, { marginTop:8 }, isRTL && s.rtl]}>Clinical Action:</Text>
              <Text style={[s.intEffectTxt, isRTL && s.rtl]}>{intResult.action}</Text>
              <TouchableOpacity style={s.askAIBtn}
                onPress={() => {
                  setAiInput(`Drug interaction between ${intResult.d1} and ${intResult.d2}: detailed clinical management`)
                  setTab("formulary")
                }}>
                <Text style={s.askAITxt}>🧠 Ask AI for detailed guidance →</Text>
              </TouchableOpacity>
            </View>
          )}

          {/* Common interaction pairs */}
          <Text style={[s.secTitle, isRTL && s.rtl, { marginTop:16, marginBottom:10 }]}>
            {lang==="ar"?"تفاعلات شائعة":"Common Interactions"}
          </Text>
          {INTERACTIONS.map((inter, i) => {
            const sc = SEV_COLORS[inter.sev]
            return (
              <TouchableOpacity key={i} style={s.interRow} onPress={() => { setDrug1(inter.d1); setDrug2(inter.d2); checkInteraction() }}>
                <View style={[{ flex:1 }, isRTL && { alignItems:"flex-end" }]}>
                  <Text style={[s.interDrugs, isRTL && s.rtl]}>{inter.d1} + {inter.d2}</Text>
                  <Text style={[s.interEffect, isRTL && s.rtl]} numberOfLines={1}>{inter.effect}</Text>
                </View>
                <View style={[s.sevBadge, { backgroundColor: sc.bg }]}>
                  <Text style={[s.sevTxt, { color: sc.text }]}>{sc.label}</Text>
                </View>
              </TouchableOpacity>
            )
          })}
        </ScrollView>
      )}

      {/* ── RX TEMPLATES TAB ── */}
      {tab === "rx" && (
        <ScrollView style={{ flex:1 }} contentContainerStyle={{ padding:16, paddingBottom:90 }}>
          <Text style={[s.secTitle, isRTL && s.rtl, { marginBottom:12 }]}>
            {lang==="ar"?"بروتوكولات علاجية جاهزة":"Evidence-Based Rx Protocols"}
          </Text>
          {RX_TEMPLATES.map((rx) => (
            <View key={rx.id} style={s.rxCard}>
              <View style={[s.rxHdr, isRTL && { flexDirection:"row-reverse" }]}>
                <View style={s.rxIco}><View style={{ width:18, height:18, borderRadius:9, borderWidth:2.5, borderColor:Colors.primary }} /></View>
                <Text style={[s.rxName, isRTL && s.rtl]}>{rx.name}</Text>
                <TouchableOpacity style={s.rxAIBtn} onPress={() => { setAiInput(`Explain the ${rx.name} protocol: drugs, rationale, monitoring`); setTab("formulary") }}>
                  <Text style={s.rxAIBtnTxt}>AI 🧠</Text>
                </TouchableOpacity>
              </View>
              {rx.drugs.map((drug, i) => (
                <View key={i} style={[s.rxDrugRow, isRTL && { flexDirection:"row-reverse" }]}>
                  <View style={s.rxDot} />
                  <Text style={[s.rxDrugTxt, isRTL && s.rtl]}>{drug}</Text>
                </View>
              ))}
              <TouchableOpacity style={s.rxPrintBtn}>
                <Text style={s.rxPrintTxt}>📄 {lang==="ar"?"طباعة الوصفة":"Print Prescription"}</Text>
              </TouchableOpacity>
            </View>
          ))}
        </ScrollView>
      )}

      {/* ── AI ASSISTANT TAB ── */}
      {tab === "formulary" && (
        <KeyboardAvoidingView style={{ flex:1 }} behavior={Platform.OS==="ios"?"padding":undefined}>
          <View style={s.aiHdr}>
            <View style={s.aiLive} />
            <Text style={s.aiHdrTitle}>
              {lang==="ar"?"المساعد الصيدلاني الذكي":"AI Pharmacy Assistant"}
            </Text>
            <Text style={s.aiHdrSub}>FDA · USP · Lexicomp</Text>
          </View>

          {/* Quick prompts */}
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={s.qpScroll} contentContainerStyle={{ gap:8 }}>
            {QUICK_PROMPTS.map((q, i) => (
              <TouchableOpacity key={i} style={s.qpBtn} onPress={() => aiChat(q)}>
                <Text style={[s.qpTxt, isRTL && s.rtl]} numberOfLines={1}>{q}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          {/* Chat messages */}
          <ScrollView ref={scrollRef} style={s.chatArea} showsVerticalScrollIndicator={false}
            contentContainerStyle={{ padding:14, gap:10 }}
            onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated:true })}>
            {aiMsgs.map((m, i) => (
              <View key={i} style={[s.mWrap, m.role==="user" ? s.mWrapU : s.mWrapB]}>
                {m.role==="assistant" && (
                  <View style={s.mAv}>
                    <View style={{ width:12, height:12, borderRadius:6, borderWidth:2.5, borderColor:Colors.primary, backgroundColor:Colors.primary2 }} />
                  </View>)}
                <View style={[s.bubble, m.role==="user" ? s.bubU : s.bubB, { maxWidth:"82%" }]}>
                  <Text style={[s.bubTxt, m.role==="user" ? s.bubTxtU : s.bubTxtB, isRTL && s.rtl]}>{m.text}</Text>
                  <Text style={[s.bubTime, m.role==="user" && { textAlign:"right" }]}>{m.time}</Text>
                </View>
              </View>
            ))}
            {aiLoading && (
              <View style={s.mWrapB}>
                <View style={s.mAv}><View style={{ width:12, height:12, borderRadius:6, borderWidth:2.5, borderColor:Colors.primary, backgroundColor:Colors.primary2 }} /></View>
                <View style={[s.bubble, s.bubB, { paddingVertical:12, paddingHorizontal:18 }]}><ActivityIndicator size="small" color={Colors.primary} /></View>
              </View>)}
          </ScrollView>

          {/* Input */}
          <View style={[s.inpRow, isRTL && { flexDirection:"row-reverse" }]}>
            <TextInput style={[s.inp, isRTL && s.rtl]} value={aiInput} onChangeText={setAiInput}
              placeholder={lang==="ar"?"اسأل عن أي دواء...":"Ask about any drug..."}
              placeholderTextColor={Colors.neutral400} multiline maxLength={500}
              onSubmitEditing={() => aiChat()} returnKeyType="send" />
            <TouchableOpacity style={[s.sendBtn, (!aiInput.trim()||aiLoading) && { backgroundColor:Colors.neutral300 }]}
              onPress={() => aiChat()} disabled={!aiInput.trim()||aiLoading} activeOpacity={0.85}>
              <View style={{ width:0, height:0, borderTopWidth:6, borderBottomWidth:6, borderLeftWidth:9, borderTopColor:"transparent", borderBottomColor:"transparent", borderLeftColor:"#FFF", marginLeft:2 }} />
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      )}
    </SafeAreaView>
  )
}

const s = StyleSheet.create({
  safe:    { flex:1, backgroundColor:"#F8F8F8" },
  rtl:     { textAlign:"right" },
  header:  { backgroundColor:"#FFF", paddingHorizontal:16, paddingTop:12, paddingBottom:10, borderBottomWidth:1, borderBottomColor:"#F0F0F0" },
  hRow:    { flexDirection:"row", justifyContent:"space-between", alignItems:"flex-start" },
  title:   { fontSize:20, fontWeight:"800", color:"#111", letterSpacing:-0.3 },
  sub:     { fontSize:11, color:"#888", fontWeight:"500", marginTop:2 },
  fdaTag:  { backgroundColor:"#EFF6FF", borderRadius:10, paddingHorizontal:10, paddingVertical:5, borderWidth:1, borderColor:Colors.primary3 },
  fdaTagTxt:{ fontSize:11, fontWeight:"800", color:Colors.primary },
  tabBtn:  { paddingHorizontal:14, paddingVertical:7, borderRadius:20, borderWidth:1.5, borderColor:"#E0E0E0", backgroundColor:"#F8F8F8", marginRight:8 },
  tabBtnOn:{ borderColor:Colors.primary, backgroundColor:Colors.primary2 },
  tabTxt:  { fontSize:11, fontWeight:"700", color:"#888" },
  tabTxtOn:{ color:Colors.primary },
  // Search
  searchWrap:{ flexDirection:"row", alignItems:"center", backgroundColor:"#F5F5F5", borderRadius:12, paddingHorizontal:14, height:44, margin:12, marginBottom:6 },
  searchIco: { width:22, alignItems:"center", justifyContent:"center", marginRight:8, position:"relative" },
  searchInp: { flex:1, fontSize:13, color:"#111", fontWeight:"500" },
  statsRow:  { flexDirection:"row", gap:8, paddingHorizontal:12, marginBottom:6 },
  statPill:  { backgroundColor:Colors.primary2, borderRadius:20, paddingHorizontal:10, paddingVertical:4 },
  statPillTxt:{ fontSize:10, fontWeight:"700", color:Colors.primary },
  // Drug row
  drugRow:  { backgroundColor:"#FFF", borderRadius:14, borderWidth:1, borderColor:"#EEEEEE", padding:14, flexDirection:"row", alignItems:"center", gap:12, marginBottom:8 },
  drugIco:  { width:40, height:40, backgroundColor:Colors.primary2, borderRadius:12, alignItems:"center", justifyContent:"center", position:"relative" },
  drugRowTop:{ flexDirection:"row", alignItems:"center", gap:6, marginBottom:3 },
  drugRowName:{ fontSize:14, fontWeight:"800", color:"#111" },
  drugRowBrand:{ fontSize:11, color:"#888", fontWeight:"600" },
  drugRowClass:{ fontSize:11, fontWeight:"600", color:Colors.primary, marginBottom:2 },
  drugRowIndic:{ fontSize:10, color:"#888", fontWeight:"500" },
  schedBadge:{ borderRadius:20, paddingHorizontal:8, paddingVertical:3 },
  schedTxt:  { fontSize:10, fontWeight:"800" },
  fdaSmall:  { backgroundColor:"#DCFCE7", borderRadius:8, paddingHorizontal:6, paddingVertical:2 },
  fdaSmallTxt:{ fontSize:9, fontWeight:"800", color:"#15803D" },
  // Drug detail
  drugDetailHdr:{ backgroundColor:Colors.primary, paddingHorizontal:16, paddingVertical:13, flexDirection:"row", alignItems:"center", gap:10 },
  backBtn:   { backgroundColor:"rgba(255,255,255,0.2)", borderRadius:10, paddingHorizontal:12, paddingVertical:6 },
  backTxt:   { fontSize:12, fontWeight:"700", color:"#FFF" },
  drugDetailTitle:{ flex:1, fontSize:15, fontWeight:"800", color:"#FFF" },
  scheduleBadge:{ borderRadius:12, paddingHorizontal:10, paddingVertical:4 },
  scheduleTxt:  { fontSize:11, fontWeight:"800" },
  drugCard:  { backgroundColor:"#FFF", borderRadius:16, borderWidth:1, borderColor:"#EEEEEE", padding:16, marginBottom:12 },
  drugCardRow:{ flexDirection:"row", alignItems:"flex-start", gap:14, marginBottom:14, paddingBottom:14, borderBottomWidth:1, borderBottomColor:"#F5F5F5" },
  drugIcoBig:{ width:56, height:56, backgroundColor:Colors.primary2, borderRadius:16, alignItems:"center", justifyContent:"center", position:"relative" },
  drugName:  { fontSize:18, fontWeight:"900", color:"#111", marginBottom:3, letterSpacing:-0.3 },
  drugBrand: { fontSize:12, color:"#888", fontWeight:"600", marginBottom:3 },
  drugClass: { fontSize:12, fontWeight:"700", color:Colors.primary },
  fdaBadge:  { backgroundColor:"#DCFCE7", borderRadius:10, paddingHorizontal:10, paddingVertical:5, alignSelf:"flex-start" },
  fdaTxt:    { fontSize:11, fontWeight:"800", color:"#15803D" },
  infoRow:   { flexDirection:"row", justifyContent:"space-between", paddingVertical:9 },
  infoL:     { fontSize:11, color:"#AAA", fontWeight:"600" },
  infoV:     { fontSize:12, color:"#111", fontWeight:"700", maxWidth:"60%", textAlign:"right" },
  warnCard:  { backgroundColor:"#FFF7ED", borderRadius:14, borderWidth:1, borderColor:"#FED7AA", padding:14, marginBottom:12 },
  warnHdr:   { flexDirection:"row", alignItems:"center", gap:8, marginBottom:10 },
  warnDot:   { width:8, height:8, borderRadius:4, backgroundColor:Colors.warning },
  warnTitle: { fontSize:13, fontWeight:"800", color:"#92400E" },
  warnItem:  { flexDirection:"row", alignItems:"flex-start", gap:8, marginBottom:7 },
  warnBullet:{ width:5, height:5, borderRadius:2.5, backgroundColor:Colors.warning, marginTop:5 },
  warnTxt:   { flex:1, fontSize:12, color:"#78350F", fontWeight:"500", lineHeight:18 },
  fdaBtn:    { backgroundColor:Colors.primary, borderRadius:12, paddingVertical:13, alignItems:"center", marginBottom:12 },
  fdaBtnTxt: { fontSize:13, fontWeight:"800", color:"#FFF" },
  fdaCard:   { backgroundColor:"#FFF", borderRadius:14, borderWidth:1, borderColor:"#EEEEEE", padding:14, marginBottom:12 },
  fdaCardTitle:{ fontSize:13, fontWeight:"800", color:"#111", marginBottom:10 },
  fdaSection:  {},
  fdaSectionTitle:{ fontSize:10, fontWeight:"800", color:Colors.primary, textTransform:"uppercase", letterSpacing:.5, marginBottom:4 },
  fdaSectionTxt:  { fontSize:12, color:"#444", lineHeight:18, fontWeight:"500" },
  aiAskBtn:  { backgroundColor:Colors.primary2, borderRadius:12, paddingVertical:12, alignItems:"center", borderWidth:1.5, borderColor:Colors.primary3 },
  aiAskBtnTxt:{ fontSize:13, fontWeight:"700", color:Colors.primary },
  // Interactions
  intCard:   { backgroundColor:"#FFF", borderRadius:16, borderWidth:1, borderColor:"#EEEEEE", padding:16, marginBottom:14 },
  intTitle:  { fontSize:16, fontWeight:"800", color:"#111", marginBottom:4 },
  intSub:    { fontSize:12, color:"#888", fontWeight:"500", marginBottom:14 },
  intInputs: { flexDirection:"row", alignItems:"center", gap:8, marginBottom:12 },
  intInp:    { flex:1, borderWidth:1.5, borderColor:"#E0E0E0", borderRadius:10, padding:10, fontSize:12, color:"#111", fontFamily:"System" },
  intVs:     { width:32, height:32, backgroundColor:Colors.primary2, borderRadius:16, alignItems:"center", justifyContent:"center" },
  intVsTxt:  { fontSize:14, fontWeight:"800", color:Colors.primary },
  checkBtn:  { backgroundColor:Colors.primary, borderRadius:12, paddingVertical:12, alignItems:"center" },
  checkBtnTxt:{ fontSize:13, fontWeight:"800", color:"#FFF" },
  intResult: { backgroundColor:"#FFF", borderRadius:14, borderWidth:1, borderColor:"#EEEEEE", borderLeftWidth:4, padding:14, marginBottom:14 },
  intResultHdr:{ flexDirection:"row", justifyContent:"space-between", alignItems:"center", marginBottom:10 },
  intResultDrugs:{ fontSize:13, fontWeight:"800", color:"#111", flex:1 },
  sevBadge:  { borderRadius:20, paddingHorizontal:10, paddingVertical:4, marginLeft:8 },
  sevTxt:    { fontSize:10, fontWeight:"800" },
  intEffectLbl:{ fontSize:10, fontWeight:"800", color:"#888", textTransform:"uppercase", letterSpacing:.5, marginBottom:4 },
  intEffectTxt:{ fontSize:12, color:"#333", lineHeight:18, fontWeight:"500", marginBottom:4 },
  askAIBtn:  { marginTop:10, backgroundColor:Colors.primary2, borderRadius:10, paddingVertical:9, alignItems:"center" },
  askAITxt:  { fontSize:12, fontWeight:"700", color:Colors.primary },
  interRow:  { backgroundColor:"#FFF", borderRadius:12, borderWidth:1, borderColor:"#EEEEEE", padding:12, flexDirection:"row", alignItems:"center", gap:10, marginBottom:8 },
  interDrugs:{ fontSize:12, fontWeight:"800", color:"#111", marginBottom:3 },
  interEffect:{ fontSize:11, color:"#888", fontWeight:"500" },
  secTitle:  { fontSize:12, fontWeight:"800", color:"#888", textTransform:"uppercase", letterSpacing:.5 },
  // RX templates
  rxCard:    { backgroundColor:"#FFF", borderRadius:14, borderWidth:1, borderColor:"#EEEEEE", padding:14, marginBottom:12 },
  rxHdr:     { flexDirection:"row", alignItems:"center", gap:10, marginBottom:12, paddingBottom:10, borderBottomWidth:1, borderBottomColor:"#F5F5F5" },
  rxIco:     { width:32, height:32, backgroundColor:Colors.primary2, borderRadius:10, alignItems:"center", justifyContent:"center" },
  rxName:    { flex:1, fontSize:14, fontWeight:"800", color:"#111" },
  rxAIBtn:   { backgroundColor:Colors.primary2, borderRadius:8, paddingHorizontal:10, paddingVertical:5 },
  rxAIBtnTxt:{ fontSize:11, fontWeight:"700", color:Colors.primary },
  rxDrugRow: { flexDirection:"row", alignItems:"center", gap:8, marginBottom:8 },
  rxDot:     { width:6, height:6, borderRadius:3, backgroundColor:Colors.primary },
  rxDrugTxt: { fontSize:12, color:"#333", fontWeight:"600", flex:1 },
  rxPrintBtn:{ borderWidth:1.5, borderColor:"#E0E0E0", borderRadius:10, paddingVertical:9, alignItems:"center", marginTop:6 },
  rxPrintTxt:{ fontSize:12, fontWeight:"700", color:"#666" },
  // AI chat
  aiHdr:     { backgroundColor:Colors.primary, paddingHorizontal:16, paddingVertical:11, flexDirection:"row", alignItems:"center", gap:10 },
  aiLive:    { width:8, height:8, borderRadius:4, backgroundColor:"#4ADE80" },
  aiHdrTitle:{ fontSize:14, fontWeight:"800", color:"#FFF", flex:1 },
  aiHdrSub:  { fontSize:10, color:"rgba(255,255,255,0.75)", fontWeight:"600" },
  qpScroll:  { backgroundColor:"#FFF", paddingVertical:9, paddingHorizontal:14, borderBottomWidth:1, borderBottomColor:"#F0F0F0" },
  qpBtn:     { paddingHorizontal:12, paddingVertical:7, borderRadius:20, borderWidth:1.5, borderColor:Colors.primary3, backgroundColor:Colors.primary2, maxWidth:180 },
  qpTxt:     { fontSize:11, fontWeight:"700", color:Colors.primary },
  chatArea:  { flex:1, backgroundColor:"#F5F5F5" },
  mWrap:     { flexDirection:"row", alignItems:"flex-end", gap:8 },
  mWrapB:    { justifyContent:"flex-start" },
  mWrapU:    { justifyContent:"flex-end" },
  mAv:       { width:28, height:28, borderRadius:14, backgroundColor:Colors.primary2, alignItems:"center", justifyContent:"center", flexShrink:0 },
  bubble:    { borderRadius:18, paddingHorizontal:13, paddingVertical:10 },
  bubB:      { backgroundColor:"#FFF", borderBottomLeftRadius:4, borderWidth:1, borderColor:"#EEEEEE" },
  bubU:      { backgroundColor:Colors.primary, borderBottomRightRadius:4 },
  bubTxt:    { fontSize:12, lineHeight:18 },
  bubTxtB:   { color:"#111" },
  bubTxtU:   { color:"#FFF" },
  bubTime:   { fontSize:9, marginTop:4, color:"#AAA", fontWeight:"500" },
  inpRow:    { backgroundColor:"#FFF", borderTopWidth:1, borderTopColor:"#F0F0F0", paddingHorizontal:14, paddingVertical:10, flexDirection:"row", alignItems:"flex-end", gap:10 },
  inp:       { flex:1, borderWidth:1.5, borderColor:"#E0E0E0", borderRadius:22, paddingHorizontal:14, paddingVertical:9, fontSize:12, color:"#111", maxHeight:100, fontWeight:"500" },
  sendBtn:   { width:42, height:42, backgroundColor:Colors.primary, borderRadius:21, alignItems:"center", justifyContent:"center", flexShrink:0 },
})
