# 🏔️ PahadRakshak

> **AI-Powered Disaster Risk Intelligence & Emergency Response Platform**  
> *Developed for TechForge 3.0 Internal Hackathon (School of Science & Technology, Swami Rama Himalayan University) & SIH 2026 Adaptability.*

---

## 📌 Executive Summary

**PahadRakshak** is a competition-ready disaster management MVP designed for high-risk mountain regions like Uttarakhand (landslides, flash floods, cloudbursts, road blockages, stranded pilgrims).

Rather than acting as a static reporting form, PahadRakshak operates an **AI-Assisted Multi-Factor Risk Engine** that synthesizes citizen ground reports, severity levels, rainfall indicators, historical risk zones, and population impact to compute an **Explainable 0–100 Risk Score**, automatically sort a **Smart Emergency Priority Queue**, and orchestrate rapid response team dispatch.

---

## 🎯 Core Product Flow

```text
Citizen Report (Location, Photo, Affected Count, Road Access)
                        │
                        ▼
           Incident Processing & Duplicate Check
                        │
                        ▼
      AI Risk Engine (Multi-Factor Weighting)
                        │
                        ▼
     Explainable Risk Score (e.g., 87/100 CRITICAL)
                        │
                        ▼
   Live Leaflet Map & Geo-Spatial Cluster Detection
                        │
                        ▼
 Authority Command Center (Smart Priority Queue)
                        │
                        ▼
   Response Team Dispatch (SDRF / NDRF / Medical)
                        │
                        ▼
     Status Tracking & Citizen Notification
```

---

## 🚀 Key Features & Differentiators

1. **Explainable AI Risk Engine**: Calculates a 0–100 score and explains *why* (e.g., "Heavy rainfall + 25 affected + Road blocked + 3 historical incidents").
2. **Smart Priority Queue**: Auto-sorts active emergencies so control rooms focus on critical life-threatening situations first.
3. **Geo-Spatial Haversine Incident Clustering**: Detects multiple ground reports within a 3.5 km radius to identify major disaster clusters.
4. **Duplicate Report Detector**: Flags nearby reports to prevent dispatcher overload.
5. **Interactive Live Disaster Map**: Custom color-coded Leaflet.js markers, cluster overlays, and historical hotspots.
6. **Fail-Safe Demo Mode (`⚡ Simulate Emergency`)**: Executes an end-to-end incident lifecycle live in 5 seconds without internet reliance.
7. **SIH 2026 Modular Adaptability**: Centralized metadata in `backend/app/core/config.py` for effortless mapping when official SIH 2026 problem statements release.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic v2
- **Database**: SQLite (Zero-config local dev & offline demo), PostgreSQL ready
- **Frontend**: Responsive SPA, HTML5/CSS3, JavaScript (ES6+), Tailwind CSS, Lucide Icons, Leaflet.js, Chart.js
- **AI & Algorithms**: Multi-factor Risk Engine, Haversine Clustering, Levenshtein/Spatial Duplicate Detection

---

## 📂 Repository Structure

```text
pahadrakshak/
├── backend/
│   ├── app/
│   │   ├── api/          # REST Endpoint Routers (auth, incidents, dashboard, map, etc.)
│   │   ├── core/         # Config & Database connection
│   │   ├── models/       # SQLAlchemy ORM models & Pydantic schemas
│   │   ├── ai/           # Risk Engine, Clustering, Duplicate Detector, Image Analyzer
│   │   └── main.py       # FastAPI Entrypoint
├── frontend/
│   ├── index.html        # Landing Page
│   ├── citizen.html      # Citizen Reporting Portal
│   ├── dashboard.html    # Authority Command Dashboard
│   ├── map.html          # Fullscreen Live Map
│   ├── analytics.html    # Disaster Analytics & Metrics
│   ├── css/custom.css    # Glassmorphism Design System
│   └── js/               # Client helpers (app.js, map.js, demo.js)
├── database/
│   └── seed_data.py      # Seed script (7 Uttarakhand incidents + 5 response teams)
├── docs/
│   ├── architecture.md   # Technical System Architecture
│   ├── sih_mapping.json  # SIH 2026 Adaptability Configuration
│   └── demo_script.md    # 3-Minute Hackathon Jury Pitch Script
├── requirements.txt      # Backend Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Project README
```

---

## 💻 Quick Start & Running Locally

### 1. Prerequisites
- Python 3.10+ (Python 3.13 tested)

### 2. Environment Setup & Dependency Installation
```bash
# Navigate into project directory
cd pahadrakshak

# Create Python Virtual Environment
python -m venv venv

# Activate Virtual Environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Upgrade pip & install dependencies
python -m pip install -r requirements.txt
```

### 3. Seed Database with Demonstration Dataset
```bash
python database/seed_data.py
```

### 4. Start Local Development Server
```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

### 5. Access Application URLs
- **Web Application**: `http://127.0.0.1:8000/app/index.html`
- **Citizen Portal**: `http://127.0.0.1:8000/app/citizen.html`
- **Authority Dashboard**: `http://127.0.0.1:8000/app/dashboard.html`
- **Live Disaster Map**: `http://127.0.0.1:8000/app/map.html`
- **Swagger API Docs**: `http://127.0.0.1:8000/docs`
- **Health Endpoint**: `http://127.0.0.1:8000/api/v1/health`

---

## 📑 Third-Party Components & AI Disclosure

- **Open Source Libraries**: FastAPI, Uvicorn, SQLAlchemy, Pydantic, Leaflet.js, Chart.js, Tailwind CSS, Lucide Icons.
- **AI & Algorithmic Disclosure**: Risk scoring, geo-haversine clustering, and duplicate detection use deterministic, mathematical algorithms built from ground up to guarantee 100% offline demo stability.

---

## 👥 Suggested Team Task Division (6 BCA Members)

- **Member 1 (Product & Pitch Lead)**: Problem definition, demo script, pitch presentation.
- **Member 2 (Frontend / Citizen Portal)**: Incident reporting form, photo upload UI, tracking cards.
- **Member 3 (Backend / REST API)**: FastAPI endpoints, status update routes, auth.
- **Member 4 (Database & Risk Engine)**: SQLAlchemy models, RiskEngine calculations, database seed script.
- **Member 5 (Dashboard & Map)**: Leaflet.js integration, Smart Priority Queue, Chart.js analytics.
- **Member 6 (Testing & Demo Support)**: Fail-safe demo simulation mode, API verification, documentation.
