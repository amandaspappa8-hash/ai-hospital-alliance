#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║   CareBot Full Redesign - Auto Installer v2.0        ║
# ║   Run: bash ~/Downloads/carebot_install.sh           ║
# ╚══════════════════════════════════════════════════════╝
set -e
D="$HOME/ai-hospital-alliance/mobile"
cd "$D" || { echo "❌ Project not found at $D"; exit 1; }
echo ""; echo "🏥 CareBot Redesign Installer"; echo "📁 $D"; echo ""

# Backup
mkdir -p .backup_$(date +%H%M)
cp App.tsx .backup_$(date +%H%M)/App.tsx 2>/dev/null || true
cp constants/theme.ts .backup_$(date +%H%M)/theme.ts 2>/dev/null || true
echo "✅ Backup created"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 1: constants/theme.ts
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > constants/theme.ts << 'EOF'
import { Platform, TextStyle, ViewStyle } from "react-native"
export const Colors = {
  primary:"#2563EB", primary1:"#1D4ED8", primary2:"#EFF6FF", primary3:"#BFDBFE", primary4:"#DBEAFE",
  neutral900:"#0F172A", neutral800:"#1E293B", neutral700:"#334155", neutral500:"#64748B",
  neutral400:"#94A3B8", neutral300:"#CBD5E1", neutral200:"#E2E8F0", neutral100:"#F1F5F9",
  neutral50:"#F8FAFC", white:"#FFFFFF",
  success:"#16A34A", success1:"#DCFCE7", success2:"#BBF7D0",
  warning:"#D97706", warning1:"#FEF3C7",
  danger:"#DC2626",  danger1:"#FEE2E2",
  info:"#0891B2",    info1:"#E0F2FE",
}
export const Typography = {
  xs:10, sm:11, base:13, md:15, lg:17, xl:20, xxl:24, h1:28,
  regular:"400" as TextStyle["fontWeight"],
  medium:"500"  as TextStyle["fontWeight"],
  semibold:"600" as TextStyle["fontWeight"],
  bold:"700"    as TextStyle["fontWeight"],
  extrabold:"800" as TextStyle["fontWeight"],
  black:"900"   as TextStyle["fontWeight"],
  family: Platform.select({ ios:"System", android:"Roboto", default:"System" }),
}
export const Spacing  = { xs:4, sm:8, md:12, lg:16, xl:20, xxl:24, xxxl:32 }
export const Radius   = { sm:8, md:12, lg:16, xl:20, xxl:24, full:999 }
export const Shadow = {
  sm: Platform.select({
    ios:{ shadowColor:"#0F172A", shadowOffset:{width:0,height:1}, shadowOpacity:0.06, shadowRadius:3 },
    android:{ elevation:2 }, default:{},
  }) as ViewStyle,
  md: Platform.select({
    ios:{ shadowColor:"#0F172A", shadowOffset:{width:0,height:2}, shadowOpacity:0.08, shadowRadius:8 },
    android:{ elevation:4 }, default:{},
  }) as ViewStyle,
}
export function statusColor(s: string) {
  const m: Record<string,{bg:string;text:string}> = {
    available: {bg:"#DCFCE7",text:"#16A34A"}, on_call:  {bg:"#FEF3C7",text:"#D97706"},
    in_surgery:{bg:"#FEE2E2",text:"#DC2626"}, offline:  {bg:"#F1F5F9",text:"#64748B"},
    active:    {bg:"#DCFCE7",text:"#16A34A"}, critical: {bg:"#FEE2E2",text:"#DC2626"},
    scheduled: {bg:"#EFF6FF",text:"#2563EB"}, completed:{bg:"#DCFCE7",text:"#16A34A"},
    cancelled: {bg:"#FEE2E2",text:"#DC2626"},
  }
  return m[s] ?? {bg:"#F1F5F9",text:"#64748B"}
}
EOF
echo "✅ constants/theme.ts"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 2: App.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > App.tsx << 'EOF'
import { registerRootComponent } from "expo"
import { NavigationContainer } from "@react-navigation/native"
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs"
import { createStackNavigator } from "@react-navigation/stack"
import { StatusBar } from "expo-status-bar"
import { View } from "react-native"
import { GestureHandlerRootView } from "react-native-gesture-handler"
import { AuthProvider, useAuth } from "./src/context/AuthContext"
import { Colors, Typography } from "./constants/theme"
import SplashScreen    from "./src/screens/SplashScreen"
import LoginScreen     from "./src/screens/LoginScreen"
import HomeScreen      from "./src/screens/HomeScreen"
import DoctorsScreen   from "./src/screens/DoctorsScreen"
import AppointmentScreen from "./src/screens/AppointmentScreen"
import ChatbotScreen   from "./src/screens/ChatbotScreen"
import ProfileScreen   from "./src/screens/ProfileScreen"

const Tab = createBottomTabNavigator()
const Stack = createStackNavigator()

function TabIcon({ name, focused }: { name:string; focused:boolean }) {
  const c = focused ? Colors.primary : Colors.neutral400
  const b = { borderColor:c }
  if (name==="Home") return (
    <View style={{width:22,height:22,alignItems:"center",justifyContent:"center"}}>
      <View style={{width:18,height:13,borderWidth:2,...b,borderRadius:3,borderTopLeftRadius:0,borderTopRightRadius:0,position:"absolute",bottom:0}}/>
      <View style={{width:0,height:0,borderLeftWidth:12,borderRightWidth:12,borderBottomWidth:10,borderLeftColor:"transparent",borderRightColor:"transparent",borderBottomColor:c,position:"absolute",top:0}}/>
      <View style={{width:6,height:7,backgroundColor:c,borderRadius:1,position:"absolute",bottom:0}}/>
    </View>)
  if (name==="Doctors") return (
    <View style={{width:22,height:22,alignItems:"center",justifyContent:"center"}}>
      <View style={{width:12,height:12,borderRadius:6,borderWidth:2,...b,marginBottom:2}}/>
      <View style={{width:18,height:7,borderTopLeftRadius:9,borderTopRightRadius:9,borderWidth:2,borderBottomWidth:0,...b}}/>
    </View>)
  if (name==="Appointments") return (
    <View style={{width:22,height:22,alignItems:"center",justifyContent:"center"}}>
      <View style={{width:18,height:16,borderWidth:2,...b,borderRadius:3,marginTop:2}}/>
      <View style={{position:"absolute",top:0,left:4,width:3,height:5,backgroundColor:c,borderRadius:1}}/>
      <View style={{position:"absolute",top:0,right:4,width:3,height:5,backgroundColor:c,borderRadius:1}}/>
      <View style={{position:"absolute",top:10,left:5,width:4,height:2,backgroundColor:c,borderRadius:1}}/>
      <View style={{position:"absolute",top:10,right:5,width:4,height:2,backgroundColor:c,borderRadius:1}}/>
    </View>)
  if (name==="Chat") return (
    <View style={{width:22,height:22,alignItems:"center",justifyContent:"center"}}>
      <View style={{width:18,height:14,borderWidth:2,...b,borderRadius:8,marginBottom:4}}/>
      <View style={{width:0,height:0,borderLeftWidth:5,borderTopWidth:5,borderLeftColor:"transparent",borderTopColor:c,position:"absolute",bottom:1,left:5}}/>
    </View>)
  if (name==="Profile") return (
    <View style={{width:22,height:22,alignItems:"center",justifyContent:"center"}}>
      <View style={{width:10,height:10,borderRadius:5,borderWidth:2,...b,marginBottom:1}}/>
      <View style={{width:16,height:6,borderTopLeftRadius:8,borderTopRightRadius:8,borderWidth:2,borderBottomWidth:0,...b}}/>
    </View>)
  return <View style={{width:22,height:22}}/>
}

function MainTabs() {
  return (
    <Tab.Navigator screenOptions={({route})=>({
      tabBarIcon:({focused})=><TabIcon name={route.name} focused={focused}/>,
      tabBarStyle:{backgroundColor:Colors.white,borderTopColor:Colors.neutral200,borderTopWidth:1,height:68,paddingBottom:10,paddingTop:8},
      tabBarActiveTintColor:Colors.primary, tabBarInactiveTintColor:Colors.neutral400,
      tabBarLabelStyle:{fontSize:Typography.xs,fontWeight:Typography.semibold,marginTop:2},
      headerShown:false,
    })}>
      <Tab.Screen name="Home"         component={HomeScreen}/>
      <Tab.Screen name="Doctors"      component={DoctorsScreen}/>
      <Tab.Screen name="Appointments" component={AppointmentScreen}/>
      <Tab.Screen name="Chat"         component={ChatbotScreen}/>
      <Tab.Screen name="Profile"      component={ProfileScreen}/>
    </Tab.Navigator>)
}

function RootNav() {
  const {token,splash} = useAuth()
  if (splash) return <SplashScreen/>
  return (
    <Stack.Navigator screenOptions={{headerShown:false}}>
      {token ? <Stack.Screen name="Main"  component={MainTabs}/>
             : <Stack.Screen name="Login" component={LoginScreen}/>}
    </Stack.Navigator>)
}

