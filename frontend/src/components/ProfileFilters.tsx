interface ProfileFiltersProps {
  search: string
  onSearchChange: (value: string) => void
  availableOnly: boolean
  onAvailableOnlyChange: (value: boolean) => void
  onClear: () => void
}

export default function ProfileFilters({
  search,
  onSearchChange,
  availableOnly,
  onAvailableOnlyChange,
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

      <label className="profile-filters__availability">
        <input
          type="checkbox"
          checked={availableOnly}
          onChange={(event) => onAvailableOnlyChange(event.target.checked)}
        />
        <span>Ready to play only</span>
      </label>

      <button
        className="profile-filters__clear"
        type="button"
        onClick={onClear}
      >
        Clear filters
      </button>
    </section>
  )
}
