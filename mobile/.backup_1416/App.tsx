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
