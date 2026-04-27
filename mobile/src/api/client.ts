import axios from "axios"
import AsyncStorage from "@react-native-async-storage/async-storage"

export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? "https://ai-hospital-alliance-production.up.railway.app"

const client = axios.create({ baseURL: API_URL, timeout: 30000 })

client.interceptors.request.use(async (config) => {
  try {
    const token = await AsyncStorage.getItem("aiha_token")
    if (token) {
      config.headers = config.headers || {}
      config.headers["Authorization"] = `Bearer ${token}`
    }
  } catch {}
  return config
})

export async function login(username: string, password: string) {
  const res = await client.post("/auth/login", { username, password })
  const token = res.data.access_token
  const user = res.data.user
  await AsyncStorage.setItem("aiha_token", token)
  await AsyncStorage.setItem("aiha_user", JSON.stringify(user))
  client.defaults.headers.common["Authorization"] = `Bearer ${token}`
  return { access_token: token, user }
}

export async function getDoctors()      { try { return (await client.get("/doctors")).data || [] } catch { return [] } }
export async function getAppointments() { try { return (await client.get("/appointments")).data || [] } catch { return [] } }
export async function getAlerts()       { try { return (await client.get("/alerts")).data || [] } catch { return [] } }
export async function getPatients()     { try { return (await client.get("/patients")).data.data || [] } catch { return [] } }

export default client

export async function claudeChat(message: string, mode: string = "triage", language: string = "en", history: any[] = []) {
  try {
    const res = await client.post("/groq/chat", {
      message,
      mode,
      language,
      history: history.map((m: any) => ({ role: m.role, content: m.content || m.text })),
    })
    return res.data
  } catch (e: any) {
    throw new Error(e?.response?.data?.detail || "Connection error")
  }
}
