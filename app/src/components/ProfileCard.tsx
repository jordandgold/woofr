import { useProfiles } from "../context/profilesContext"
import type { Profile } from "../types/Profile"

interface ProfileCardProps {
  profile: Profile
}

export default function ProfileCard({ profile }: ProfileCardProps) {
  const { updateProfile } = useProfiles()

  const onFavorite = async () => {
    const favorited = !profile.favorited

    try {
      const response = await fetch(`/api/favorites/${profile.id}`, {
        method: favorited ? "PUT" : "DELETE",
      })
      if (!response.ok) throw new Error("Failed to update favorite.")

      updateProfile(profile.id, { favorited })
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <article className="profile-card">
      <div className="profile-card__media">
        <img
          className="profile-card__image"
          src={profile.imageUrl}
          alt={`${profile.name} the ${profile.breed}`}
          loading="lazy"
        />

        <button
          className={`profile-card__favorite ${
            profile.favorited ? "profile-card__favorite--active" : ""
          }`}
          type="button"
          aria-label={`Favorite ${profile.name}`}
          aria-pressed={profile.favorited}
          onClick={() => onFavorite()}
        >
          <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
          </svg>
        </button>
      </div>
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