function App() {
  return (
    <GestureHandlerRootView style={{flex:1}}>
      <AuthProvider>
        <NavigationContainer>
          <StatusBar style="dark" backgroundColor={Colors.white}/>
          <RootNav/>
        </NavigationContainer>
      </AuthProvider>
    </GestureHandlerRootView>)
}
registerRootComponent(App)
export default App
EOF
echo "✅ App.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 3: SplashScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/SplashScreen.tsx << 'EOF'
import { useEffect, useRef } from "react"
import { View, Text, StyleSheet, Animated, Easing } from "react-native"
import { Colors, Typography, Spacing } from "../../constants/theme"
export default function SplashScreen() {
  const scale = useRef(new Animated.Value(0.8)).current
  const opacity = useRef(new Animated.Value(0)).current
  useEffect(()=>{
    Animated.parallel([
      Animated.timing(scale,  {toValue:1,duration:700,easing:Easing.out(Easing.back(1.2)),useNativeDriver:true}),
      Animated.timing(opacity,{toValue:1,duration:500,useNativeDriver:true}),
    ]).start()
  },[])
  return (
    <View style={s.c}>
      <Animated.View style={[s.wrap,{transform:[{scale}],opacity}]}>
        <View style={s.box}><View style={s.bub}/><View style={s.dot}/></View>
        <Text style={s.brand}>Care<Text style={{fontWeight:"900"}}>Bot</Text></Text>
        <Text style={s.sub}>AI Healthcare Platform</Text>
      </Animated.View>
      <View style={s.loader}><View style={s.track}><View style={s.bar}/></View></View>
    </View>)
}
const s = StyleSheet.create({
  c:    {flex:1,backgroundColor:Colors.primary,alignItems:"center",justifyContent:"center"},
  wrap: {alignItems:"center"},
  box:  {width:88,height:88,backgroundColor:"rgba(255,255,255,0.2)",borderRadius:28,alignItems:"center",justifyContent:"center",marginBottom:Spacing.lg},
  bub:  {width:44,height:36,backgroundColor:Colors.white,borderRadius:18,borderBottomLeftRadius:4,position:"absolute"},
  dot:  {width:8,height:8,backgroundColor:Colors.primary,borderRadius:4,position:"absolute",top:12,left:19},
  brand:{fontSize:32,fontWeight:"400",color:Colors.white,letterSpacing:-0.5},
  sub:  {fontSize:Typography.base,color:"rgba(255,255,255,0.7)",marginTop:4,fontWeight:"500"},
  loader:{position:"absolute",bottom:60,left:0,right:0,alignItems:"center"},
  track: {width:120,height:3,backgroundColor:"rgba(255,255,255,0.25)",borderRadius:2,overflow:"hidden"},
  bar:   {width:"60%",height:"100%",backgroundColor:Colors.white,borderRadius:2},
})
EOF
echo "✅ SplashScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 4: LoginScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/LoginScreen.tsx << 'EOF'
import { useState } from "react"
import { View,Text,TextInput,TouchableOpacity,StyleSheet,KeyboardAvoidingView,Platform,ScrollView,Alert,ActivityIndicator } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors,Typography,Spacing,Radius } from "../../constants/theme"
import { login } from "../api/client"
import { useAuth } from "../context/AuthContext"
import { t,setLang,getLang,LANGS } from "../i18n"
export default function LoginScreen() {
  const {login:authLogin} = useAuth()
  const [username,setUsername] = useState("")
  const [password,setPassword] = useState("")
  const [loading,setLoading]   = useState(false)
  const [showPass,setShowPass] = useState(false)
  const [lang,setLangState]    = useState(getLang())
  const isRTL = lang==="ar"
  function switchLang(c:string){setLang(c as any);setLangState(c as any)}
  async function handleLogin(){
    if(!username.trim()||!password.trim()){Alert.alert("","Please enter username and password");return}
    setLoading(true)
    try{ const d=await login(username,password); authLogin(d.access_token,d.user) }
    catch(e:any){ Alert.alert("Login Failed",e?.response?.data?.detail??"Check your credentials") }
    finally{ setLoading(false) }
  }
  return (
    <SafeAreaView style={s.safe}>
      <KeyboardAvoidingView style={{flex:1}} behavior={Platform.OS==="ios"?"padding":undefined}>
        <ScrollView contentContainerStyle={s.scroll} keyboardShouldPersistTaps="handled" showsVerticalScrollIndicator={false}>
          <View style={[s.langRow,isRTL&&{flexDirection:"row-reverse"}]}>
            {LANGS.map(l=>(
              <TouchableOpacity key={l.code} style={[s.langBtn,lang===l.code&&s.langOn]} onPress={()=>switchLang(l.code)}>
                <Text style={[s.langTxt,lang===l.code&&s.langTxtOn]}>{l.flag} {l.code.toUpperCase()}</Text>
              </TouchableOpacity>))}
          </View>
          <View style={s.logo}>
            <View style={s.logoBox}><View style={s.logoBub}/><View style={s.logoDot}/></View>
            <Text style={s.logoTxt}>Care<Text style={{fontWeight:"900"}}>Bot</Text></Text>
            <Text style={s.logoSub}>AI Healthcare Platform</Text>
          </View>
          <View style={s.card}>
            <Text style={[s.title,isRTL&&s.rtl]}>{t("welcome_back")}</Text>
            <Text style={[s.sub,isRTL&&s.rtl]}>{t("sign_in_sub")}</Text>
            {[{label:t("username"),val:username,set:setUsername,secure:false},{label:t("password"),val:password,set:setPassword,secure:!showPass}].map((f,i)=>(
              <View key={i} style={s.field}>
                <Text style={[s.lbl,isRTL&&s.rtl]}>{f.label}</Text>
                <View style={s.inputWrap}>
                  <TextInput style={[s.input,isRTL&&s.rtl]} value={f.val} onChangeText={f.set} placeholder={f.label} placeholderTextColor={Colors.neutral400} secureTextEntry={f.secure} autoCapitalize="none" autoCorrect={false}/>
                  {i===1&&<TouchableOpacity onPress={()=>setShowPass(!showPass)} style={{padding:4}}><Text style={{fontSize:11,color:Colors.neutral400}}>{showPass?"hide":"show"}</Text></TouchableOpacity>}
                </View>
              </View>))}
            <TouchableOpacity style={[s.btn,loading&&{opacity:0.7}]} onPress={handleLogin} disabled={loading} activeOpacity={0.85}>
              {loading?<ActivityIndicator color={Colors.white}/>:<Text style={s.btnTxt}>{t("sign_in")}</Text>}
            </TouchableOpacity>
            <View style={s.div}><View style={s.divLine}/><Text style={s.divTxt}>{t("quick_login")}</Text><View style={s.divLine}/></View>
            <View style={[s.qRow,isRTL&&{flexDirection:"row-reverse"}]}>
              {[{l:"Admin",u:"admin",p:"admin123"},{l:"Doctor",u:"doctor1",p:"doctor123"},{l:"Nurse",u:"nurse1",p:"nurse123"}].map(q=>(
                <TouchableOpacity key={q.l} style={s.qBtn} onPress={()=>{setUsername(q.u);setPassword(q.p)}} activeOpacity={0.75}>
                  <Text style={s.qTxt}>{q.l}</Text>
                </TouchableOpacity>))}
            </View>
          </View>
          <Text style={s.footer}>AI Hospital Alliance · Secure Medical Platform</Text>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>)
}
const s = StyleSheet.create({
  safe:{flex:1,backgroundColor:Colors.neutral50},
  scroll:{flexGrow:1,paddingHorizontal:Spacing.lg,paddingBottom:Spacing.xxl},
  rtl:{textAlign:"right"},
  langRow:{flexDirection:"row",gap:6,paddingTop:Spacing.md,marginBottom:Spacing.lg},
  langBtn:{flex:1,paddingVertical:7,borderRadius:Radius.sm,borderWidth:1.5,borderColor:Colors.neutral200,backgroundColor:Colors.white,alignItems:"center"},
  langOn:{borderColor:Colors.primary,backgroundColor:Colors.primary2},
  langTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral500},
  langTxtOn:{color:Colors.primary},
  logo:{alignItems:"center",paddingVertical:Spacing.xxl},
  logoBox:{width:72,height:72,backgroundColor:Colors.primary,borderRadius:22,alignItems:"center",justifyContent:"center",marginBottom:Spacing.md},
  logoBub:{width:38,height:30,backgroundColor:Colors.white,borderRadius:15,borderBottomLeftRadius:4,position:"absolute"},
  logoDot:{width:7,height:7,backgroundColor:Colors.primary,borderRadius:4,position:"absolute",top:22,left:19},
  logoTxt:{fontSize:Typography.xxl,fontWeight:"400",color:Colors.neutral900,letterSpacing:-0.5},
  logoSub:{fontSize:Typography.sm,color:Colors.neutral500,marginTop:4,fontWeight:"500"},
  card:{backgroundColor:Colors.white,borderRadius:Radius.xl,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.xl},
  title:{fontSize:Typography.xl,fontWeight:Typography.black,color:Colors.neutral900,marginBottom:4},
  sub:{fontSize:Typography.sm,color:Colors.neutral500,marginBottom:Spacing.xl},
  field:{marginBottom:Spacing.md},
  lbl:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral700,marginBottom:6,textTransform:"uppercase",letterSpacing:0.5},
  inputWrap:{flexDirection:"row",alignItems:"center",borderWidth:1.5,borderColor:Colors.neutral200,borderRadius:Radius.md,paddingHorizontal:Spacing.md,height:48,backgroundColor:Colors.neutral50},
  input:{flex:1,fontSize:Typography.base,color:Colors.neutral900,fontWeight:"500"},
  btn:{backgroundColor:Colors.primary,borderRadius:Radius.md,height:52,alignItems:"center",justifyContent:"center",marginTop:Spacing.sm},
  btnTxt:{fontSize:Typography.md,fontWeight:Typography.black,color:Colors.white,letterSpacing:0.3},
  div:{flexDirection:"row",alignItems:"center",gap:10,marginVertical:Spacing.lg},
  divLine:{flex:1,height:1,backgroundColor:Colors.neutral200},
  divTxt:{fontSize:Typography.xs,color:Colors.neutral400,fontWeight:"600"},
  qRow:{flexDirection:"row",gap:8},
  qBtn:{flex:1,paddingVertical:10,borderRadius:Radius.sm,borderWidth:1.5,borderColor:Colors.primary3,backgroundColor:Colors.primary2,alignItems:"center"},
  qTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.primary},
  footer:{textAlign:"center",fontSize:Typography.xs,color:Colors.neutral400,marginTop:Spacing.xl,fontWeight:"500"},
})
EOF
echo "✅ LoginScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 5: HomeScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/HomeScreen.tsx << 'EOF'
import { useState,useEffect,useCallback } from "react"
import { View,Text,ScrollView,TouchableOpacity,StyleSheet,RefreshControl,ActivityIndicator } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors,Typography,Spacing,Radius,statusColor } from "../../constants/theme"
import { useAuth } from "../context/AuthContext"
import { getDoctors,getPatients,getAlerts } from "../api/client"
import { t,setLang,getLang,LANGS } from "../i18n"

const FEATS = [
  {key:"s",lbl:{en:"Symptom\nCheck",ar:"فحص\nالأعراض",fr:"Vérif.\nSymptômes"},bg:"#EFF6FF",c:Colors.primary},
  {key:"t",lbl:{en:"Telecon-\nsult",ar:"استشارة\nبُعد",fr:"Télé-\nconsult"},bg:"#F0FDF4",c:Colors.success},
  {key:"i",lbl:{en:"Insurance",ar:"التأمين",fr:"Assurance"},bg:"#FFFBEB",c:Colors.warning},
  {key:"h",lbl:{en:"Health\nMonitor",ar:"مراقبة\nالصحة",fr:"Santé\nMonit."},bg:"#FFF1F2",c:"#E11D48"},
  {key:"m",lbl:{en:"Medication",ar:"الأدوية",fr:"Médication"},bg:"#F5F3FF",c:"#7C3AED"},
  {key:"r",lbl:{en:"Scan\nReport",ar:"تقرير\nالمسح",fr:"Rapport\nScan"},bg:"#FFF7ED",c:"#EA580C"},
]
const MOCK_DR = [
  {name:"Leslie Alexander",specialty:"Headaches & Migraines",rating:4.9,status:"available"},
  {name:"Adam Max",specialty:"Psychology",rating:4.9,status:"available"},
  {name:"Cecily Welsh",specialty:"Dentist",rating:4.8,status:"on_call"},
]

