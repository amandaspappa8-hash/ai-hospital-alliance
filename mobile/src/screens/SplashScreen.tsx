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
