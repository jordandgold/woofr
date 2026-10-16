import type { Profile } from "../types/Profile"

interface ProfileCardProps {
  profile: Profile
}

export default function ProfileCard({ profile }: ProfileCardProps) {
  return (
    <article className="profile-card">
      <img
        className="profile-card__image"
        src={profile.imageUrl}
        alt={`${profile.name} the ${profile.breed}`}
        loading="lazy"
      />
      <div className="profile-card__header">
        <div>
          <h2>{profile.name}</h2>
          <p className="profile-card__subtitle">{profile.breed}</p>
        </div>

        <span
          className={`availability ${
            profile.available ? "availability--available" : ""
          }`}
        >
          {profile.available ? "Ready to play" : "Taking a nap"}
        </span>
      </div>

      <div className="profile-card__details">
        <span>
          {profile.age} {profile.age === 1 ? "year" : "years"} old
        </span>
        <span>{profile.distanceMiles.toFixed(1)} mi away</span>
        <span>⚡ {profile.energyLevel} energy</span>
      </div>

      <p className="profile-card__bio">{profile.bio}</p>

      <button
        className="profile-card__button"
        type="button"
        onClick={() => alert(`Woof! You liked ${profile.name}!`)}
      >
        Say hello 🐾
      </button>
    </article>
  )
}
