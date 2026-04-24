import { useState, useRef, useCallback } from "react"
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  TextInput, KeyboardAvoidingView, Platform, ActivityIndicator,
  Dimensions, FlatList
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors, Spacing, Radius, Typography } from "../../constants/theme"
import { getLang } from "../i18n"
import AsyncStorage from "@react-native-async-storage/async-storage"
import { API_URL } from "../api/client"

const W = Dimensions.get("window").width
type Msg = { role:"user"|"assistant"; text:string; time:string }

// ── 12 Medical Specialties ────────────────────────────
const SPECIALTIES = [
  {
    id:"cardiology", icon:"❤️", color:"#FEE2E2", accent:"#DC2626",
    name:{ en:"Cardiology", ar:"أمراض القلب", fr:"Cardiologie" },
    desc:{ en:"Heart & Vascular", ar:"القلب والأوعية", fr:"Cœur & Vaisseaux" },
    tools:["ECG Analysis","Troponin Interpretation","Heart Failure Staging","TIMI/GRACE Score","Anti-arrhythmic Guide"],
    prompts:["Interpret ECG: ST elevation V1-V4, reciprocal changes","STEMI management protocol step by step","Heart failure NYHA classification for dyspnea on exertion","Calculate TIMI score: age 68, DM, anterior ST depression","Differential for chest pain + diaphoresis in 55M"],
    system:"You are an expert AI cardiologist. Provide clinical guidance on: ECG interpretation, ACS management, heart failure, arrhythmias, cardiac risk stratification, valve diseases, and cardiovascular pharmacology. Always recommend emergency consultation for critical presentations. Format responses with urgency levels and evidence-based guidelines (ACC/AHA)."
  },
  {
    id:"neurology", icon:"🧠", color:"#F5F3FF", accent:"#7C3AED",
    name:{ en:"Neurology", ar:"الأعصاب", fr:"Neurologie" },
    desc:{ en:"Brain & Nervous System", ar:"الدماغ والجهاز العصبي", fr:"Cerveau & Nerfs" },
    tools:["Stroke Scale (NIHSS)","Seizure Classification","GCS Assessment","MS Scoring","Headache Classifier"],
    prompts:["NIHSS scoring for acute stroke with left hemiplegia","Seizure management in status epilepticus","Multiple sclerosis first presentation MRI criteria","Thunderclap headache differential diagnosis","Bell's palsy vs stroke facial weakness differentiation"],
    system:"You are an expert AI neurologist. Provide clinical guidance on: stroke management, epilepsy, headache disorders, movement disorders, MS, neuropathies, and neurocritical care. Apply AAN guidelines. For stroke symptoms, emphasize time-critical interventions (tPA window, thrombectomy)."
  },
  {
    id:"radiology", icon:"🩻", color:"#EFF6FF", accent:"#2563EB",
    name:{ en:"Radiology & Imaging", ar:"الأشعة والتصوير", fr:"Radiologie & Imagerie" },
    desc:{ en:"X-Ray, MRI, CT, US", ar:"أشعة، رنين، مقطعي", fr:"Radio, IRM, Scanner" },
    tools:["X-Ray Report AI","CT Interpretation","MRI Analysis","Ultrasound Guide","Contrast Protocol"],
    prompts:["Describe findings: chest X-ray with right lower lobe consolidation","MRI brain T2 hyperintense lesion 1.5cm right temporal","CT abdomen: hypodense lesion liver segment 6, 2.3cm","Ultrasound thyroid: hypoechoic nodule 1.8cm with microcalcifications","Chest X-ray interpretation: cardiomegaly + bilateral pleural effusions"],
    system:"You are an expert AI radiologist with subspecialty knowledge in chest, neuro, abdominal, and musculoskeletal imaging. Interpret imaging findings systematically: describe the finding, provide differential diagnosis ranked by likelihood, recommend follow-up imaging if needed, and flag urgent/critical findings. Use standard reporting terminology (BIRADS, TIRADS, LI-RADS where applicable)."
  },
  {
    id:"emergency", icon:"🚨", color:"#FEF2F2", accent:"#EF4444",
    name:{ en:"Emergency Medicine", ar:"طب الطوارئ", fr:"Médecine d'Urgence" },
    desc:{ en:"Critical & Trauma Care", ar:"الإسعاف والصدمات", fr:"Soins Critiques" },
    tools:["ABCDE Assessment","Trauma Protocol","Sepsis 3 Criteria","Shock Classification","Rapid Sequence Intubation"],
    prompts:["Primary ABCDE survey for polytrauma patient","Sepsis-3 criteria met: management bundle in first hour","Anaphylaxis management with epinephrine dosing","Rapid sequence intubation: drug dosing for 80kg patient","Hemorrhagic shock grade 3: massive transfusion protocol"],
    system:"You are an expert AI emergency physician. Provide rapid, structured guidance on: trauma resuscitation, sepsis bundles, toxicology, cardiac arrest, airway management, shock classification, and critical procedures. Prioritize life-threatening conditions. Apply ATLS, Surviving Sepsis Campaign, and ACLS guidelines. Use clear action-oriented language."
  },
  {
    id:"pediatrics", icon:"👶", color:"#FFF7ED", accent:"#EA580C",
    name:{ en:"Pediatrics", ar:"طب الأطفال", fr:"Pédiatrie" },
    desc:{ en:"Children's Health", ar:"صحة الأطفال", fr:"Santé Infantile" },
    tools:["Pediatric Dosing Calc","Growth Chart Assessment","Vaccine Schedule","Febrile Seizure Guide","Neonatal Assessment"],
    prompts:["Amoxicillin dose for 18-month-old 12kg with otitis media","Febrile seizure management: 2-year-old first episode 39.5°C","Neonatal jaundice: bilirubin 18 at day 3, phototherapy threshold","Kawasaki disease diagnostic criteria in 4-year-old","Pediatric asthma exacerbation severity scoring and management"],
    system:"You are an expert AI pediatrician with neonatology knowledge. Calculate weight-based dosing, assess developmental milestones, interpret pediatric vital signs by age, guide vaccination schedules, and manage common pediatric emergencies. Always specify age-appropriate reference ranges. Apply AAP and WHO guidelines."
  },
  {
    id:"surgery", icon:"🔪", color:"#F0FDF4", accent:"#16A34A",
    name:{ en:"General Surgery", ar:"الجراحة العامة", fr:"Chirurgie Générale" },
    desc:{ en:"Surgical Planning & Care", ar:"التخطيط الجراحي", fr:"Planification Chirurgicale" },
    tools:["Pre-op Risk (ASA)","Surgical Antibiotic Prophylaxis","Post-op Checklist","Drain Management","Wound Classification"],
    prompts:["Pre-operative risk assessment: ASA classification for 65M with DM and HTN","Surgical antibiotic prophylaxis for laparoscopic cholecystectomy","Post-appendectomy day 2 fever workup: wound vs deep infection","Bowel obstruction: conservative vs surgical management criteria","Whipple procedure: post-op complications and monitoring"],
    system:"You are an expert AI general surgeon and perioperative specialist. Guide pre-operative optimization, intraoperative decision-making, post-operative care, surgical complication management, and wound care. Apply evidence-based surgical principles and enhanced recovery after surgery (ERAS) protocols."
  },
  {
    id:"orthopedics", icon:"🦴", color:"#F1F5F9", accent:"#475569",
    name:{ en:"Orthopedics", ar:"العظام والمفاصل", fr:"Orthopédie" },
    desc:{ en:"Bones, Joints & Spine", ar:"العظام والمفاصل", fr:"Os, Articulations" },
    tools:["Fracture Classification","Spine Assessment","Arthroplasty Criteria","Osteoporosis Score","Sports Injury Guide"],
    prompts:["Distal radius fracture: Colles vs Smith classification and management","Lumbar disc herniation L4-L5: conservative vs surgical criteria","Hip fracture in 78F: Garden classification and surgical timing","Anterior cruciate ligament tear diagnosis and reconstruction criteria","Osteoporosis management: FRAX score interpretation and treatment"],
    system:"You are an expert AI orthopedic surgeon and sports medicine specialist. Guide fracture management, joint replacement criteria, spine disorders, sports injuries, and rehabilitation. Apply AO Foundation fracture classification, bone health guidelines, and evidence-based rehabilitation protocols."
  },
  {
    id:"gynecology", icon:"🌸", color:"#FDF2F8", accent:"#9D174D",
    name:{ en:"Obstetrics & Gynecology", ar:"النساء والولادة", fr:"Obstétrique & Gynécologie" },
    desc:{ en:"Women's Health", ar:"صحة المرأة", fr:"Santé Féminine" },
    tools:["Pregnancy Calculator","CTG Interpretation","Preeclampsia Screen","PCOS Diagnosis","Cervical Cancer Screen"],
    prompts:["CTG interpretation: variable decelerations at 36 weeks, baseline 150bpm","Preeclampsia management: BP 160/105 at 34 weeks + proteinuria","PCOS diagnosis: Rotterdam criteria and management options","Postpartum hemorrhage: PPH protocol and uterotonic drugs","Ectopic pregnancy: beta-HCG 2500, no IUP on ultrasound"],
    system:"You are an expert AI obstetrician-gynecologist. Provide guidance on: antepartum and intrapartum care, CTG interpretation, obstetric emergencies, gynecological conditions, family planning, and women's cancer screening. Apply ACOG and FIGO guidelines. For obstetric emergencies, emphasize maternal and fetal safety."
  },
  {
    id:"psychiatry", icon:"🧩", color:"#FFF7ED", accent:"#D97706",
    name:{ en:"Psychiatry", ar:"الطب النفسي", fr:"Psychiatrie" },
    desc:{ en:"Mental Health & Behavior", ar:"الصحة النفسية", fr:"Santé Mentale" },
    tools:["DSM-5 Criteria","PHQ-9 Assessment","Medication Guide","Crisis Protocol","Cognitive Assessment"],
    prompts:["DSM-5 criteria for major depressive episode vs bipolar disorder","Schizophrenia first episode: initial medication and monitoring","Suicidal ideation: risk stratification and safety planning","Lithium toxicity signs: level 2.1 mEq/L management","Psychosis: antipsychotic selection guide for first episode"],
    system:"You are an expert AI psychiatrist with knowledge of DSM-5, psychopharmacology, and crisis intervention. Provide guidance on: diagnostic criteria, medication selection and monitoring, psychotherapy indications, and crisis management. For suicidal/homicidal ideation, emphasize safety assessment and immediate intervention. Apply APA guidelines."
  },
  {
    id:"endocrinology", icon:"⚗️", color:"#ECFDF5", accent:"#059669",
    name:{ en:"Endocrinology", ar:"الغدد الصماء", fr:"Endocrinologie" },
    desc:{ en:"Hormones & Metabolism", ar:"الهرمونات والتمثيل", fr:"Hormones & Métabolisme" },
    tools:["Diabetes Management","Thyroid Protocol","Adrenal Assessment","HbA1c Calculator","Insulin Dosing"],
    prompts:["Type 2 DM: HbA1c 9.8%, metformin failure — next medication step","Thyroid nodule 2.5cm: TIRADS 4, next investigation","DKA management: pH 7.1, glucose 480, bicarbonate 8","Hypothyroidism: TSH 45 with symptoms, levothyroxine initiation","Cushing syndrome: 24h urine cortisol 450, next step"],
    system:"You are an expert AI endocrinologist. Guide management of: diabetes (type 1, type 2, gestational), thyroid disorders, adrenal diseases, pituitary disorders, metabolic bone disease, and reproductive endocrinology. Apply ADA, ATA, and Endocrine Society guidelines. Include practical medication dosing and monitoring parameters."
  },
  {
    id:"oncology", icon:"🎗️", color:"#FFF1F2", accent:"#BE123C",
    name:{ en:"Oncology", ar:"علم الأورام", fr:"Oncologie" },
    desc:{ en:"Cancer Diagnosis & Treatment", ar:"تشخيص وعلاج السرطان", fr:"Diagnostic & Traitement Cancer" },
    tools:["TNM Staging","Chemotherapy Guide","Tumor Markers","ECOG Performance","Palliative Care"],
    prompts:["Breast cancer staging: 2.3cm tumor, 2 positive nodes, ER/PR+, HER2-","Lung adenocarcinoma: EGFR mutation positive, first-line treatment","Colorectal cancer follow-up: CEA rising after curative resection","Chemotherapy toxicity: neutropenic fever protocol","Palliative care transition criteria: ECOG 3-4 patient"],
    system:"You are an expert AI oncologist with knowledge of surgical, medical, and radiation oncology. Guide: cancer staging using TNM, chemotherapy regimen selection, targeted therapy, immunotherapy, supportive care, and palliative medicine. Apply NCCN, ESMO, and ASCO guidelines. Always include performance status assessment."
  },
  {
    id:"nephrology", icon:"🫘", color:"#F0F9FF", accent:"#0369A1",
    name:{ en:"Nephrology", ar:"أمراض الكلى", fr:"Néphrologie" },
    desc:{ en:"Kidney & Renal Disease", ar:"الكلى وأمراض الجهاز البولي", fr:"Reins & Maladies Rénales" },
    tools:["eGFR Calculator","CKD Staging","Dialysis Guide","AKI Assessment","Electrolyte Correction"],
    prompts:["AKI: creatinine 4.2 from baseline 1.0, urine output 200mL/24h — staging and management","CKD stage 4: eGFR 22, medication dose adjustments needed","Hyperkalemia 6.8 mEq/L: ECG changes present — emergency management","Hemodialysis indication criteria: when to initiate in CKD5","Hyponatremia 118: chronic vs acute, correction rate and monitoring"],
    system:"You are an expert AI nephrologist. Guide: AKI and CKD management, dialysis decisions, electrolyte disorders, glomerulonephritis, renal replacement therapy, and renal drug dosing adjustments. Apply KDIGO guidelines. Include CKD staging, eGFR interpretation, and proteinuria assessment."
  },
]

