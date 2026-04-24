import { registerRootComponent } from "expo"
import { NavigationContainer } from "@react-navigation/native"
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs"
import { createStackNavigator } from "@react-navigation/stack"
import { StatusBar } from "expo-status-bar"
import { Text } from "react-native"
import { GestureHandlerRootView } from "react-native-gesture-handler"
import { AuthProvider, useAuth } from "./src/context/AuthContext"
import SplashScreen from "./src/screens/SplashScreen"
import LoginScreen from "./src/screens/LoginScreen"
import HomeScreen from "./src/screens/HomeScreen"
import DoctorsScreen from "./src/screens/DoctorsScreen"
import AppointmentScreen from "./src/screens/AppointmentScreen"
import ChatbotScreen from "./src/screens/ChatbotScreen"
import ProfileScreen from "./src/screens/ProfileScreen"

const Tab = createBottomTabNavigator()
const Stack = createStackNavigator()

function TabIcon({ name, focused }: { name: string; focused: boolean }) {
  const icons: Record<string, string> = { Home:"🏠", Doctors:"👨‍⚕️", Appointments:"📅", Chat:"🤖", Profile:"👤" }
  return <Text style={{ fontSize:22, opacity:focused?1:0.4 }}>{icons[name]}</Text>
}

function MainTabs() {
  return (
    <Tab.Navigator screenOptions={({ route }) => ({
      tabBarIcon: ({ focused }) => <TabIcon name={route.name} focused={focused} />,
      tabBarStyle: { backgroundColor:"#12122a", borderTopColor:"#1e1e3a", height:65, paddingBottom:8 },
      tabBarActiveTintColor:"#4f46e5", tabBarInactiveTintColor:"#64748b",
      tabBarLabelStyle: { fontSize:10, fontWeight:"600" },
      headerShown: false,
    })}>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Doctors" component={DoctorsScreen} />
      <Tab.Screen name="Appointments" component={AppointmentScreen} />
      <Tab.Screen name="Chat" component={ChatbotScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  )
}

function RootNav() {
  const { token, splash } = useAuth()
  if (splash) return <SplashScreen />
  return (
    <Stack.Navigator screenOptions={{ headerShown:false }}>
      {token ? <Stack.Screen name="Main" component={MainTabs} />
              : <Stack.Screen name="Login" component={LoginScreen} />}
    </Stack.Navigator>
  )
}

function App() {
  return (
    <GestureHandlerRootView style={{ flex:1 }}>
      <AuthProvider>
        <NavigationContainer>
          <StatusBar style="light" backgroundColor="#0a0a1a" />
          <RootNav />
        </NavigationContainer>
      </AuthProvider>
    </GestureHandlerRootView>
  )
}

registerRootComponent(App)
export default App
