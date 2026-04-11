export function hasRole(userRole: string | undefined, allowed: string[]) {
  if (!userRole) return false;
  return allowed.includes(userRole);
}
