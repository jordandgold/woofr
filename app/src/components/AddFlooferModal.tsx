import {
  useEffect,
  useRef,
  useState,
  type DragEvent,
  type FormEvent,
} from "react"
import type { Profile } from "../types/Profile"

interface AddFlooferModalProps {
  open: boolean
  onClose: () => void
}

const MAX_PHOTO_BYTES = 5 * 1024 * 1024

const initialForm = {
  name: "",
  breed: "",
  age: "",
  distanceMiles: "",
  energyLevel: "medium" as Profile["energyLevel"],
  available: true,
  bio: "",
}

function FlooferForm({ onClose }: Pick<AddFlooferModalProps, "onClose">) {
  const [form, setForm] = useState(initialForm)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Photo upload
  const [photo, setPhoto] = useState<{ file: File; url: string } | null>(null)
  const [photoError, setPhotoError] = useState<string | null>(null)
  const [dragging, setDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const photoUrlRef = useRef<string | null>(null)

  // Release the preview URL when the form unmounts.
  useEffect(
    () => () => {
      if (photoUrlRef.current) URL.revokeObjectURL(photoUrlRef.current)
    },
    [],
  )

  const selectPhoto = (file: File | undefined) => {
    if (!file) return

    if (!file.type.startsWith("image/")) {
      setPhotoError("Please choose an image file.")
      return
    }
    if (file.size > MAX_PHOTO_BYTES) {
      setPhotoError("Image must be 5 MB or smaller.")
      return
    }

    if (photoUrlRef.current) URL.revokeObjectURL(photoUrlRef.current)
    const url = URL.createObjectURL(file)
    photoUrlRef.current = url
    setPhoto({ file, url })
    setPhotoError(null)
  }

  const removePhoto = () => {
    if (photoUrlRef.current) URL.revokeObjectURL(photoUrlRef.current)
    photoUrlRef.current = null
    setPhoto(null)
    setPhotoError(null)
    if (fileInputRef.current) fileInputRef.current.value = ""
  }

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setDragging(false)
    selectPhoto(event.dataTransfer.files[0])
  }

  const update = <K extends keyof typeof initialForm>(
    key: K,
    value: (typeof initialForm)[K],
  ) => setForm((prev) => ({ ...prev, [key]: value }))

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    setSubmitting(true)

    try {
      const body = new FormData()
      body.append("name", form.name)
      body.append("breed", form.breed)
      body.append("age", String(form.age))
      body.append("distanceMiles", String(form.distanceMiles))
      body.append("available", String(form.available))
      body.append("energyLevel", form.energyLevel)
      body.append("bio", form.bio)
      if (photo) body.append("photo", photo.file)

      const response = await fetch("/api/profiles", {
        method: "POST",
        body, // no Content-Type header: the browser sets multipart/form-data with the boundary
      })

      if (response.ok) {
        onClose()
      }
    } catch (e) {
      console.error(e)
      setError("We couldn't add this floofer. Please try again.")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="floofer-form" onSubmit={handleSubmit}>
      <h2 id="floofer-modal-title">Add a Floofer 🐶</h2>

      <div className="floofer-form__field">
        <span id="floofer-photo-label">Profile photo</span>

        <div
          className={`photo-dropzone ${
            dragging ? "photo-dropzone--dragging" : ""
          } ${photo ? "photo-dropzone--has-photo" : ""}`}
          role="button"
          tabIndex={0}
          aria-labelledby="floofer-photo-label"
          onClick={() => fileInputRef.current?.click()}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault()
              fileInputRef.current?.click()
            }
          }}
          onDragOver={(event) => {
            event.preventDefault()
            setDragging(true)
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          {photo ? (
            <img
              className="photo-dropzone__preview"
              src={photo.url}
              alt="Selected profile photo preview"
            />
          ) : (
            <div className="photo-dropzone__prompt">
              <span className="photo-dropzone__icon" aria-hidden="true">
                📷
              </span>
              <strong>Drag & drop a photo</strong>
              <span>or click to browse (PNG or JPG, up to 5 MB)</span>
            </div>
          )}
        </div>

        <input
          ref={fileInputRef}
          className="photo-dropzone__input"
          type="file"
          accept="image/*"
          tabIndex={-1}
          onChange={(event) => selectPhoto(event.target.files?.[0])}
        />

        {photo && (
          <button
            type="button"
            className="photo-dropzone__remove"
            onClick={removePhoto}
          >
            Remove photo
          </button>
        )}

        {photoError && (
          <p className="floofer-form__error" role="alert">
            {photoError}
          </p>
        )}
      </div>

      <label className="floofer-form__field">
        <span>Name</span>
        <input
          type="text"
          required
          maxLength={40}
          value={form.name}
          onChange={(e) => update("name", e.target.value)}
        />
      </label>

      <label className="floofer-form__field">
        <span>Breed</span>
        <input
          type="text"
          required
          maxLength={60}
          value={form.breed}
          onChange={(e) => update("breed", e.target.value)}
        />
      </label>

      <div className="floofer-form__row">
        <label className="floofer-form__field">
          <span>Age (years)</span>
          <input
            type="number"
            required
            min={0}
            max={30}
            step={1}
            value={form.age}
            onChange={(e) => update("age", e.target.value)}
          />
        </label>

        <label className="floofer-form__field">
          <span>Distance (miles)</span>
          <input
            type="number"
            required
            min={0}
            step={0.1}
            value={form.distanceMiles}
            onChange={(e) => update("distanceMiles", e.target.value)}
          />
        </label>
      </div>

      <label className="floofer-form__field">
        <span>Energy level</span>
        <select
          value={form.energyLevel}
          onChange={(e) =>
            update("energyLevel", e.target.value as Profile["energyLevel"])
          }
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </label>

      <label className="floofer-form__field">
        <span>Bio</span>
        <textarea
          required
          rows={3}
          maxLength={200}
          value={form.bio}
          onChange={(e) => update("bio", e.target.value)}
        />
      </label>

      <label className="floofer-form__check">
        <input
          type="checkbox"
          checked={form.available}
          onChange={(e) => update("available", e.target.checked)}
        />
        <span>Ready to play</span>
      </label>

      {error && (
        <p className="floofer-form__error" role="alert">
          {error}
        </p>
      )}

      <div className="floofer-form__actions">
        <button
          type="button"
          className="floofer-form__cancel"
          onClick={onClose}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="floofer-form__submit"
          disabled={submitting}
        >
          {submitting ? "Adding..." : "Add Floofer"}
        </button>
      </div>
    </form>
  )
}

export default function AddFlooferModal({
  open,
  onClose,
}: AddFlooferModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    if (open && !dialog.open) {
      dialog.showModal()
    } else if (!open && dialog.open) {
      dialog.close()
    }
  }, [open])

  // A modal <dialog> doesn't stop the page behind it from scrolling.
  useEffect(() => {
    if (!open) return

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = "hidden"

    return () => {
      document.body.style.overflow = previousOverflow
    }
  }, [open])

  return (
    <dialog
      ref={dialogRef}
      className="floofer-modal"
      aria-labelledby="floofer-modal-title"
      onClose={onClose}
      onClick={(event) => {
        // Clicking the backdrop (the dialog element itself) dismisses it.
        if (event.target === event.currentTarget) onClose()
      }}
    >
      {/* Mounted only while open so the form state resets each time. */}
      {open && <FlooferForm onClose={onClose} />}
    </dialog>
  )
}
