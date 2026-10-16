import { useEffect, useState } from "react"
import ProfileCard from "./components/ProfileCard"
import ProfileFilters from "./components/ProfileFilters"
import { useProfiles } from "./context/profilesContext"
import type { Profile } from "./types/Profile"
import "./App.css"

export default function App() {
  const { profiles, setProfiles } = useProfiles()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Profile Filters
  const [debouncedSearch, setDebouncedSearch] = useState("")
  const [searchTerm, setSearchTerm] = useState<string>("")
  const [availableOnly, setAvailableOnly] = useState<boolean>(false)

  const onSearchChange = (searchTerm: string) => {
    setSearchTerm(searchTerm)
  }

  const onAvailableOnlyChange = (checked: boolean) => {
    setAvailableOnly(checked)
  }

  const onFilterClear = () => {
    setSearchTerm("")
    setAvailableOnly(false)
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchTerm)
    }, 300) // 300ms delay

    return () => clearTimeout(timer) // Clear timeout if user types again before 300ms
  }, [searchTerm])

  useEffect(() => {
    const controller = new AbortController()

    async function fetchProfiles() {
      setError(null)
      setLoading(true)
      try {
        const params = new URLSearchParams()
        if (debouncedSearch) params.append("search", debouncedSearch)
        if (availableOnly)
          params.append("availableOnly", availableOnly.toString())

        const response = await fetch(`/api/profiles?${params.toString()}`, {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error("Failed to fetch profiles.")
        }

        const data: Profile[] = await response.json()
        setProfiles(data)
      } catch (err) {
        if (err instanceof Error && err.name === "AbortError") {
          return
        }

        setError("We couldn't load profiles. Please try again.")
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      }
    }

    fetchProfiles()

    return () => controller.abort()
  }, [debouncedSearch, availableOnly, setProfiles])

  return (
    <main className="app">
      <header className="app-header">
        <p className="app-eyebrow">YOUR NEIGHBORHOOD, THEIR PLAYGROUND</p>
        <h1>
          Woofr<span>🐾</span>
        </h1>
        <p className="app-subtitle">
          Their new best friend could be just around the corner.
        </p>
      </header>

      <ProfileFilters
        search={searchTerm}
        onSearchChange={onSearchChange}
        availableOnly={availableOnly}
        onAvailableOnlyChange={onAvailableOnlyChange}
        onClear={onFilterClear}
      />

      {error ? (
        <div className="page-state">{error}</div>
      ) : loading ? (
        <div className="page-state">Finding your neighborhood... 🐾</div>
      ) : (
        <section className="profile-grid" aria-label="Neighborhood profiles">
          {profiles.length > 0 ? (
            profiles.map((profile) => (
              <ProfileCard key={profile.id} profile={profile} />
            ))
          ) : (
            <p>No profiles found in your neighborhood yet!</p>
          )}
        </section>
      )}
    </main>
  )
}
