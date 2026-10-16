export interface Profile {
  id: string
  name: string
  breed: string
  age: number
  distanceMiles: number
  available: boolean
  energyLevel: "low" | "medium" | "high"
  bio: string
  imageUrl: string
  favorited: boolean
  created_at: string
}

export type SortOption = "newest" | "nearest"

export type NewProfile = Omit<Profile, "id" | "favorited" | "imageUrl" | "created_at"> & {
  photo: File | null
}
