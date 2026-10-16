import HeartIcon from "./HeartIcon"
import type { SortOption } from "../types/Profile"

interface ProfileFiltersProps {
  search: string
  onSearchChange: (value: string) => void
  availableOnly: boolean
  onAvailableOnlyChange: (value: boolean) => void
  favoritesOnly: boolean
  onFavoritesOnlyChange: (value: boolean) => void
  sort: SortOption
  onSortChange: (value: SortOption) => void
  onClear: () => void
}

export default function ProfileFilters({
  search,
  onSearchChange,
  availableOnly,
  onAvailableOnlyChange,
  favoritesOnly,
  onFavoritesOnlyChange,
  sort,
  onSortChange,
  onClear,
}: ProfileFiltersProps) {
  return (
    <section className="profile-filters" aria-label="Filter profiles">
      <label className="profile-filters__search">
        <span>Search profiles</span>
        <input
          type="search"
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Search by name or breed..."
        />
      </label>

      <label className="profile-filters__sort">
        <span>Sort by</span>
        <select
          value={sort}
          onChange={(event) => onSortChange(event.target.value as SortOption)}
        >
          <option value="newest">Newest</option>
          <option value="nearest">Nearest</option>
        </select>
      </label>

      <label className="profile-filters__availability">
        <input
          type="checkbox"
          checked={availableOnly}
          onChange={(event) => onAvailableOnlyChange(event.target.checked)}
        />
        <span>Ready to play only</span>
      </label>

      <div className="profile-filters__actions">
        <button
          className={`profile-filters__favorites ${
            favoritesOnly ? "profile-filters__favorites--active" : ""
          }`}
          type="button"
          aria-label="Show favorites only"
          aria-pressed={favoritesOnly}
          title="Favorites"
          onClick={() => onFavoritesOnlyChange(!favoritesOnly)}
        >
          <HeartIcon />
        </button>

        <button
          className="profile-filters__clear"
          type="button"
          onClick={onClear}
        >
          Clear filters
        </button>
      </div>
    </section>
  )
}
