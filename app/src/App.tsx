import { useEffect, useMemo, useState, type CSSProperties } from "react"
import AddFlooferModal from "./components/AddFlooferModal"
import ProfileCard from "./components/ProfileCard"
import ProfileCardSkeleton from "./components/ProfileCardSkeleton"
import ProfileFilters from "./components/ProfileFilters"
import { useProfiles } from "./context/profilesContext"
import type { Profile, SortOption } from "./types/Profile"
import "./App.css"

export default function App() {
  const { profiles, setProfiles } = useProfiles()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Profile Filters
  const [debouncedSearch, setDebouncedSearch] = useState("")
  const [searchTerm, setSearchTerm] = useState<string>("")
  const [availableOnly, setAvailableOnly] = useState<boolean>(false)
  const [favoritesOnly, setFavoritesOnly] = useState<boolean>(false)
  const [sort, setSort] = useState<SortOption>("newest")

  const onSearchChange = (searchTerm: string) => {
    setSearchTerm(searchTerm)
  }

  const onAvailableOnlyChange = (checked: boolean) => {
    setAvailableOnly(checked)
  }

  // Favorites are filtered here (not on the server) so un-favoriting a card
  // removes it from the favorites view immediately.
  const visibleProfiles = useMemo(
    () =>
      profiles
        .filter((p) => !favoritesOnly || p.favorited)
        .sort((a, b) =>
          sort === "nearest"
            ? a.distanceMiles - b.distanceMiles
            : Date.parse(b.created_at) - Date.parse(a.created_at)
        ),
    [profiles, favoritesOnly, sort]
  )

  // Add Floofer
  const [addModalOpen, setAddModalOpen] = useState(false)

  const onFilterClear = () => {
    setSearchTerm("")
    setAvailableOnly(false)
    setFavoritesOnly(false)
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
        <div className="app-header__brand">
          <h1>
            Woofr<span>🐾</span>
          </h1>
          <p className="app-subtitle">
            Their new best friend could be just around the corner.
          </p>
        </div>
        <button
          className="app-header__add"
          type="button"
          onClick={() => setAddModalOpen(true)}
        >
          + Add Floofer
        </button>
      </header>

      <div className="app-layout">
        <aside className="app-sidebar">
          <ProfileFilters
            search={searchTerm}
            onSearchChange={onSearchChange}
            availableOnly={availableOnly}
            onAvailableOnlyChange={onAvailableOnlyChange}
            favoritesOnly={favoritesOnly}
            onFavoritesOnlyChange={setFavoritesOnly}
            sort={sort}
            onSortChange={setSort}
            onClear={onFilterClear}
          />
        </aside>

        <div className="app-content">
          {error ? (
            <div className="page-state">{error}</div>
          ) : loading ? (
            <section
              className="profile-grid"
              aria-label="Neighborhood profiles"
              aria-busy="true"
            >
              <p className="visually-hidden" role="status">
                Finding your neighborhood...
              </p>
              {Array.from({ length: 6 }, (_, i) => (
                <ProfileCardSkeleton key={i} />
              ))}
            </section>
          ) : (
            <section className="profile-grid" aria-label="Neighborhood profiles">
              {visibleProfiles.length > 0 ? (
                visibleProfiles.map((profile, index) => (
                  <div
                    key={profile.id}
                    className="profile-grid__item"
                    // Stagger the entrance, capped so long lists don't drag on.
                    style={{ "--index": Math.min(index, 12) } as CSSProperties}
                  >
                    <ProfileCard profile={profile} />
                  </div>
                ))
              ) : (
                <p>
                  {favoritesOnly
                    ? "No favorites yet. Tap a heart to add one!"
                    : "No profiles found in your neighborhood yet!"}
                </p>
              )}
            </section>
          )}
        </div>
      </div>

      <AddFlooferModal
        open={addModalOpen}
        onClose={() => setAddModalOpen(false)}
      />
    </main>
  )
}
