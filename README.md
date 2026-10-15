# Woofr 🐾

A neighborhood discovery app built with React, TypeScript, and FastAPI. Users can browse nearby profiles and explore potential matches.

This project serves as a full-stack engineering practice environment, with a focus on frontend development, API integration, and building interactive user experiences.

## Tech Stack

**Frontend**

- React
- TypeScript
- Vite
- CSS

**Backend**

- Python
- FastAPI
- Pydantic

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
cd grindr-interview-prep
```

If you already have the project locally, navigate directly to its root directory.

### 2. Start the backend

Open a terminal and navigate to the backend directory:

```bash
cd backend
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

Keep this terminal running.

### 3. Start the frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
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
grindr-interview-prep/
├── README.md
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── types/
    │   ├── App.tsx
    │   ├── App.css
    │   ├── index.css
    │   └── main.tsx
    ├── package.json
    └── vite.config.ts
```

## Development Notes

- The frontend runs on port `5173`.
- The backend runs on port `8000`.
- Vite proxies `/api` requests to the backend during development.
- The backend currently serves sample profile data.
- React components and TypeScript interfaces are organized to encourage reusable, maintainable code.

## Future Improvements

- Add profile search and availability filters.
- Add loading, error, and empty states.
- Implement backend filtering and query parameters.
- Add automated frontend and backend tests.
- Improve accessibility and responsive behavior.
