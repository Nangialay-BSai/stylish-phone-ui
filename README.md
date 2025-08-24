## Safar — Afghanistan Ride-Hailing Platform (Monorepo)

This repo contains the backend services and infrastructure to run a minimal Safar stack locally.

### Quick start (Docker)

1. Install Docker and Docker Compose.
2. Copy `.env.example` to `.env` and adjust values.
3. Start services:
   - `docker compose up --build`

Services:
- Postgres + PostGIS on port 5432
- Redis on port 6379
- Backend FastAPI on port 8000 (http://localhost:8000/docs)

### Local dev (without Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### Environment variables

Create `.env` at the repo root or configure your environment:

```
ENV=dev
APP_NAME=Safar Backend
DATABASE_URL=postgresql+psycopg://safar:safar@localhost:5432/safar
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=dev-secret-change
```

### Status

- [x] Repo skeleton and Docker Compose
- [ ] OTP auth
- [ ] Rides quote and pricing
- [ ] WebSocket channels
# Stylish Pink Phone UI 🌸📱

A stylish, responsive phone user interface built with HTML, CSS, and JavaScript.  
Includes a live clock, smooth animations, and interactive app modals for a realistic mobile experience.

## ✨ Features
- **Live clock** with real-time updates
- **Interactive modals** for app-like behavior
- **Responsive design** (works on mobile & desktop)
- **Smooth transitions** and animations
- **Custom color scheme** (soft pink theme)

## 📂 Project Structure
```
📁 assets/     # Images, icons, and other assets
📄 index.html  # Main HTML file
📄 style.css   # Stylesheet
📄 script.js   # JavaScript for interactivity
```

## 🚀 Live Demo
[View on GitHub Pages](https://YOUR_USERNAME.github.io/stylish-phone-ui/)

## 🛠️ Technologies Used
- HTML5
- CSS3
- JavaScript (Vanilla)

## 📜 License
This project is licensed under the MIT License — feel free to use and modify it.