export default function HomeScreen() {
  const {user} = useAuth()
  const [lang,setLangState] = useState(getLang())
  const [doctors,setDoctors] = useState<any[]>([])
  const [alerts,setAlerts]   = useState<any[]>([])
  const [loading,setLoading] = useState(true)
  const [refreshing,setRefreshing] = useState(false)
  const isRTL = lang==="ar"

  function greet(){
    const h=new Date().getHours()
    return h<12?t("greeting_morning"):h<17?t("greeting_afternoon"):t("greeting_evening")
  }
  async function load(){
    try{
      const [d,a]=await Promise.all([getDoctors(),getAlerts()])
      if(Array.isArray(d)&&d.length>0) setDoctors(d.slice(0,4))
      if(Array.isArray(a)&&a.length>0) setAlerts(a.slice(0,3))
    }catch{}
    setLoading(false)
  }
  useEffect(()=>{load()},[])
  const onRefresh=useCallback(async()=>{setRefreshing(true);await load();setRefreshing(false)},[])
  function switchLang(c:string){setLang(c as any);setLangState(c as any)}

  const shown = doctors.length>0?doctors:MOCK_DR
  const today = new Date().toLocaleDateString(lang==="ar"?"ar-SA":lang==="fr"?"fr-FR":"en-US",{weekday:"long",day:"numeric",month:"long"})

  return (
    <SafeAreaView style={s.safe}>
      <View style={s.hdr}>
        <View style={[s.hdrTop,isRTL&&{flexDirection:"row-reverse"}]}>
          <View>
            <Text style={[s.greet,isRTL&&s.rtl]}>{greet()},</Text>
            <Text style={[s.name,isRTL&&s.rtl]} numberOfLines={1}>{user?.full_name??user?.username??"Robertson"} 👋</Text>
            <Text style={[s.date,isRTL&&s.rtl]}>{today}</Text>
          </View>
          <TouchableOpacity style={s.notif}>
            <View style={s.notifDot}/>
            <View style={{width:14,height:14,borderRadius:7,borderWidth:2,borderColor:Colors.neutral700}}/>
          </TouchableOpacity>
        </View>
        <View style={[s.langRow,isRTL&&{flexDirection:"row-reverse"}]}>
          {LANGS.map(l=>(
            <TouchableOpacity key={l.code} style={[s.langBtn,lang===l.code&&s.langOn]} onPress={()=>switchLang(l.code)}>
              <Text style={[s.langTxt,lang===l.code&&s.langTxtOn]}>{l.flag} {l.code.toUpperCase()}</Text>
            </TouchableOpacity>))}
        </View>
      </View>

      <ScrollView style={s.scroll} showsVerticalScrollIndicator={false}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primary}/>}>

        {/* Banner */}
        <TouchableOpacity style={s.banner} activeOpacity={0.88}>
          <View style={s.banIco}><View style={s.banBub}/><View style={s.banDot}/></View>
          <View style={{flex:1}}>
            <Text style={[s.banTitle,isRTL&&s.rtl]} numberOfLines={2}>{t("discover_ai")}</Text>
            <Text style={[s.banSub,isRTL&&s.rtl]} numberOfLines={1}>{t("discover_sub")}</Text>
          </View>
          <View style={s.banArr}><View style={{width:0,height:0,borderTopWidth:6,borderBottomWidth:6,borderLeftWidth:8,borderTopColor:"transparent",borderBottomColor:"transparent",borderLeftColor:Colors.white}}/></View>
        </TouchableOpacity>

        {/* Stats */}
        <View style={[s.statsRow,isRTL&&{flexDirection:"row-reverse"}]}>
          <View style={s.stat}><Text style={s.statL}>Heart Rate</Text><Text style={[s.statV,{color:Colors.danger}]}>97 <Text style={s.statU}>bpm</Text></Text><Text style={[s.statT,{color:Colors.success}]}>Normal</Text></View>
          <View style={s.stat}><Text style={s.statL}>SpO2</Text><Text style={[s.statV,{color:Colors.primary}]}>98<Text style={s.statU}>%</Text></Text><Text style={[s.statT,{color:Colors.success}]}>Excellent</Text></View>
        </View>

        {/* Features */}
        <View style={[s.sh,isRTL&&{flexDirection:"row-reverse"}]}><Text style={[s.shTitle,isRTL&&s.rtl]}>{t("our_features")}</Text></View>
        <View style={s.featGrid}>
          {FEATS.map(f=>(
            <TouchableOpacity key={f.key} style={s.featItem} activeOpacity={0.8}>
              <View style={[s.featIco,{backgroundColor:f.bg}]}>
                <View style={{width:20,height:20,borderRadius:5,borderWidth:2,borderColor:f.c}}/>
              </View>
              <Text style={[s.featLbl,isRTL&&s.rtl]} numberOfLines={2}>{(f.lbl as any)[lang]??(f.lbl as any).en}</Text>
            </TouchableOpacity>))}
        </View>

        {/* Doctors */}
        <View style={[s.sh,isRTL&&{flexDirection:"row-reverse"}]}>
          <Text style={[s.shTitle,isRTL&&s.rtl]}>{t("top_doctors")}</Text>
          <TouchableOpacity><Text style={s.seeAll}>{t("see_all")}</Text></TouchableOpacity>
        </View>
        {loading?<ActivityIndicator color={Colors.primary} style={{paddingVertical:Spacing.xl}}/>:(
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{marginHorizontal:-Spacing.lg,paddingHorizontal:Spacing.lg}}>
            {shown.map((d,i)=>{
              const sc=statusColor(d.status??"available")
              return (
                <TouchableOpacity key={i} style={s.docCard} activeOpacity={0.85}>
                  <View style={s.docImg}>
                    <View style={{width:28,height:28,borderRadius:14,borderWidth:2,borderColor:Colors.primary,marginBottom:2}}/>
                    <View style={{width:36,height:14,borderTopLeftRadius:18,borderTopRightRadius:18,borderWidth:2,borderBottomWidth:0,borderColor:Colors.primary}}/>
                    <View style={[s.avail,{backgroundColor:sc.text}]}/>
                  </View>
                  <View style={s.docBody}>
                    <Text style={[s.docName,isRTL&&s.rtl]} numberOfLines={1}>Dr. {d.name??d.full_name}</Text>
                    <Text style={[s.docSpec,isRTL&&s.rtl]} numberOfLines={1}>{d.specialty??d.specialization}</Text>
                    <Text style={s.docRat}>★ {(d.rating??4.9).toFixed(1)}</Text>
                    <TouchableOpacity style={s.bookBtn}><Text style={s.bookTxt}>{t("book_now")}</Text></TouchableOpacity>
                  </View>
                </TouchableOpacity>)})}
          </ScrollView>)}

        {/* Alerts */}
        {alerts.length>0&&(
          <>
            <View style={[s.sh,isRTL&&{flexDirection:"row-reverse"}]}>
              <Text style={[s.shTitle,isRTL&&s.rtl]}>Active Alerts</Text>
              <View style={s.alertBadge}><Text style={s.alertBadgeTxt}>{alerts.length}</Text></View>
            </View>
            {alerts.map((a,i)=>{
              const sc=statusColor(a.severity??"active")
              return (
                <TouchableOpacity key={i} style={s.alertCard}>
                  <View style={[s.alertDot,{backgroundColor:a.severity==="critical"?Colors.danger:Colors.warning}]}/>
                  <View style={{flex:1}}>
                    <Text style={[s.alertTitle,isRTL&&s.rtl]} numberOfLines={1}>{a.patient_name??"Patient"}</Text>
                    <Text style={[s.alertMsg,isRTL&&s.rtl]} numberOfLines={2}>{a.message??a.description}</Text>
                  </View>
                  <View style={[s.sevBadge,{backgroundColor:sc.bg}]}><Text style={[s.sevTxt,{color:sc.text}]}>{t(a.severity??"active")}</Text></View>
                </TouchableOpacity>)})}
          </>)}

        {/* Upcoming */}
        <View style={[s.sh,isRTL&&{flexDirection:"row-reverse"}]}>
          <Text style={[s.shTitle,isRTL&&s.rtl]}>{t("appointment_scheduling")}</Text>
          <TouchableOpacity><Text style={s.seeAll}>{t("see_all")}</Text></TouchableOpacity>
        </View>
        <TouchableOpacity style={s.apptCard}>
          <View style={s.apptDate}><Text style={s.apptDay}>17</Text><Text style={s.apptMon}>APR</Text></View>
          <View style={{flex:1}}>
            <Text style={[s.apptDr,isRTL&&s.rtl]} numberOfLines={1}>Dr. Leslie Alexander</Text>
            <Text style={[s.apptSub,isRTL&&s.rtl]}>2:00 PM · Pearl Dental Clinic</Text>
          </View>
          <View style={s.apptBadge}><Text style={s.apptBadgeTxt}>{t("available")}</Text></View>
        </TouchableOpacity>

        <View style={{height:Spacing.xxl}}/>
      </ScrollView>
    </SafeAreaView>)
}
const s = StyleSheet.create({
  safe:{flex:1,backgroundColor:Colors.neutral50},
  rtl:{textAlign:"right"},
  hdr:{backgroundColor:Colors.white,paddingHorizontal:Spacing.lg,paddingTop:Spacing.md,paddingBottom:Spacing.md,borderBottomWidth:1,borderBottomColor:Colors.neutral200},
  hdrTop:{flexDirection:"row",justifyContent:"space-between",alignItems:"flex-start",marginBottom:Spacing.md},
  greet:{fontSize:Typography.sm,color:Colors.neutral500,fontWeight:"500"},
  name:{fontSize:Typography.xl,fontWeight:Typography.black,color:Colors.neutral900,letterSpacing:-0.3,marginTop:1},
  date:{fontSize:Typography.xs,color:Colors.neutral400,marginTop:2,fontWeight:"500"},
  notif:{width:40,height:40,borderRadius:20,borderWidth:1.5,borderColor:Colors.neutral200,backgroundColor:Colors.white,alignItems:"center",justifyContent:"center",position:"relative"},
  notifDot:{width:8,height:8,borderRadius:4,backgroundColor:Colors.danger,position:"absolute",top:6,right:6,zIndex:1,borderWidth:1.5,borderColor:Colors.white},
  langRow:{flexDirection:"row",gap:6},
  langBtn:{flex:1,paddingVertical:6,borderRadius:Radius.sm,borderWidth:1.5,borderColor:Colors.neutral200,backgroundColor:Colors.white,alignItems:"center"},
  langOn:{borderColor:Colors.primary,backgroundColor:Colors.primary2},
  langTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral500},
  langTxtOn:{color:Colors.primary},
  scroll:{flex:1,paddingHorizontal:Spacing.lg},
  banner:{backgroundColor:Colors.primary,borderRadius:Radius.lg,padding:Spacing.md,flexDirection:"row",alignItems:"center",gap:Spacing.sm,marginTop:Spacing.md,marginBottom:Spacing.md},
  banIco:{width:44,height:44,backgroundColor:"rgba(255,255,255,0.2)",borderRadius:12,alignItems:"center",justifyContent:"center"},
  banBub:{width:26,height:22,backgroundColor:Colors.white,borderRadius:11,borderBottomLeftRadius:3,position:"absolute"},
  banDot:{width:5,height:5,backgroundColor:Colors.primary,borderRadius:3,position:"absolute",top:8,left:8},
  banTitle:{fontSize:Typography.base,fontWeight:Typography.black,color:Colors.white,lineHeight:18},
  banSub:{fontSize:Typography.xs,color:"rgba(255,255,255,0.75)",marginTop:2},
  banArr:{width:30,height:30,backgroundColor:"rgba(255,255,255,0.2)",borderRadius:15,alignItems:"center",justifyContent:"center"},
  statsRow:{flexDirection:"row",gap:Spacing.sm,marginBottom:Spacing.md},
  stat:{flex:1,backgroundColor:Colors.white,borderRadius:Radius.md,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.md},
  statL:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral400,textTransform:"uppercase",letterSpacing:0.3},
  statV:{fontSize:22,fontWeight:Typography.black,letterSpacing:-0.5,marginTop:4},
  statU:{fontSize:11,fontWeight:"600"},
  statT:{fontSize:Typography.xs,fontWeight:Typography.bold,marginTop:4},
  sh:{flexDirection:"row",justifyContent:"space-between",alignItems:"center",marginBottom:Spacing.sm,marginTop:Spacing.xs},
  shTitle:{fontSize:Typography.md,fontWeight:Typography.black,color:Colors.neutral900,letterSpacing:-0.2},
  seeAll:{fontSize:Typography.sm,fontWeight:Typography.bold,color:Colors.primary},
  featGrid:{flexDirection:"row",flexWrap:"wrap",gap:Spacing.sm,marginBottom:Spacing.md},
  featItem:{width:"30%",backgroundColor:Colors.white,borderRadius:Radius.md,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.md,alignItems:"center",gap:Spacing.sm},
  featIco:{width:44,height:44,borderRadius:12,alignItems:"center",justifyContent:"center"},
  featLbl:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral800,textAlign:"center",lineHeight:15},
  docCard:{width:152,backgroundColor:Colors.white,borderRadius:Radius.lg,borderWidth:1,borderColor:Colors.neutral200,marginRight:Spacing.sm,overflow:"hidden"},
  docImg:{height:90,backgroundColor:Colors.primary4,alignItems:"center",justifyContent:"center",position:"relative"},
  avail:{position:"absolute",top:8,right:8,width:12,height:12,borderRadius:6,borderWidth:2,borderColor:Colors.white},
  docBody:{padding:Spacing.sm},
  docName:{fontSize:Typography.sm,fontWeight:Typography.black,color:Colors.neutral900},
  docSpec:{fontSize:Typography.xs,fontWeight:"600",color:Colors.primary,marginTop:1},
  docRat:{fontSize:Typography.xs,color:Colors.warning,fontWeight:Typography.bold,marginTop:3},
  bookBtn:{backgroundColor:Colors.primary,borderRadius:8,paddingVertical:6,alignItems:"center",marginTop:8},
  bookTxt:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.white,letterSpacing:0.3},
  alertBadge:{backgroundColor:Colors.danger,borderRadius:Radius.full,width:20,height:20,alignItems:"center",justifyContent:"center"},
  alertBadgeTxt:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.white},
  alertCard:{backgroundColor:Colors.white,borderRadius:Radius.md,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.md,flexDirection:"row",alignItems:"flex-start",gap:Spacing.sm,marginBottom:Spacing.sm},
  alertDot:{width:10,height:10,borderRadius:5,marginTop:3},
  alertTitle:{fontSize:Typography.base,fontWeight:Typography.bold,color:Colors.neutral900},
  alertMsg:{fontSize:Typography.xs,color:Colors.neutral500,marginTop:2,lineHeight:16},
  sevBadge:{borderRadius:Radius.full,paddingHorizontal:8,paddingVertical:3},
  sevTxt:{fontSize:Typography.xs,fontWeight:Typography.bold},
  apptCard:{backgroundColor:Colors.white,borderRadius:Radius.lg,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.md,flexDirection:"row",alignItems:"center",gap:Spacing.md,marginBottom:Spacing.sm},
  apptDate:{backgroundColor:Colors.primary2,borderRadius:10,padding:Spacing.sm,alignItems:"center",minWidth:48},
  apptDay:{fontSize:20,fontWeight:Typography.black,color:Colors.primary,lineHeight:22},
  apptMon:{fontSize:9,fontWeight:Typography.black,color:Colors.primary,letterSpacing:0.5},
  apptDr:{fontSize:Typography.base,fontWeight:Typography.black,color:Colors.neutral900},
  apptSub:{fontSize:Typography.xs,color:Colors.neutral500,marginTop:2},
  apptBadge:{backgroundColor:Colors.success1,borderRadius:Radius.full,paddingHorizontal:8,paddingVertical:4},
  apptBadgeTxt:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.success},
})
EOF
echo "✅ HomeScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 6: DoctorsScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/DoctorsScreen.tsx << 'EOF'
import { useState,useEffect,useCallback } from "react"
import { View,Text,ScrollView,TouchableOpacity,StyleSheet,TextInput,ActivityIndicator,RefreshControl } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors,Typography,Spacing,Radius,statusColor } from "../../constants/theme"
import { getDoctors } from "../api/client"
import { t,getLang } from "../i18n"
const SPECS=["All","Cardiology","Neurology","Orthopedics","General","Dentistry","Psychology"]
const MOCK=[
  {id:1,name:"Leslie Alexander",specialty:"Headaches & Migraines",status:"available",rating:4.9,patients:250,experience:12},
  {id:2,name:"Adam Max",specialty:"Psychology",status:"available",rating:4.9,patients:180,experience:8},
  {id:3,name:"Cecily Welsh",specialty:"Dentistry",status:"on_call",rating:4.8,patients:310,experience:15},
  {id:4,name:"Jane Cooper",specialty:"Cardiology",status:"available",rating:4.9,patients:420,experience:18},
  {id:5,name:"Wade Warren",specialty:"Neurology",status:"in_surgery",rating:4.7,patients:290,experience:14},
  {id:6,name:"Albert Flores",specialty:"Orthopedics",status:"offline",rating:4.6,patients:200,experience:10},
]
export default function DoctorsScreen() {
  const lang=getLang(); const isRTL=lang==="ar"
  const [search,setSearch]=useState("")
  const [filter,setFilter]=useState("All")
  const [doctors,setDoctors]=useState<any[]>(MOCK)
  const [loading,setLoading]=useState(true)
  const [refreshing,setRefreshing]=useState(false)
  async function load(){
    try{ const d=await getDoctors(); if(Array.isArray(d)&&d.length>0) setDoctors(d) }catch{}
    setLoading(false)
  }
  useEffect(()=>{load()},[])
  const onRefresh=useCallback(async()=>{setRefreshing(true);await load();setRefreshing(false)},[])
  const filtered=doctors.filter(d=>{
    const nm=(d.name??d.full_name??"").toLowerCase()
    const sp=(d.specialty??d.specialization??"").toLowerCase()
    return nm.includes(search.toLowerCase())||sp.includes(search.toLowerCase())
  }).filter(d=>filter==="All"||(d.specialty??d.specialization??"").toLowerCase().includes(filter.toLowerCase()))

  return (
    <SafeAreaView style={s.safe}>
      <View style={s.hdr}>
        <Text style={[s.title,isRTL&&s.rtl]}>{t("find_doctor")}</Text>
        <Text style={[s.sub,isRTL&&s.rtl]}>{filtered.length} {t("specialists")}</Text>
        <View style={[s.searchWrap,isRTL&&{flexDirection:"row-reverse"}]}>
          <TextInput style={[s.searchInput,isRTL&&s.rtl]} value={search} onChangeText={setSearch} placeholder={t("search_doctor")} placeholderTextColor={Colors.neutral400}/>
          {search.length>0&&<TouchableOpacity onPress={()=>setSearch("")}><Text style={{color:Colors.neutral400,fontSize:18}}>×</Text></TouchableOpacity>}
        </View>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={s.chips}>
          {SPECS.map(sp=>(
            <TouchableOpacity key={sp} style={[s.chip,filter===sp&&s.chipOn]} onPress={()=>setFilter(sp)}>
              <Text style={[s.chipTxt,filter===sp&&s.chipTxtOn]}>{sp}</Text>
            </TouchableOpacity>))}
        </ScrollView>
      </View>
      {loading?<ActivityIndicator color={Colors.primary} style={{flex:1}}/>:(
        <ScrollView style={s.list} showsVerticalScrollIndicator={false}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primary}/>}>
          {filtered.map((d,i)=>{
            const sc=statusColor(d.status??"available")
            return (
              <TouchableOpacity key={d.id??i} style={s.card} activeOpacity={0.85}>
                <View style={[s.cardRow,isRTL&&{flexDirection:"row-reverse"}]}>
                  <View style={s.avWrap}>
                    <View style={s.av}><Text style={s.avI}>{(d.name??d.full_name??"D").charAt(0)}</Text></View>
                    <View style={[s.sDot,{backgroundColor:sc.text}]}/>
                  </View>
                  <View style={[s.info,isRTL&&{alignItems:"flex-end"}]}>
                    <Text style={[s.dName,isRTL&&s.rtl]} numberOfLines={1}>Dr. {d.name??d.full_name}</Text>
                    <Text style={[s.dSpec,isRTL&&s.rtl]} numberOfLines={1}>{d.specialty??d.specialization}</Text>
                    <View style={[s.meta,isRTL&&{flexDirection:"row-reverse"}]}>
                      <Text style={s.rat}>★ {(d.rating??4.8).toFixed(1)}</Text>
                      <View style={s.metaDot}/>
                      <Text style={s.metaTxt}>{d.patients??200}+ pts</Text>
                      <View style={s.metaDot}/>
                      <Text style={s.metaTxt}>{d.experience??10}yr</Text>
                    </View>
                  </View>
                  <View style={[s.sBadge,{backgroundColor:sc.bg}]}>
                    <Text style={[s.sTxt,{color:sc.text}]}>{t(d.status??"available")}</Text>
                  </View>
                </View>
                <View style={[s.actions,isRTL&&{flexDirection:"row-reverse"}]}>
                  <TouchableOpacity style={s.actBtn}><Text style={s.actTxt}>{t("book_now")}</Text></TouchableOpacity>
                  <TouchableOpacity style={s.actBtnO}><Text style={s.actTxtO}>{t("video_call")}</Text></TouchableOpacity>
                </View>
              </TouchableOpacity>)})}
          <View style={{height:Spacing.xxl}}/>
        </ScrollView>)}
    </SafeAreaView>)
}
const s=StyleSheet.create({
  safe:{flex:1,backgroundColor:Colors.neutral50},rtl:{textAlign:"right"},
  hdr:{backgroundColor:Colors.white,paddingHorizontal:Spacing.lg,paddingTop:Spacing.md,paddingBottom:Spacing.sm,borderBottomWidth:1,borderBottomColor:Colors.neutral200},
  title:{fontSize:Typography.xl,fontWeight:Typography.black,color:Colors.neutral900,letterSpacing:-0.3},
  sub:{fontSize:Typography.sm,color:Colors.neutral500,marginTop:2,fontWeight:"500",marginBottom:Spacing.md},
  searchWrap:{flexDirection:"row",alignItems:"center",backgroundColor:Colors.neutral50,borderWidth:1.5,borderColor:Colors.neutral200,borderRadius:Radius.md,paddingHorizontal:Spacing.md,height:46,marginBottom:Spacing.sm},
  searchInput:{flex:1,fontSize:Typography.base,color:Colors.neutral900,fontWeight:"500"},
  chips:{marginBottom:Spacing.sm},
  chip:{paddingHorizontal:14,paddingVertical:6,borderRadius:Radius.full,borderWidth:1.5,borderColor:Colors.neutral200,backgroundColor:Colors.white,marginRight:8},
  chipOn:{borderColor:Colors.primary,backgroundColor:Colors.primary2},
  chipTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral500},
  chipTxtOn:{color:Colors.primary},
  list:{flex:1,paddingHorizontal:Spacing.lg,paddingTop:Spacing.md},
  card:{backgroundColor:Colors.white,borderRadius:Radius.lg,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.md,marginBottom:Spacing.sm},
  cardRow:{flexDirection:"row",alignItems:"flex-start",gap:Spacing.sm},
  avWrap:{position:"relative"},
  av:{width:52,height:52,borderRadius:26,backgroundColor:Colors.primary2,alignItems:"center",justifyContent:"center",borderWidth:2,borderColor:Colors.primary3},
  avI:{fontSize:Typography.lg,fontWeight:Typography.black,color:Colors.primary},
  sDot:{width:12,height:12,borderRadius:6,position:"absolute",bottom:0,right:0,borderWidth:2,borderColor:Colors.white},
  info:{flex:1,minWidth:0},
  dName:{fontSize:Typography.md,fontWeight:Typography.black,color:Colors.neutral900},
  dSpec:{fontSize:Typography.sm,fontWeight:"600",color:Colors.primary,marginTop:2},
  meta:{flexDirection:"row",alignItems:"center",marginTop:5,gap:4,flexWrap:"wrap"},
  rat:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.warning},
  metaDot:{width:3,height:3,borderRadius:1.5,backgroundColor:Colors.neutral300},
  metaTxt:{fontSize:Typography.xs,color:Colors.neutral500,fontWeight:"500"},
  sBadge:{borderRadius:Radius.full,paddingHorizontal:10,paddingVertical:4,alignSelf:"flex-start"},
  sTxt:{fontSize:Typography.xs,fontWeight:Typography.black},
  actions:{flexDirection:"row",gap:Spacing.sm,marginTop:Spacing.md,paddingTop:Spacing.md,borderTopWidth:1,borderTopColor:Colors.neutral100},
  actBtn:{flex:1,backgroundColor:Colors.primary,borderRadius:Radius.sm,paddingVertical:10,alignItems:"center"},
  actTxt:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.white,letterSpacing:0.3},
  actBtnO:{flex:1,borderWidth:1.5,borderColor:Colors.primary,borderRadius:Radius.sm,paddingVertical:10,alignItems:"center"},
  actTxtO:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.primary,letterSpacing:0.3},
})
EOF
echo "✅ DoctorsScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 7: AppointmentScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/AppointmentScreen.tsx << 'EOF'
import { useState,useEffect,useCallback } from "react"
import { View,Text,ScrollView,TouchableOpacity,StyleSheet,ActivityIndicator,RefreshControl,Alert } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors,Typography,Spacing,Radius,statusColor } from "../../constants/theme"
import { getAppointments } from "../api/client"
import { t,getLang } from "../i18n"
const DAYS=["Su","Mo","Tu","We","Th","Fr","Sa"]
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
const MOCK=[
  {id:1,doctor_name:"Dr. Leslie Alexander",specialty:"Headaches",time:"11:30 AM",date:"2026-04-17",status:"scheduled",fee:90},
  {id:2,doctor_name:"Dr. Adam Max",specialty:"Psychology",time:"1:00 PM",date:"2026-04-17",status:"completed",fee:80},
  {id:3,doctor_name:"Dr. Cecily Welsh",specialty:"Dentistry",time:"2:00 PM",date:"2026-04-18",status:"scheduled",fee:120},
  {id:4,doctor_name:"Dr. Jane Cooper",specialty:"Cardiology",time:"10:00 AM",date:"2026-04-19",status:"cancelled",fee:150},
]
export default function AppointmentScreen() {
  const lang=getLang(); const isRTL=lang==="ar"
  const [appts,setAppts]=useState<any[]>(MOCK)
  const [loading,setLoading]=useState(true)
  const [refreshing,setRefreshing]=useState(false)
  const [selDate,setSelDate]=useState(17)
  const [tab,setTab]=useState<"upcoming"|"history">("upcoming")
  async function load(){
    try{ const d=await getAppointments(); if(Array.isArray(d)&&d.length>0) setAppts(d) }catch{}
    setLoading(false)
  }
  useEffect(()=>{load()},[])
  const onRefresh=useCallback(async()=>{setRefreshing(true);await load();setRefreshing(false)},[])
  const calDays=[...Array(3).fill(null),...Array.from({length:30},(_,i)=>i+1)]
  const shown=appts.filter(a=>tab==="upcoming"?a.status==="scheduled":a.status!=="scheduled")
  return (
    <SafeAreaView style={s.safe}>
      <View style={s.hdr}>
        <View style={[s.hdrRow,isRTL&&{flexDirection:"row-reverse"}]}>
          <Text style={[s.title,isRTL&&s.rtl]}>{t("appointments_title")}</Text>
          <View style={s.cntBadge}><Text style={s.cntTxt}>{appts.filter(a=>a.status==="scheduled").length} {t("scheduled_today")}</Text></View>
        </View>
      </View>
      <ScrollView style={s.scroll} showsVerticalScrollIndicator={false}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primary}/>}>
        {/* Calendar */}
        <View style={s.cal}>
          <View style={[s.calHdr,isRTL&&{flexDirection:"row-reverse"}]}>
            <TouchableOpacity style={s.calNav}><Text style={s.calNavT}>‹</Text></TouchableOpacity>
            <Text style={s.calMonth}>April 2026</Text>
            <TouchableOpacity style={s.calNav}><Text style={s.calNavT}>›</Text></TouchableOpacity>
          </View>
          <View style={s.dow}>{DAYS.map(d=><Text key={d} style={s.dowT}>{d}</Text>)}</View>
          <View style={s.grid}>
            {calDays.map((d,i)=>!d?<View key={i} style={s.cell}/>:(
              <TouchableOpacity key={i} style={[s.cell,d===selDate&&s.cellSel,d===17&&d!==selDate&&s.cellToday]} onPress={()=>setSelDate(d)}>
                <Text style={[s.cellT,d===selDate&&s.cellTSel,d===17&&d!==selDate&&s.cellTToday]}>{d}</Text>
                {appts.some(a=>new Date(a.date).getDate()===d)&&<View style={[s.calDot,{backgroundColor:d===selDate?Colors.white:Colors.primary}]}/>}
              </TouchableOpacity>))}
          </View>
        </View>
        {/* Tabs */}
        <View style={s.tabs}>
          {(["upcoming","history"] as const).map(tb=>(
            <TouchableOpacity key={tb} style={[s.tab,tab===tb&&s.tabOn]} onPress={()=>setTab(tb)}>
              <Text style={[s.tabT,tab===tb&&s.tabTOn]}>{tb==="upcoming"?t("appointments"):"History"}</Text>
            </TouchableOpacity>))}
        </View>
        {loading?<ActivityIndicator color={Colors.primary} style={{paddingVertical:Spacing.xl}}/>:
          shown.length===0?<View style={s.empty}><Text style={s.emptyT}>No {tab} appointments</Text></View>:
          shown.map((a,i)=>{
            const sc=statusColor(a.status??"scheduled")
            const dt=new Date(a.date)
            return (
              <TouchableOpacity key={i} style={s.card} activeOpacity={0.85}>
                <View style={[s.cardRow,isRTL&&{flexDirection:"row-reverse"}]}>
                  <View style={s.dateBox}><Text style={s.dateDay}>{dt.getDate()}</Text><Text style={s.dateMon}>{MON[dt.getMonth()]}</Text></View>
                  <View style={[s.info,isRTL&&{alignItems:"flex-end"}]}>
                    <Text style={[s.dr,isRTL&&s.rtl]} numberOfLines={1}>{a.doctor_name}</Text>
                    <Text style={[s.spec,isRTL&&s.rtl]} numberOfLines={1}>{a.specialty}</Text>
                    <View style={[s.meta,isRTL&&{flexDirection:"row-reverse"}]}>
                      <Text style={s.time}>{a.time}</Text>
                      {a.fee&&<Text style={s.fee}>${a.fee}</Text>}
                    </View>
                  </View>
                  <View style={[s.sBadge,{backgroundColor:sc.bg}]}><Text style={[s.sTxt,{color:sc.text}]}>{a.status}</Text></View>
                </View>
                {a.status==="scheduled"&&(
                  <View style={[s.acts,isRTL&&{flexDirection:"row-reverse"}]}>
                    <TouchableOpacity style={s.payBtn} onPress={()=>Alert.alert("Payment","Coming soon")}><Text style={s.payTxt}>{t("pay_now")}</Text></TouchableOpacity>
                    <TouchableOpacity style={s.reBtn}><Text style={s.reTxt}>{t("reschedule")}</Text></TouchableOpacity>
                  </View>)}
              </TouchableOpacity>)})}
        <View style={{height:Spacing.xxl}}/>
      </ScrollView>
    </SafeAreaView>)
}
const s=StyleSheet.create({
  safe:{flex:1,backgroundColor:Colors.neutral50},rtl:{textAlign:"right"},
  hdr:{backgroundColor:Colors.white,paddingHorizontal:Spacing.lg,paddingTop:Spacing.md,paddingBottom:Spacing.md,borderBottomWidth:1,borderBottomColor:Colors.neutral200},
  hdrRow:{flexDirection:"row",justifyContent:"space-between",alignItems:"center"},
  title:{fontSize:Typography.xl,fontWeight:Typography.black,color:Colors.neutral900,letterSpacing:-0.3},
  cntBadge:{backgroundColor:Colors.primary2,borderRadius:Radius.full,paddingHorizontal:12,paddingVertical:5},
  cntTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.primary},
  scroll:{flex:1,paddingHorizontal:Spacing.lg},
  cal:{backgroundColor:Colors.white,borderRadius:Radius.xl,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.md,marginTop:Spacing.md,marginBottom:Spacing.md},
  calHdr:{flexDirection:"row",justifyContent:"space-between",alignItems:"center",marginBottom:Spacing.md},
  calNav:{width:32,height:32,borderRadius:16,backgroundColor:Colors.neutral50,alignItems:"center",justifyContent:"center"},
  calNavT:{fontSize:18,color:Colors.primary,fontWeight:Typography.bold},
  calMonth:{fontSize:Typography.md,fontWeight:Typography.black,color:Colors.neutral900},
  dow:{flexDirection:"row",marginBottom:Spacing.sm},
  dowT:{flex:1,textAlign:"center",fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.neutral400,letterSpacing:0.3},
  grid:{flexDirection:"row",flexWrap:"wrap"},
  cell:{width:"14.28%",aspectRatio:1,alignItems:"center",justifyContent:"center",borderRadius:8,marginBottom:2},
  cellSel:{backgroundColor:Colors.primary},
  cellToday:{borderWidth:2,borderColor:Colors.primary},
  cellT:{fontSize:Typography.sm,fontWeight:Typography.bold,color:Colors.neutral700},
  cellTSel:{color:Colors.white},
  cellTToday:{color:Colors.primary},
  calDot:{width:4,height:4,borderRadius:2,marginTop:1},
  tabs:{flexDirection:"row",backgroundColor:Colors.white,borderRadius:Radius.md,padding:4,marginBottom:Spacing.md,borderWidth:1,borderColor:Colors.neutral200},
  tab:{flex:1,paddingVertical:9,alignItems:"center",borderRadius:10},
  tabOn:{backgroundColor:Colors.primary2},
  tabT:{fontSize:Typography.sm,fontWeight:Typography.bold,color:Colors.neutral500},
  tabTOn:{color:Colors.primary},
  card:{backgroundColor:Colors.white,borderRadius:Radius.lg,borderWidth:1,borderColor:Colors.neutral200,padding:Spacing.md,marginBottom:Spacing.sm},
  cardRow:{flexDirection:"row",alignItems:"flex-start",gap:Spacing.sm},
  dateBox:{backgroundColor:Colors.primary2,borderRadius:10,padding:Spacing.sm,alignItems:"center",minWidth:50},
  dateDay:{fontSize:20,fontWeight:Typography.black,color:Colors.primary,lineHeight:22},
  dateMon:{fontSize:9,fontWeight:Typography.black,color:Colors.primary,letterSpacing:0.5},
  info:{flex:1,minWidth:0},
  dr:{fontSize:Typography.base,fontWeight:Typography.black,color:Colors.neutral900},
  spec:{fontSize:Typography.xs,fontWeight:"600",color:Colors.primary,marginTop:1},
  meta:{flexDirection:"row",alignItems:"center",gap:8,marginTop:4},
  time:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral500},
  fee:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.neutral900},
  sBadge:{borderRadius:Radius.full,paddingHorizontal:10,paddingVertical:4},
  sTxt:{fontSize:Typography.xs,fontWeight:Typography.black,textTransform:"capitalize"},
  acts:{flexDirection:"row",gap:Spacing.sm,marginTop:Spacing.md,paddingTop:Spacing.md,borderTopWidth:1,borderTopColor:Colors.neutral100},
  payBtn:{flex:1,backgroundColor:Colors.primary,borderRadius:Radius.sm,paddingVertical:9,alignItems:"center"},
  payTxt:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.white,letterSpacing:0.3},
  reBtn:{flex:1,borderWidth:1.5,borderColor:Colors.neutral300,borderRadius:Radius.sm,paddingVertical:9,alignItems:"center"},
  reTxt:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.neutral700},
  empty:{alignItems:"center",paddingVertical:Spacing.xxxl},
  emptyT:{fontSize:Typography.base,color:Colors.neutral400,fontWeight:"600"},
})
EOF
echo "✅ AppointmentScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 8: ChatbotScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/ChatbotScreen.tsx << 'EOF'
import { useState,useRef,useCallback } from "react"
import { View,Text,ScrollView,TouchableOpacity,StyleSheet,TextInput,KeyboardAvoidingView,Platform,ActivityIndicator } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors,Typography,Spacing,Radius } from "../../constants/theme"
import { t,getLang } from "../i18n"
import { API_URL } from "../api/client"
import AsyncStorage from "@react-native-async-storage/async-storage"
type Msg={role:"user"|"assistant";text:string;time:string}
const SQ=["q1","q2","q3","q4"]
export default function ChatbotScreen() {
  const lang=getLang(); const isRTL=lang==="ar"
  const [msgs,setMsgs]=useState<Msg[]>([{role:"assistant",text:lang==="ar"?"مرحباً! أنا CareBot، مساعدك الطبي الذكي. كيف يمكنني مساعدتك اليوم؟":lang==="fr"?"Bonjour! Je suis CareBot. Comment puis-je vous aider?":"Hello! I'm CareBot, your AI medical assistant. How can I help you today?",time:now()}])
  const [input,setInput]=useState("")
  const [loading,setLoading]=useState(false)
  const ref=useRef<ScrollView>(null)
  function now(){const d=new Date();return `${d.getHours()}:${String(d.getMinutes()).padStart(2,"0")}`}
  const send=useCallback(async(text?:string)=>{
    const msg=text??input.trim(); if(!msg||loading) return
    setInput("")
    const um:Msg={role:"user",text:msg,time:now()}
    const nm=[...msgs,um]; setMsgs(nm); setLoading(true)
    setTimeout(()=>ref.current?.scrollToEnd({animated:true}),100)
    try{
      const token=await AsyncStorage.getItem("aiha_token")
      const res=await fetch(`${API_URL}/chatbot/chat`,{method:"POST",headers:{"Content-Type":"application/json",...(token?{Authorization:`Bearer ${token}`}:{})},body:JSON.stringify({message:msg,language:lang,history:nm.slice(-8).map(m=>({role:m.role,content:m.text}))})})
      const data=await res.json()
      setMsgs(p=>[...p,{role:"assistant",text:data.response??data.message??data.reply??"I'm here to help. Could you provide more details?",time:now()}])
    }catch{
      setMsgs(p=>[...p,{role:"assistant",text:lang==="ar"?"أعتذر، حدث خطأ. يرجى المحاولة مرة أخرى.":"I apologize, there was a connection issue. Please try again.",time:now()}])
    }finally{setLoading(false);setTimeout(()=>ref.current?.scrollToEnd({animated:true}),100)}
  },[input,msgs,loading,lang])
  return (
    <SafeAreaView style={s.safe}>
      <View style={s.hdr}>
        <View style={s.botAv}><View style={s.botBub}/><View style={s.botDot}/></View>
        <View style={{flex:1}}>
          <Text style={[s.hdrTitle,isRTL&&s.rtl]}>{t("chatbot_title")}</Text>
          <View style={[s.onRow,isRTL&&{flexDirection:"row-reverse"}]}><View style={s.onDot}/><Text style={s.onTxt}>{t("chatbot_online")}</Text></View>
        </View>
        <TouchableOpacity style={s.clearBtn} onPress={()=>setMsgs([])}><Text style={s.clearTxt}>Clear</Text></TouchableOpacity>
      </View>
      <KeyboardAvoidingView style={{flex:1}} behavior={Platform.OS==="ios"?"padding":undefined}>
        <ScrollView ref={ref} style={s.msgs} showsVerticalScrollIndicator={false} contentContainerStyle={{padding:Spacing.md,gap:Spacing.sm}} onContentSizeChange={()=>ref.current?.scrollToEnd({animated:true})}>
          {msgs.map((m,i)=>(
            <View key={i} style={[s.mWrap,m.role==="user"?s.mWrapU:s.mWrapB]}>
              {m.role==="assistant"&&<View style={s.mAv}><View style={s.mAvBub}/></View>}
              <View style={[s.bubble,m.role==="user"?s.bubU:s.bubB,{maxWidth:"78%"}]}>
                <Text style={[s.bubTxt,m.role==="user"?s.bubTxtU:s.bubTxtB,isRTL&&s.rtl]}>{m.text}</Text>
                <Text style={[s.bubTime,m.role==="user"&&{textAlign:"right"}]}>{m.time}</Text>
              </View>
            </View>))}
          {loading&&(
            <View style={s.mWrapB}>
              <View style={s.mAv}><View style={s.mAvBub}/></View>
              <View style={[s.bubble,s.bubB,{paddingVertical:14,paddingHorizontal:20}]}><ActivityIndicator size="small" color={Colors.primary}/></View>
            </View>)}
        </ScrollView>
        {msgs.length<3&&(
          <View style={s.sqWrap}>
            <Text style={[s.sqLabel,isRTL&&s.rtl]}>{t("suggested")}</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {SQ.map(k=><TouchableOpacity key={k} style={s.sqBtn} onPress={()=>send(t(k))}><Text style={[s.sqTxt,isRTL&&s.rtl]}>{t(k)}</Text></TouchableOpacity>)}
            </ScrollView>
          </View>)}
        <View style={[s.inpRow,isRTL&&{flexDirection:"row-reverse"}]}>
          <TextInput style={[s.inp,isRTL&&s.rtl]} value={input} onChangeText={setInput} placeholder={t("type_here")} placeholderTextColor={Colors.neutral400} multiline maxLength={500} onSubmitEditing={()=>send()} returnKeyType="send"/>
          <TouchableOpacity style={[s.sendBtn,(!input.trim()||loading)&&{backgroundColor:Colors.neutral300}]} onPress={()=>send()} disabled={!input.trim()||loading} activeOpacity={0.85}>
            <View style={{width:0,height:0,borderTopWidth:6,borderBottomWidth:6,borderLeftWidth:9,borderTopColor:"transparent",borderBottomColor:"transparent",borderLeftColor:Colors.white,marginLeft:2}}/>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>)
}
const s=StyleSheet.create({
  safe:{flex:1,backgroundColor:Colors.neutral50},rtl:{textAlign:"right"},
  hdr:{backgroundColor:Colors.primary,paddingHorizontal:Spacing.lg,paddingVertical:Spacing.md,flexDirection:"row",alignItems:"center",gap:Spacing.sm},
  botAv:{width:42,height:42,backgroundColor:"rgba(255,255,255,0.2)",borderRadius:21,alignItems:"center",justifyContent:"center"},
  botBub:{width:26,height:22,backgroundColor:Colors.white,borderRadius:11,borderBottomLeftRadius:3,position:"absolute"},
  botDot:{width:5,height:5,backgroundColor:Colors.primary,borderRadius:3,position:"absolute",top:8,left:8},
  hdrTitle:{fontSize:Typography.md,fontWeight:Typography.black,color:Colors.white},
  onRow:{flexDirection:"row",alignItems:"center",gap:5,marginTop:2},
  onDot:{width:7,height:7,borderRadius:4,backgroundColor:"#4ADE80"},
  onTxt:{fontSize:Typography.xs,color:"rgba(255,255,255,0.8)",fontWeight:"500"},
  clearBtn:{paddingHorizontal:12,paddingVertical:6,backgroundColor:"rgba(255,255,255,0.15)",borderRadius:Radius.sm},
  clearTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.white},
  msgs:{flex:1,backgroundColor:Colors.neutral100},
  mWrap:{flexDirection:"row",alignItems:"flex-end",gap:8},
  mWrapB:{justifyContent:"flex-start"},
  mWrapU:{justifyContent:"flex-end"},
  mAv:{width:28,height:28,borderRadius:14,backgroundColor:Colors.primary2,alignItems:"center",justifyContent:"center",flexShrink:0},
  mAvBub:{width:14,height:12,backgroundColor:Colors.primary,borderRadius:6,borderBottomLeftRadius:2},
  bubble:{borderRadius:18,paddingHorizontal:14,paddingVertical:10},
  bubB:{backgroundColor:Colors.white,borderBottomLeftRadius:4,borderWidth:1,borderColor:Colors.neutral200},
  bubU:{backgroundColor:Colors.primary,borderBottomRightRadius:4},
  bubTxt:{fontSize:Typography.base,lineHeight:20},
  bubTxtB:{color:Colors.neutral900},
  bubTxtU:{color:Colors.white},
  bubTime:{fontSize:9,marginTop:5,color:Colors.neutral400,fontWeight:"500"},
  sqWrap:{backgroundColor:Colors.white,borderTopWidth:1,borderTopColor:Colors.neutral200,paddingVertical:10,paddingHorizontal:Spacing.md},
  sqLabel:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.neutral400,letterSpacing:0.5,marginBottom:8},
  sqBtn:{paddingHorizontal:14,paddingVertical:8,borderRadius:Radius.full,borderWidth:1.5,borderColor:Colors.primary3,backgroundColor:Colors.primary2,marginRight:8},
  sqTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.primary,lineHeight:16},
  inpRow:{backgroundColor:Colors.white,borderTopWidth:1,borderTopColor:Colors.neutral200,paddingHorizontal:Spacing.md,paddingVertical:Spacing.sm,flexDirection:"row",alignItems:"flex-end",gap:Spacing.sm},
  inp:{flex:1,borderWidth:1.5,borderColor:Colors.neutral200,borderRadius:Radius.lg,paddingHorizontal:Spacing.md,paddingVertical:Spacing.sm,fontSize:Typography.base,color:Colors.neutral900,maxHeight:100,fontWeight:"500"},
  sendBtn:{width:44,height:44,backgroundColor:Colors.primary,borderRadius:22,alignItems:"center",justifyContent:"center",flexShrink:0},
})
EOF
echo "✅ ChatbotScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 9: ProfileScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/ProfileScreen.tsx << 'EOF'
import { useState } from "react"
import { View,Text,ScrollView,TouchableOpacity,StyleSheet,Alert,Switch } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors,Typography,Spacing,Radius } from "../../constants/theme"
import { useAuth } from "../context/AuthContext"
import { t,setLang,getLang,LANGS } from "../i18n"
export default function ProfileScreen() {
  const {user,logout}=useAuth()
  const [lang,setLangState]=useState(getLang())
  const [notifs,setNotifs]=useState(true)
  const isRTL=lang==="ar"
  function switchLang(c:string){setLang(c as any);setLangState(c as any)}
  function handleLogout(){
    Alert.alert(t("log_out"),lang==="ar"?"هل أنت متأكد؟":lang==="fr"?"Voulez-vous vous déconnecter?":"Are you sure you want to log out?",
      [{text:lang==="ar"?"إلغاء":lang==="fr"?"Annuler":"Cancel",style:"cancel"},{text:t("log_out"),style:"destructive",onPress:logout}])
  }
  const name=user?.full_name??user?.username??"Robertson"
  const role=user?.role??"Medical Staff"
  const email=user?.email??"user@carebot.ai"
  return (
    <SafeAreaView style={s.safe}>
      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={s.pHdr}>
          <View style={s.av}><Text style={s.avT}>{name.charAt(0).toUpperCase()}</Text></View>
          <Text style={[s.nm,isRTL&&s.rtl]}>{name}</Text>
          <View style={s.roleBadge}><Text style={s.roleTxt}>{role}</Text></View>
          <Text style={[s.email,isRTL&&s.rtl]}>{email}</Text>
          <View style={[s.stats,isRTL&&{flexDirection:"row-reverse"}]}>
            {[{n:"142",l:"Appointments"},{n:"38",l:"Patients"},{n:"4.9",l:"Rating"}].map((it,i)=>(
              <View key={i} style={{flexDirection:"row",alignItems:"center"}}>
                {i>0&&<View style={s.statDiv}/>}
                <View style={s.statItem}><Text style={s.statN}>{it.n}</Text><Text style={[s.statL,isRTL&&s.rtl]}>{it.l}</Text></View>
              </View>))}
          </View>
        </View>
        <View style={s.body}>
          <View style={[s.plan,isRTL&&{flexDirection:"row-reverse"}]}>
            <View style={s.planIco}><View style={{width:18,height:18,borderRadius:9,borderWidth:3,borderColor:Colors.white}}/></View>
            <View style={{flex:1}}>
              <Text style={[s.planTitle,isRTL&&s.rtl]}>{t("enterprise_plan")}</Text>
              <Text style={[s.planSub,isRTL&&s.rtl]}>Full access · AI Hospital Alliance</Text>
            </View>
            <View style={s.proBadge}><Text style={s.proTxt}>PRO</Text></View>
          </View>
          {/* Language */}
          <View style={s.section}>
            <Text style={[s.secTitle,isRTL&&s.rtl]}>Language</Text>
            <View style={[s.langRow,isRTL&&{flexDirection:"row-reverse"}]}>
              {LANGS.map(l=>(
                <TouchableOpacity key={l.code} style={[s.langBtn,lang===l.code&&s.langOn]} onPress={()=>switchLang(l.code)}>
                  <Text style={s.langFlag}>{l.flag}</Text>
                  <Text style={[s.langTxt,lang===l.code&&s.langTxtOn]}>{l.label}</Text>
                </TouchableOpacity>))}
            </View>
          </View>
          {/* Menu */}
          {[{title:t("account"),items:[lang==="ar"?"تعديل الملف الشخصي":lang==="fr"?"Modifier le profil":"Edit Profile",lang==="ar"?"تغيير كلمة المرور":lang==="fr"?"Changer le mot de passe":"Change Password",lang==="ar"?"السجلات الطبية":lang==="fr"?"Dossiers médicaux":"Medical Records"]},{title:t("settings"),items:[t("patient_notification"),lang==="ar"?"الخصوصية":"Privacy",lang==="ar"?"حول التطبيق":"About App"]}].map((sec,si)=>(
            <View key={si} style={s.section}>
              <Text style={[s.secTitle,isRTL&&s.rtl]}>{sec.title}</Text>
              <View style={s.menuCard}>
                {sec.items.map((item,ii)=>(
                  <View key={ii} style={[s.menuItem,ii<sec.items.length-1&&s.menuBorder,isRTL&&{flexDirection:"row-reverse"}]}>
                    <View style={s.menuIco}><View style={{width:16,height:16,borderRadius:4,borderWidth:2,borderColor:Colors.primary}}/></View>
                    <Text style={[s.menuTxt,isRTL&&s.rtl]}>{item}</Text>
                    {si===1&&ii===0
                      ?<Switch value={notifs} onValueChange={setNotifs} trackColor={{false:Colors.neutral300,true:Colors.primary3}} thumbColor={notifs?Colors.primary:Colors.white}/>
                      :<View style={{width:0,height:0,borderTopWidth:5,borderBottomWidth:5,borderLeftWidth:7,borderTopColor:"transparent",borderBottomColor:"transparent",borderLeftColor:Colors.neutral300}}/>}
                  </View>))}
              </View>
            </View>))}
          <TouchableOpacity style={s.logoutBtn} onPress={handleLogout} activeOpacity={0.85}>
            <Text style={s.logoutTxt}>{t("log_out")}</Text>
          </TouchableOpacity>
          <Text style={s.ver}>CareBot v1.0.0 · AI Hospital Alliance</Text>
          <View style={{height:Spacing.xxl}}/>
        </View>
      </ScrollView>
    </SafeAreaView>)
}
const s=StyleSheet.create({
  safe:{flex:1,backgroundColor:Colors.neutral50},rtl:{textAlign:"right"},
  pHdr:{backgroundColor:Colors.primary,paddingTop:Spacing.xl,paddingBottom:Spacing.xxl,paddingHorizontal:Spacing.lg,alignItems:"center"},
  av:{width:80,height:80,borderRadius:40,backgroundColor:"rgba(255,255,255,0.25)",alignItems:"center",justifyContent:"center",marginBottom:Spacing.md,borderWidth:3,borderColor:"rgba(255,255,255,0.4)"},
  avT:{fontSize:Typography.h1,fontWeight:Typography.black,color:Colors.white},
  nm:{fontSize:Typography.xl,fontWeight:Typography.black,color:Colors.white,letterSpacing:-0.3,marginBottom:6},
  roleBadge:{backgroundColor:"rgba(255,255,255,0.2)",borderRadius:Radius.full,paddingHorizontal:14,paddingVertical:4,marginBottom:6},
  roleTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.white,textTransform:"capitalize"},
  email:{fontSize:Typography.sm,color:"rgba(255,255,255,0.7)",fontWeight:"500"},
  stats:{flexDirection:"row",backgroundColor:"rgba(255,255,255,0.15)",borderRadius:Radius.lg,paddingVertical:Spacing.md,paddingHorizontal:Spacing.xl,marginTop:Spacing.lg},
  statDiv:{width:1,backgroundColor:"rgba(255,255,255,0.25)"},
  statItem:{flex:1,alignItems:"center"},
  statN:{fontSize:Typography.xl,fontWeight:Typography.black,color:Colors.white},
  statL:{fontSize:Typography.xs,fontWeight:"600",color:"rgba(255,255,255,0.7)",marginTop:2},
  body:{padding:Spacing.lg},
  plan:{backgroundColor:Colors.primary,borderRadius:Radius.lg,padding:Spacing.md,flexDirection:"row",alignItems:"center",gap:Spacing.sm,marginBottom:Spacing.md},
  planIco:{width:40,height:40,backgroundColor:"rgba(255,255,255,0.2)",borderRadius:20,alignItems:"center",justifyContent:"center"},
  planTitle:{fontSize:Typography.base,fontWeight:Typography.black,color:Colors.white},
  planSub:{fontSize:Typography.xs,color:"rgba(255,255,255,0.75)",marginTop:1},
  proBadge:{backgroundColor:"rgba(255,255,255,0.25)",borderRadius:6,paddingHorizontal:8,paddingVertical:3},
  proTxt:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.white,letterSpacing:1},
  section:{marginBottom:Spacing.lg},
  secTitle:{fontSize:Typography.xs,fontWeight:Typography.black,color:Colors.neutral400,letterSpacing:1,textTransform:"uppercase",marginBottom:Spacing.sm},
  langRow:{flexDirection:"row",gap:8},
  langBtn:{flex:1,backgroundColor:Colors.white,borderRadius:Radius.md,borderWidth:1.5,borderColor:Colors.neutral200,padding:Spacing.sm,alignItems:"center",gap:4},
  langOn:{borderColor:Colors.primary,backgroundColor:Colors.primary2},
  langFlag:{fontSize:20},
  langTxt:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.neutral500},
  langTxtOn:{color:Colors.primary},
  menuCard:{backgroundColor:Colors.white,borderRadius:Radius.lg,borderWidth:1,borderColor:Colors.neutral200,overflow:"hidden"},
  menuItem:{flexDirection:"row",alignItems:"center",paddingHorizontal:Spacing.md,paddingVertical:14,gap:Spacing.md},
  menuBorder:{borderBottomWidth:1,borderBottomColor:Colors.neutral100},
  menuIco:{width:36,height:36,backgroundColor:Colors.primary2,borderRadius:10,alignItems:"center",justifyContent:"center"},
  menuTxt:{flex:1,fontSize:Typography.base,fontWeight:"600",color:Colors.neutral800},
  logoutBtn:{flexDirection:"row",alignItems:"center",justifyContent:"center",gap:Spacing.sm,backgroundColor:Colors.danger1,borderRadius:Radius.lg,borderWidth:1.5,borderColor:"#FECACA",paddingVertical:15,marginBottom:Spacing.md},
  logoutTxt:{fontSize:Typography.md,fontWeight:Typography.black,color:Colors.danger},
  ver:{textAlign:"center",fontSize:Typography.xs,color:Colors.neutral400,fontWeight:"500"},
})
EOF
echo "✅ ProfileScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FILE 10: CallScreen.tsx
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat > src/screens/CallScreen.tsx << 'EOF'
import { useState,useEffect,useRef } from "react"
import { View,Text,TouchableOpacity,StyleSheet } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { Colors,Typography,Spacing,Radius } from "../../constants/theme"
import { t,getLang } from "../i18n"
type P={route?:{params?:{type?:"video"|"voice";doctorName?:string;specialty?:string}};navigation?:any}
export default function CallScreen({route,navigation}:P) {
  const lang=getLang(); const isRTL=lang==="ar"
  const type=route?.params?.type??"video"
  const drName=route?.params?.doctorName??"Dr. Leslie Alexander"
  const spec=route?.params?.specialty??"General Medicine"
  const [muted,setMuted]=useState(false)
  const [camOff,setCamOff]=useState(false)
  const [spk,setSpk]=useState(true)
  const [status,setStatus]=useState<"connecting"|"connected"|"ended">("connecting")
  const [secs,setSecs]=useState(0)
  const tmr=useRef<any>(null)
  useEffect(()=>{
    const t=setTimeout(()=>{setStatus("connected");tmr.current=setInterval(()=>setSecs(s=>s+1),1000)},2000)
    return ()=>{clearTimeout(t);clearInterval(tmr.current)}
  },[])
  function fmt(s:number){return `${String(Math.floor(s/60)).padStart(2,"0")}:${String(s%60).padStart(2,"0")}`}
  function end(){clearInterval(tmr.current);setStatus("ended");setTimeout(()=>navigation?.goBack?.(),800)}
  return (
    <SafeAreaView style={s.safe}>
      <View style={type==="video"?s.vidBg:s.voiceBg}>
        {type==="video"?(
          camOff?<View style={s.camOff}><Text style={{color:Colors.neutral400,fontSize:Typography.base}}>Camera is off</Text></View>:
          <View style={{flex:1,alignItems:"center",justifyContent:"center"}}>
            <View style={s.remAv}><Text style={s.remI}>{drName.charAt(3)}</Text></View>
          </View>):(
          <>
            <View style={s.voiceAv}><Text style={s.voiceI}>{drName.charAt(3)}</Text></View>
            <View style={s.waves}>{[1,2,3,4,5].map(i=><View key={i} style={[s.wave,{height:20+i*8,opacity:0.3+i*0.12}]}/>)}</View>
          </>)}
      </View>
      {/* Top info */}
      <View style={[s.top,isRTL&&{flexDirection:"row-reverse"}]}>
        <View>
          <Text style={[s.drNm,isRTL&&s.rtl]}>{drName}</Text>
          <Text style={[s.drSp,isRTL&&s.rtl]}>{spec}</Text>
        </View>
        <View style={s.statusWrap}>
          {status==="connecting"?<Text style={s.statusTxt}>{t("connecting")}</Text>:
           status==="connected"?<Text style={s.timerTxt}>{fmt(secs)}</Text>:
           <Text style={[s.statusTxt,{color:Colors.danger}]}>Call ended</Text>}
        </View>
      </View>
      {/* PIP for video */}
      {type==="video"&&<View style={s.pip}><View style={s.pipIn}><Text style={{fontSize:10,color:Colors.neutral400}}>You</Text></View></View>}
      {/* Controls */}
      <View style={s.ctrls}>
        <TouchableOpacity style={[s.ctrl,muted&&s.ctrlOn]} onPress={()=>setMuted(!muted)}>
          <View style={s.ctrlIco}><View style={{width:8,height:14,borderRadius:4,borderWidth:2.5,borderColor:muted?Colors.neutral400:Colors.white}}/></View>
          <Text style={[s.ctrlLbl,muted&&{color:Colors.neutral400}]}>{t("mute")}</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[s.ctrl,!spk&&s.ctrlOn]} onPress={()=>setSpk(!spk)}>
          <View style={s.ctrlIco}><View style={{width:10,height:14,backgroundColor:spk?Colors.white:Colors.neutral400,borderRadius:2}}/></View>
          <Text style={[s.ctrlLbl,!spk&&{color:Colors.neutral400}]}>{lang==="ar"?"مكبر":lang==="fr"?"Son":"Speaker"}</Text>
        </TouchableOpacity>
        {type==="video"&&(
          <TouchableOpacity style={[s.ctrl,camOff&&s.ctrlOn]} onPress={()=>setCamOff(!camOff)}>
            <View style={s.ctrlIco}><View style={{width:14,height:10,borderRadius:3,borderWidth:2.5,borderColor:camOff?Colors.neutral400:Colors.white}}/></View>
            <Text style={[s.ctrlLbl,camOff&&{color:Colors.neutral400}]}>{t("camera")}</Text>
          </TouchableOpacity>)}
        <TouchableOpacity style={s.endBtn} onPress={end} activeOpacity={0.85}>
          <View style={s.endIco}><View style={{width:22,height:4,backgroundColor:Colors.white,borderRadius:2}}/></View>
          <Text style={s.endLbl}>{t("end_call")}</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>)
}
const s=StyleSheet.create({
  safe:{flex:1,backgroundColor:Colors.neutral900},rtl:{textAlign:"right"},
  vidBg:{flex:1},voiceBg:{flex:1,backgroundColor:Colors.neutral900,alignItems:"center",justifyContent:"center"},
  camOff:{flex:1,backgroundColor:Colors.neutral800,alignItems:"center",justifyContent:"center"},
  remAv:{width:100,height:100,borderRadius:50,backgroundColor:Colors.primary,alignItems:"center",justifyContent:"center"},
  remI:{fontSize:40,fontWeight:Typography.black,color:Colors.white},
  voiceAv:{width:120,height:120,borderRadius:60,backgroundColor:Colors.primary,alignItems:"center",justifyContent:"center",marginBottom:Spacing.xl},
  voiceI:{fontSize:48,fontWeight:Typography.black,color:Colors.white},
  waves:{flexDirection:"row",alignItems:"flex-end",gap:6},
  wave:{width:6,backgroundColor:Colors.primary,borderRadius:3},
  top:{position:"absolute",top:0,left:0,right:0,flexDirection:"row",justifyContent:"space-between",alignItems:"flex-start",padding:Spacing.lg,paddingTop:Spacing.xxl},
  drNm:{fontSize:Typography.lg,fontWeight:Typography.black,color:Colors.white,letterSpacing:-0.2},
  drSp:{fontSize:Typography.sm,color:"rgba(255,255,255,0.7)",marginTop:2,fontWeight:"500"},
  statusWrap:{backgroundColor:"rgba(0,0,0,0.3)",borderRadius:Radius.full,paddingHorizontal:14,paddingVertical:6},
  statusTxt:{fontSize:Typography.sm,color:"rgba(255,255,255,0.8)",fontWeight:"500"},
  timerTxt:{fontSize:Typography.md,color:Colors.white,fontWeight:Typography.black,letterSpacing:1},
  pip:{position:"absolute",bottom:120,right:16,width:80,height:100,borderRadius:12,overflow:"hidden",borderWidth:2,borderColor:Colors.white},
  pipIn:{flex:1,backgroundColor:Colors.neutral700,alignItems:"center",justifyContent:"center"},
  ctrls:{position:"absolute",bottom:0,left:0,right:0,flexDirection:"row",justifyContent:"space-around",alignItems:"center",paddingHorizontal:Spacing.xl,paddingBottom:40,paddingTop:Spacing.xl,backgroundColor:"rgba(0,0,0,0.6)"},
  ctrl:{alignItems:"center",gap:Spacing.xs,width:60},ctrlOn:{opacity:0.5},
  ctrlIco:{width:52,height:52,borderRadius:26,backgroundColor:"rgba(255,255,255,0.15)",alignItems:"center",justifyContent:"center"},
  ctrlLbl:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.white,textAlign:"center"},
  endBtn:{alignItems:"center",gap:Spacing.xs},
  endIco:{width:60,height:60,borderRadius:30,backgroundColor:Colors.danger,alignItems:"center",justifyContent:"center"},
  endLbl:{fontSize:Typography.xs,fontWeight:Typography.bold,color:Colors.white,textAlign:"center"},
})
EOF
echo "✅ CallScreen.tsx"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅  All 10 files installed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Now run:"
echo "   npx expo start --clear"
echo ""
