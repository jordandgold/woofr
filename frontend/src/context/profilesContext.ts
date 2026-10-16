import { createContext, useContext } from "react"
import type { Profile } from "../types/Profile"

export interface ProfilesContextValue {
  profiles: Profile[]
  setProfiles: (profiles: Profile[]) => void
  updateProfile: (id: string, changes: Partial<Profile>) => void
}

export const ProfilesContext = createContext<ProfilesContextValue | null>(null)

export function useProfiles() {
  const context = useContext(ProfilesContext)

  if (!context) {
    throw new Error("useProfiles must be used within a ProfilesProvider")
  }

  return context
}
