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
}
