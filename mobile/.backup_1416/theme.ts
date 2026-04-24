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
