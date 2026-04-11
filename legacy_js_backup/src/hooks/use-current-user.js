import { getUser } from "@/lib/auth-storage";
export function useCurrentUser() {
    return getUser();
}
