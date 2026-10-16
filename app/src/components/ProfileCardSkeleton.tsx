export default function ProfileCardSkeleton() {
  return (
    <div className="profile-card profile-card--skeleton" aria-hidden="true">
      <div className="skeleton skeleton--image" />
      <div className="skeleton skeleton--title" />
      <div className="skeleton skeleton--subtitle" />
      <div className="skeleton-row">
        <div className="skeleton skeleton--chip" />
        <div className="skeleton skeleton--chip" />
      </div>
      <div className="skeleton skeleton--line" />
      <div className="skeleton skeleton--line skeleton--line-short" />
      <div className="skeleton skeleton--button" />
    </div>
  )
}
