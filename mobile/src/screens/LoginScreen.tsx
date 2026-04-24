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
