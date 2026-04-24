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
