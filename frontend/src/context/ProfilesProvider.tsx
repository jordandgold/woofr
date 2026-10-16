import { useCallback, useMemo, useState, type ReactNode } from "react"
import type { Profile } from "../types/Profile"
import { ProfilesContext } from "./profilesContext"

export default function ProfilesProvider({ children }: { children: ReactNode }) {
  const [profiles, setProfiles] = useState<Profile[]>([])

  const updateProfile = useCallback(
    (id: string, changes: Partial<Profile>) => {
      setProfiles((prev) =>
        prev.map((p) => (p.id === id ? { ...p, ...changes } : p))
      )
    },
    []
  )

  const value = useMemo(
    () => ({ profiles, setProfiles, updateProfile }),
    [profiles, updateProfile]
  )

  return (
    <ProfilesContext.Provider value={value}>{children}</ProfilesContext.Provider>
  )
}
