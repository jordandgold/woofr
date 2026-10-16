import HeartIcon from "./HeartIcon"
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
          <HeartIcon />
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