export default function SpecialtiesScreen() {
  const lang = getLang()
  const isRTL = lang === "ar"
  const [selSpec, setSelSpec] = useState<any>(null)
  const [msgs, setMsgs]     = useState<Msg[]>([])
  const [input, setInput]   = useState("")
  const [loading, setLoading] = useState(false)
  const [activeTool, setActiveTool] = useState<string|null>(null)
  const ref = useRef<ScrollView>(null)

  function now() {
    const d = new Date()
    return `${d.getHours()}:${String(d.getMinutes()).padStart(2,"0")}`
  }

  function openSpec(spec: any) {
    setSelSpec(spec)
    setMsgs([{
      role:"assistant",
      text: lang==="ar"
        ? `مرحباً! أنا مساعد الذكاء الاصطناعي لـ ${spec.name.ar}.\n\nيمكنني مساعدتك في:\n${spec.tools.map((t:string) => `• ${t}`).join("\n")}\n\nاختر أداة أو اكتب سؤالك مباشرة.`
        : `Hello! I'm the AI specialist for ${spec.name.en}.\n\nI can help with:\n${spec.tools.map((t:string) => `• ${t}`).join("\n")}\n\nSelect a tool or type your question.`,
      time: now()
    }])
    setActiveTool(null)
  }

  const sendMsg = useCallback(async (text?: string) => {
    if (!selSpec) return
    const msg = text ?? input.trim()
    if (!msg || loading) return
    setInput("")

    const um: Msg = { role:"user", text:msg, time:now() }
    const newMsgs = [...msgs, um]
    setMsgs(newMsgs)
    setLoading(true)
    setTimeout(() => ref.current?.scrollToEnd({ animated:true }), 100)

    try {
      const token = await AsyncStorage.getItem("aiha_token")
      const res = await fetch(`${API_URL}/chatbot/chat`, {
        method:"POST",
        headers:{ "Content-Type":"application/json", ...(token ? { Authorization:`Bearer ${token}` } : {}) },
        body: JSON.stringify({
          message: msg,
          language: lang,
          system: selSpec.system,
          history: newMsgs.slice(-12).map((m: Msg) => ({ role:m.role, content:m.text })),
        }),
      })
      const data = await res.json()
      setMsgs(p => [...p, {
        role:"assistant",
        text: data.response ?? data.message ?? "Please try again.",
        time: now()
      }])
    } catch {
      setMsgs(p => [...p, {
        role:"assistant",
        text: lang==="ar" ? "عذراً، خطأ في الاتصال. حاول مرة أخرى." : "Connection error. Please try again.",
        time: now()
      }])
    }
    setLoading(false)
    setTimeout(() => ref.current?.scrollToEnd({ animated:true }), 100)
  }, [input, msgs, loading, lang, selSpec])

  // ── SPECIALTY DETAIL VIEW ──────────────────────────
  if (selSpec) return (
    <SafeAreaView style={[s.safe, { backgroundColor: selSpec.color }]}>
      {/* Header */}
      <View style={[s.specHdr, { backgroundColor: selSpec.color }]}>
        <TouchableOpacity style={s.backBtn} onPress={() => setSelSpec(null)}>
          <Text style={[s.backTxt, { color: selSpec.accent }]}>← {lang==="ar"?"رجوع":"Back"}</Text>
        </TouchableOpacity>
        <View style={{ flex:1, alignItems:"center" }}>
          <Text style={{ fontSize:28 }}>{selSpec.icon}</Text>
          <Text style={[s.specHdrName, { color: selSpec.accent }]}>
            {selSpec.name[lang] ?? selSpec.name.en}
          </Text>
        </View>
        <View style={{ width:60 }} />
      </View>

      {/* Tools bar */}
      <View style={[s.toolsBar, { backgroundColor: selSpec.color, borderBottomColor: selSpec.accent+"22" }]}>
        <Text style={[s.toolsLbl, { color: selSpec.accent }]}>
          {lang==="ar"?"الأدوات الذكية":"AI Tools"}
        </Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap:8, paddingTop:6 }}>
          {selSpec.tools.map((tool: string) => (
            <TouchableOpacity key={tool}
              style={[s.toolBtn, { borderColor: selSpec.accent+"44", backgroundColor: activeTool===tool ? selSpec.accent : "#FFF" }]}
              onPress={() => {
                setActiveTool(tool)
                sendMsg(`Help me with: ${tool}`)
              }}>
              <Text style={[s.toolTxt, { color: activeTool===tool ? "#FFF" : selSpec.accent }]}>
                {tool}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      <KeyboardAvoidingView style={{ flex:1, backgroundColor:"#F8F8F8" }} behavior={Platform.OS==="ios"?"padding":undefined}>
        {/* Chat */}
        <ScrollView ref={ref} style={s.chatArea} showsVerticalScrollIndicator={false}
          contentContainerStyle={{ padding:14, gap:10 }}
          onContentSizeChange={() => ref.current?.scrollToEnd({ animated:true })}>

          {msgs.map((m, i) => (
            <View key={i} style={[s.mWrap, m.role==="user" ? s.mWrapU : s.mWrapB]}>
              {m.role==="assistant" && (
                <View style={[s.mAv, { backgroundColor: selSpec.color, borderColor: selSpec.accent+"44" }]}>
                  <Text style={{ fontSize:14 }}>{selSpec.icon}</Text>
                </View>
              )}
              <View style={[
                s.bubble,
                m.role==="user"
                  ? { backgroundColor: selSpec.accent, borderBottomRightRadius:4 }
                  : s.bubB,
                { maxWidth:"82%" }
              ]}>
                <Text style={[s.bubTxt, { color: m.role==="user" ? "#FFF" : "#111" }, isRTL && s.rtl]}>
                  {m.text}
                </Text>
                <Text style={[s.bubTime, m.role==="user" && { textAlign:"right", color:"rgba(255,255,255,0.6)" }]}>
                  {m.time}
                </Text>
              </View>
            </View>
          ))}

          {loading && (
            <View style={s.mWrapB}>
              <View style={[s.mAv, { backgroundColor: selSpec.color }]}>
                <Text style={{ fontSize:14 }}>{selSpec.icon}</Text>
              </View>
              <View style={[s.bubble, s.bubB, { paddingVertical:13, paddingHorizontal:20 }]}>
                <ActivityIndicator size="small" color={selSpec.accent} />
              </View>
            </View>
          )}
        </ScrollView>

        {/* Quick clinical prompts */}
        <View style={[s.qpBar, { borderTopColor: selSpec.accent+"22" }]}>
          <Text style={[s.qpLbl, { color: selSpec.accent }]}>
            {lang==="ar"?"أسئلة سريرية":"Clinical Prompts"}
          </Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap:8, paddingTop:4 }}>
            {selSpec.prompts.map((p: string, i: number) => (
              <TouchableOpacity key={i} style={[s.qpBtn, { borderColor: selSpec.accent+"33", backgroundColor: selSpec.color }]} onPress={() => sendMsg(p)}>
                <Text style={[s.qpTxt, { color: selSpec.accent }, isRTL && s.rtl]} numberOfLines={2}>{p}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Input */}
        <View style={[s.inpRow, isRTL && { flexDirection:"row-reverse" }]}>
          <TextInput style={[s.inp, isRTL && s.rtl, { borderColor: selSpec.accent+"33" }]}
            value={input} onChangeText={setInput}
            placeholder={lang==="ar"?"اكتب سؤالك الطبي...":"Type your clinical question..."}
            placeholderTextColor="#AAA" multiline maxLength={600}
            onSubmitEditing={() => sendMsg()} returnKeyType="send" />
          <TouchableOpacity
            style={[s.sendBtn, { backgroundColor: selSpec.accent }, (!input.trim()||loading) && { opacity:0.4 }]}
            onPress={() => sendMsg()} disabled={!input.trim()||loading} activeOpacity={0.85}>
            <View style={{ width:0, height:0, borderTopWidth:6, borderBottomWidth:6, borderLeftWidth:9, borderTopColor:"transparent", borderBottomColor:"transparent", borderLeftColor:"#FFF", marginLeft:2 }} />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )

  // ── SPECIALTIES GRID ──────────────────────────────
  return (
    <SafeAreaView style={s.safe}>
      <View style={s.hdr}>
        <Text style={[s.hdrTitle, isRTL && s.rtl]}>
          {lang==="ar"?"التخصصات الطبية":lang==="fr"?"Spécialités Médicales":"Medical Specialties"}
        </Text>
        <Text style={[s.hdrSub, isRTL && s.rtl]}>
          {lang==="ar"?"مساعد AI متخصص لكل قسم":lang==="fr"?"IA spécialisée par département":"Dedicated AI for each department"}
        </Text>
        {/* Stats */}
        <View style={[s.statsRow, isRTL && { flexDirection:"row-reverse" }]}>
          <View style={s.statPill}><Text style={s.statPillTxt}>12 {lang==="ar"?"تخصصاً":"Specialties"}</Text></View>
          <View style={[s.statPill, { backgroundColor:"#F5F3FF" }]}><Text style={[s.statPillTxt, { color:"#7C3AED" }]}>Claude Sonnet</Text></View>
          <View style={[s.statPill, { backgroundColor:"#DCFCE7" }]}><Text style={[s.statPillTxt, { color:"#16A34A" }]}>100% AI</Text></View>
        </View>
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ padding:16, paddingBottom:90 }}>
        <View style={s.grid}>
          {SPECIALTIES.map((spec) => (
            <TouchableOpacity key={spec.id} style={[s.specCard, { backgroundColor: spec.color, borderColor: spec.accent+"22" }]}
              onPress={() => openSpec(spec)} activeOpacity={0.85}>
              {/* AI badge */}
              <View style={[s.aiBadge, { backgroundColor: spec.accent }]}>
                <Text style={s.aiBadgeTxt}>AI ✓</Text>
              </View>
              <Text style={{ fontSize:32, marginBottom:8 }}>{spec.icon}</Text>
              <Text style={[s.specName, { color: spec.accent }, isRTL && s.rtl]}>
                {spec.name[lang] ?? spec.name.en}
              </Text>
              <Text style={[s.specDesc, isRTL && s.rtl]}>
                {spec.desc[lang] ?? spec.desc.en}
              </Text>
              <View style={s.toolsPreview}>
                {spec.tools.slice(0,2).map((t: string) => (
                  <View key={t} style={[s.toolPreviewPill, { backgroundColor: spec.accent+"18" }]}>
                    <Text style={[s.toolPreviewTxt, { color: spec.accent }]} numberOfLines={1}>{t}</Text>
                  </View>
                ))}
                <View style={[s.toolPreviewPill, { backgroundColor: spec.accent+"18" }]}>
                  <Text style={[s.toolPreviewTxt, { color: spec.accent }]}>+{spec.tools.length-2}</Text>
                </View>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  )
}

const CARD_W = (W - 48) / 2
const s = StyleSheet.create({
  safe:    { flex:1, backgroundColor:"#F8F8F8" },
  rtl:     { textAlign:"right" },
  hdr:     { backgroundColor:"#FFF", paddingHorizontal:16, paddingTop:12, paddingBottom:12, borderBottomWidth:1, borderBottomColor:"#F0F0F0" },
  hdrTitle:{ fontSize:22, fontWeight:"800", color:"#111", letterSpacing:-0.4 },
  hdrSub:  { fontSize:12, color:"#888", fontWeight:"500", marginTop:2, marginBottom:10 },
  statsRow:{ flexDirection:"row", gap:8 },
  statPill:{ backgroundColor:Colors.primary2, borderRadius:20, paddingHorizontal:10, paddingVertical:4 },
  statPillTxt:{ fontSize:10, fontWeight:"700", color:Colors.primary },
  grid:    { flexDirection:"row", flexWrap:"wrap", gap:12 },
  specCard:{ width:CARD_W, borderRadius:18, borderWidth:1, padding:14, position:"relative", minHeight:180 },
  aiBadge: { position:"absolute", top:10, right:10, borderRadius:8, paddingHorizontal:7, paddingVertical:3 },
  aiBadgeTxt:{ fontSize:9, fontWeight:"900", color:"#FFF" },
  specName:{ fontSize:14, fontWeight:"900", letterSpacing:-0.3, marginBottom:3 },
  specDesc:{ fontSize:10, color:"#666", fontWeight:"600", marginBottom:10 },
  toolsPreview:{ flexDirection:"row", flexWrap:"wrap", gap:4 },
  toolPreviewPill:{ borderRadius:20, paddingHorizontal:8, paddingVertical:3 },
  toolPreviewTxt: { fontSize:9, fontWeight:"700" },
  // Specialty detail
  specHdr:  { paddingHorizontal:16, paddingVertical:14, flexDirection:"row", alignItems:"center" },
  backBtn:  { width:60, paddingVertical:6, paddingHorizontal:12, backgroundColor:"rgba(255,255,255,0.7)", borderRadius:10 },
  backTxt:  { fontSize:12, fontWeight:"700" },
  specHdrName:{ fontSize:16, fontWeight:"900", letterSpacing:-0.3, marginTop:4 },
  toolsBar: { paddingHorizontal:14, paddingVertical:10, borderBottomWidth:1 },
  toolsLbl: { fontSize:10, fontWeight:"800", textTransform:"uppercase", letterSpacing:.5, marginBottom:0 },
  toolBtn:  { paddingHorizontal:12, paddingVertical:7, borderRadius:20, borderWidth:1.5 },
  toolTxt:  { fontSize:11, fontWeight:"700" },
  chatArea: { flex:1, backgroundColor:"#F5F5F5" },
  mWrap:    { flexDirection:"row", alignItems:"flex-end", gap:8 },
  mWrapB:   { justifyContent:"flex-start" },
  mWrapU:   { justifyContent:"flex-end" },
  mAv:      { width:32, height:32, borderRadius:16, alignItems:"center", justifyContent:"center", flexShrink:0, borderWidth:1 },
  bubble:   { borderRadius:18, paddingHorizontal:13, paddingVertical:10 },
  bubB:     { backgroundColor:"#FFF", borderBottomLeftRadius:4, borderWidth:1, borderColor:"#EEEEEE" },
  bubTxt:   { fontSize:12.5, lineHeight:19 },
  bubTime:  { fontSize:9, marginTop:4, color:"#AAA", fontWeight:"500" },
  qpBar:    { backgroundColor:"#FFF", paddingHorizontal:14, paddingVertical:10, borderTopWidth:1 },
  qpLbl:    { fontSize:9, fontWeight:"800", textTransform:"uppercase", letterSpacing:.5, marginBottom:0 },
  qpBtn:    { paddingHorizontal:12, paddingVertical:7, borderRadius:12, borderWidth:1.5, maxWidth:200 },
  qpTxt:    { fontSize:10.5, fontWeight:"700", lineHeight:15 },
  inpRow:   { backgroundColor:"#FFF", borderTopWidth:1, borderTopColor:"#F0F0F0", paddingHorizontal:14, paddingVertical:10, flexDirection:"row", alignItems:"flex-end", gap:10 },
  inp:      { flex:1, borderWidth:1.5, borderRadius:22, paddingHorizontal:14, paddingVertical:9, fontSize:13, color:"#111", maxHeight:100, fontWeight:"500", backgroundColor:"#FAFAFA" },
  sendBtn:  { width:42, height:42, borderRadius:21, alignItems:"center", justifyContent:"center", flexShrink:0 },
})
