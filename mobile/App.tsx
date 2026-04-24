import { registerRootComponent } from "expo"
import { NavigationContainer } from "@react-navigation/native"
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs"
import { createStackNavigator } from "@react-navigation/stack"
import { StatusBar } from "expo-status-bar"
import { View, Text } from "react-native"
import { GestureHandlerRootView } from "react-native-gesture-handler"
import { AuthProvider, useAuth } from "./src/context/AuthContext"
import { Colors } from "./constants/theme"
import SplashScreen         from "./src/screens/SplashScreen"
import LoginScreen          from "./src/screens/LoginScreen"
import HomeScreen           from "./src/screens/HomeScreen"
import MedicalRecordsScreen from "./src/screens/MedicalRecordsScreen"
import AIDoctorScreen       from "./src/screens/AIDoctorScreen"
import AppointmentScreen    from "./src/screens/AppointmentScreen"
import PharmacyScreen       from "./src/screens/PharmacyScreen"
import ProfileScreen        from "./src/screens/ProfileScreen"

const Tab = createBottomTabNavigator()
const Stack = createStackNavigator()

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarStyle: {
          backgroundColor: "#111111",
          borderTopWidth: 0,
          height: 60,
          paddingBottom: 8,
          paddingTop: 8,
        },
        tabBarActiveTintColor: "#FFFFFF",
        tabBarInactiveTintColor: "rgba(255,255,255,0.4)",
        tabBarLabelStyle: { fontSize: 10, fontWeight: "700" },
        tabBarIcon: ({ focused, color }) => {
          const size = 22
          return (
            <View style={{ width: size, height: size, alignItems: "center", justifyContent: "center" }}>
              <View style={{ width: 18, height: 18, borderRadius: 4, borderWidth: 2, borderColor: color, alignItems: "center", justifyContent: "center" }}>
                <Text style={{ fontSize: 10, color: color, fontWeight: "900" }}>
                  {route.name === "Home" ? "H" :
                   route.name === "Records" ? "R" :
                   route.name === "AI" ? "AI" :
                   route.name === "Appts" ? "A" :
                   route.name === "Pharmacy" ? "Rx" : "P"}
                </Text>
              </View>
            </View>
          )
        },
      })}
    >
      <Tab.Screen name="Home"     component={HomeScreen}           options={{ tabBarLabel: "Home" }} />
      <Tab.Screen name="Records"  component={MedicalRecordsScreen} options={{ tabBarLabel: "Records" }} />
      <Tab.Screen name="AI"       component={AIDoctorScreen}       options={{ tabBarLabel: "AI Doctor" }} />
      <Tab.Screen name="Appts"    component={AppointmentScreen}    options={{ tabBarLabel: "Appts" }} />
      <Tab.Screen name="Pharmacy" component={PharmacyScreen}       options={{ tabBarLabel: "Pharmacy" }} />
      <Tab.Screen name="Profile"  component={ProfileScreen}        options={{ tabBarLabel: "Profile" }} />
    </Tab.Navigator>
  )
}

function RootNav() {
  const { token, splash } = useAuth()
  if (splash) return <SplashScreen />
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {token
        ? <Stack.Screen name="Main" component={MainTabs} />
        : <Stack.Screen name="Login" component={LoginScreen} />
      }
    </Stack.Navigator>
  )
}

function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <AuthProvider>
        <NavigationContainer>
          <StatusBar style="dark" backgroundColor="#ffffff" />
          <RootNav />
        </NavigationContainer>
      </AuthProvider>
    </GestureHandlerRootView>
  )
}

registerRootComponent(App)
export default App
