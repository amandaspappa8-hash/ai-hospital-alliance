import { createContext, useContext, useState, useEffect, ReactNode } from "react"
import AsyncStorage from "@react-native-async-storage/async-storage"
type AuthCtx = { token: string|null; user: any; splash: boolean; login: (t:string,u:any)=>void; logout: ()=>void }
const AuthContext = createContext<AuthCtx>({ token:null, user:null, splash:true, login:()=>{}, logout:()=>{} })
export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string|null>(null)
  const [user, setUser] = useState<any>(null)
  const [splash, setSplash] = useState(true)
  useEffect(() => {
    setTimeout(async () => {
      try {
        const t = await AsyncStorage.getItem("aiha_token")
        if (t) { setToken(t); const u = await AsyncStorage.getItem("aiha_user"); if (u) setUser(JSON.parse(u)) }
      } catch {}
      setSplash(false)
    }, 2000)
  }, [])
  function login(t: string, u: any) { setToken(t); setUser(u); AsyncStorage.setItem("aiha_token", t); AsyncStorage.setItem("aiha_user", JSON.stringify(u)) }
  function logout() { setToken(null); setUser(null); AsyncStorage.removeItem("aiha_token"); AsyncStorage.removeItem("aiha_user") }
  return <AuthContext.Provider value={{ token, user, splash, login, logout }}>{children}</AuthContext.Provider>
}
export const useAuth = () => useContext(AuthContext)
