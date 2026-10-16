# Woofr 🐾

A neighborhood discovery app built with React, TypeScript, and FastAPI. Users can browse nearby dog profiles with photos, search and filter them, and favorite the ones they like.

This project serves as a full-stack engineering practice environment, with a focus on frontend development, API integration, and building interactive user experiences.

## Tech Stack

**App (frontend)**

- React
- TypeScript
- Vite
- CSS

**Server (backend)**

- Python
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite

## Prerequisites

Make sure you have the following installed:

- Node.js and npm
- Python 3.11+
- Git (optional)

## Getting Started

### 1. Clone the repository

If you're working from a Git repository:

```bash
git clone <repository-url>
cd woofr
```

If you already have the project locally, navigate directly to its root directory.

### 2. Start the server

Open a terminal and navigate to the server directory:

```bash
cd server
```

Create a virtual environment if you haven't already:

```bash
python3 -m venv .venv
```

Activate the virtual environment on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:

- **API:** http://localhost:8000/api/profiles
- **Interactive API documentation:** http://localhost:8000/docs

On first start the server creates a SQLite database (`server/woofr.db`) and seeds it with the starter profiles. Favorites are saved there, so they persist across restarts. To reset the data, stop the server, delete `woofr.db`, and start it again.

Keep this terminal running.

### 3. Start the app

Open a second terminal and navigate to the app directory:

```bash
cd app
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the application at:

**http://localhost:5173**

Keep this terminal running as well.

## Project Structure

```text
woofr/
├── README.md
├── server/
│   ├── main.py            # App setup: middleware, static files, routers
│   ├── models.py          # Profile model (SQLModel table)
│   ├── db.py              # SQLite engine, session dependency, seeding
│   ├── data.py            # Starter profiles used to seed the database
│   ├── routers/
│   │   ├── profiles.py    # /api/profiles, /api/available-names
│   │   └── favorites.py   # /api/favorites
│   ├── static/dogs/       # Profile photos, served at /api/static/dogs/
│   │   └── uploads/       # User-uploaded photos (git-ignored)
│   ├── requirements.txt
│   └── tests/
└── app/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── context/       # ProfilesContext + useProfiles hook
    │   ├── types/
    │   ├── App.tsx
    │   ├── App.css
    │   ├── index.css
    │   └── main.tsx
    ├── package.json
    └── vite.config.ts
```

## API Endpoints

| Method   | Path                       | Description                                                                 |
| -------- | -------------------------- | --------------------------------------------------------------------------- |
| `GET`    | `/api/profiles`            | List profiles. Optional `search` (name or breed) and `availableOnly=true`.   |
| `POST`   | `/api/profiles`            | Create a profile (multipart form, optional `photo`). Returns 201 with the new profile. |
| `GET`    | `/api/available-names`     | Sorted names of available profiles.                                         |
| `GET`    | `/api/favorites`           | List favorited profiles.                                                    |
| `PUT`    | `/api/favorites/{id}`      | Favorite a profile (204). Safe to repeat; 404 if the id doesn't exist.      |
| `DELETE` | `/api/favorites/{id}`      | Remove a favorite (204); 404 if the id doesn't exist.                       |
| `GET`    | `/api/static/dogs/{name}.jpg` | Profile photo.                                                           |

## Development Notes

- The app (frontend) runs on port `5173`.
- The server (backend) runs on port `8000`.
- Vite proxies `/api` requests to the server during development.
- Profiles are stored in SQLite and seeded from `server/data.py` the first time the server starts.
- Favorites are stored on the profile row and are shared by everyone using the server; there is no user concept yet.
- Changing a model column does not alter an existing database (there are no migrations). Delete `woofr.db` and restart to reseed.
- Uploaded photos are saved to `server/static/dogs/uploads/` (git-ignored). Profiles without a photo use the gray placeholder `server/static/dogs/default.svg`.
- Seed profile photos in `server/static/dogs/` come from the [Dog CEO API](https://dog.ceo/dog-api/) (Stanford Dogs dataset), which is fine for a demo but check licensing before commercial use.
- Profiles are kept in a React context (`app/src/context/`) so a card can update its own record after favoriting.
- React components and TypeScript interfaces are organized to encourage reusable, maintainable code.

## Running Tests

### Server Tests

The server uses **pytest** and FastAPI's `TestClient` to test API endpoints, search functionality, availability filtering, favorites, and error handling.

From the `server/` directory, activate your Python virtual environment:

```bash
cd server
source .venv/bin/activate
```

Run all server tests:

```bash
python -m pytest -v
```

The `-v` flag enables verbose output, displaying the result of each individual test.

To run a specific test file:

```bash
python -m pytest tests/test_profiles.py -v
```

Tests run against the FastAPI application using `TestClient`, so **you do not need to start the server** before running them. Each test gets a fresh in-memory SQLite database seeded with the starter profiles (see `tests/conftest.py`), so tests never touch `woofr.db`.

## Future Improvements

- Per-user favorites (requires users or sessions) and a "favorites only" view.
- Database migrations (e.g. Alembic) in place of deleting `woofr.db`.
- Optimistic updates and an in-flight guard on the favorite button.
- Automated app tests.
- Improve accessibility and responsive behavior.
