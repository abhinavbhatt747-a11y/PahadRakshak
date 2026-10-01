# PahadRakshak — Hackathon Pitch Deck & Jury Presentation Script

**Event**: TechForge 3.0 Internal Hackathon (School of Science & Technology, SRHU)  
**Nomination Focus**: Smart India Hackathon (SIH) 2026 Adaptation  
**Project**: PahadRakshak — AI-Powered Disaster Risk Intelligence & Emergency Response Platform  

---

## 🎨 SLIDE 1: Title & Hook (The Identity)

### Slide Header:
# 🏔️ PahadRakshak
### Subtitle:
### AI-Powered Disaster Risk Intelligence & Emergency Response Platform

- **Presented By**: Team PahadRakshak (SST, Swami Rama Himalayan University)
- **Target Domain**: Disaster Management, Mountain Resilience & Smart Emergency Response
- **Tagline**: *"Transforming Chaotic Citizen Reports into Actionable, Prioritized Emergency Intelligence across Uttarakhand."*

#### 🎙️ Speaker Notes (First 30 Seconds Hook):
> *"Respected Judges and teammates, in high-altitude mountain states like Uttarakhand, landslides, flash floods, and cloudbursts occur without warning. Traditional reporting portals are static — when a crisis strikes, control rooms are flooded with hundreds of unprioritized calls and don't know which life-threatening situation needs help first.  
> Presenting **PahadRakshak** — an AI-powered disaster intelligence platform that ingests citizen reports, social media posts, and environmental data to score risks, prioritize emergencies, and orchestrate rapid SDRF team response."*

---

## ⚠️ SLIDE 2: The Ground Reality (The Problem)

### Slide Header:
## 💥 Critical Challenges in Hilly Regions (Uttarakhand)

1. **Mountain Terrain Vulnerability**: Narrow highways (NH-07 Badrinath route, Kedarnath corridor) are easily blocked by landslides, trapping tourists, pilgrims, and ambulances.
2. **Control Room Overload**: During cloudbursts, hundreds of citizens call simultaneously. Control rooms lack automated risk ranking.
3. **Information Silos**: Social media posts (X/Twitter videos) go unnoticed by official dispatchers.
4. **Static CRUD Portals**: Existing college projects build basic form portals that just save data rows into a table without risk intelligence or priority queues.

#### 🎙️ Speaker Notes:
> *"The fundamental flaw in current systems is that they are passive databases. They don't analyze risk, they don't detect duplicate reports, and they don't tell officers where lives are in immediate danger."*

---

## 💡 SLIDE 3: The Vision & Solution (PahadRakshak)

### Slide Header:
## 🛡️ PahadRakshak: A Closed-Loop Emergency Orchestration Ecosystem

- **For Citizens**: Fast PWA Mobile App & Web Portal for geo-tagged reporting with photo evidence and live status tracking.
- **For AI Engine**: Multi-factor 0–100 risk scoring with Explainable AI reasoning, Haversine spatial clustering, and social media mining.
- **For District Authorities (DDMA/SDRF/NDRF)**: Command Dashboard with Smart Priority Queue, Live Disaster Map, and Automated Team Dispatch with travel time estimation.

#### 🎙️ Speaker Notes:
> *"PahadRakshak bridges citizens on the ground directly with SDRF, NDRF, BRO, and District Emergency Operation Control Rooms through one unified, intelligent ecosystem."*

---

## 🔄 SLIDE 4: Closed-Loop Emergency Workflow

### Slide Header:
## ⚙️ The Core Product Loop

```text
[Multi-Source Ingestion]  ➔  [AI Risk Engine]  ➔  [Smart Priority Queue]  ➔  [Live Disaster Map]  ➔  [Team Dispatch]  ➔  [Resolution & Update]
• Citizen Mobile App        • 0-100 Score         • Auto-Ranked Top          • Custom Markers       • SDRF/NDRF Unit       • Notification
• Social Media (X/Twitter)  • Explainable AI      • Critical First           • Cluster Circles      • Route Time           • Status Pill
• Rainfall Telemetry        • 6 Weighted Factors                             • Hotspot Overlays     • Distance (km)
```

#### 🎙️ Speaker Notes:
> *"Every emergency moves through a 6-step closed-loop lifecycle — from ingestion to AI scoring, priority ranking, map visualization, response team deployment, and final resolution."*

---

## 🧠 SLIDE 5: Innovation Pillar 1 — Multi-Factor Risk Engine & Explainable AI

### Slide Header:
## 🤖 Multi-Factor Risk Scoring Engine (0 – 100)

Calculated across 6 weighted environmental & crowd factors:
$$\text{Risk Score} = f(\text{Severity}) + f(\text{Rainfall}) + f(\text{History}) + f(\text{Density}) + f(\text{Affected}) + f(\text{Accessibility})$$

- **Explainable AI Output**:
  > **Score: 87/100 (CRITICAL RISK)**  
  > *Reasons: Heavy rainfall detected (65mm) + 25 affected individuals + Confirmed road blockage + 3 historical slope failure events nearby.*

#### 🎙️ Speaker Notes:
> *"Our AI is not a black box. It calculates a transparent score and explains the exact mathematical reasons to control room officers so they can trust the decision."*

---

## 🔥 SLIDE 6: Innovation Pillar 2 — Smart Auto-Ranked Priority Queue

### Slide Header:
## 🚨 Smart Priority Queue for District Control Rooms

- **Automatic Sorting**: Incidents are auto-ranked by AI Risk Score descending.
- **Critical First**: #1 spot is occupied by the most life-threatening situation (e.g. Landslide blocking ambulance route with 45 stranded).
- **One-Click Dispatch**: Officers can click `Dispatch Team` directly from the priority card.

#### 🎙️ Speaker Notes:
> *"Control room officers no longer waste precious minutes searching through lists. The Smart Priority Queue auto-promotes critical emergencies to the top instantly."*

---

## 📱 SLIDE 7: Innovation Pillar 3 — Social Media Disaster Mining

### Slide Header:
## 🌐 Automated Social Media Mining Crawler

- **Scans Public Platforms**: Scans X (Twitter), Facebook, Instagram for disaster keywords (`#Landslide`, `#Chamoli`, `#Cloudburst`).
- **NLP Location & Category Extraction**: Extracts location (*NH-07 Helang Stretch*) and disaster type (*Landslide*).
- **Control Room Badge**: Tags incident as `[SOURCE: SOCIAL MEDIA X/TWITTER]` with author handle (`@GarhwalTraveler`).
- **Inspector Panel**: Officers can click `🔍 Inspect` to view original tweet, author profile, and direct link.

#### 🎙️ Speaker Notes:
> *"During disasters, citizens post videos on Twitter before calling official lines. PahadRakshak mines social media posts, extracts locations, evaluates AI risk, and places them directly onto the Control Room Map."*

---

## 🗺️ SLIDE 8: Innovation Pillar 4 — Spatial Clustering & Live Disaster Map

### Slide Header:
## 📍 Geo-Haversine Clustering & Interactive Map

- **Geo-Haversine Clustering**: Links reports within a 3.5 km radius to identify major disaster cluster zones.
- **Duplicate Report Detector**: Prevents dispatcher overload by linking duplicate nearby reports.
- **Interactive Dark Map**: Leaflet.js map with color-coded pulsing risk markers:
  - 🔴 **CRITICAL** (76–100)
  - 🟠 **HIGH** (51–75)
  - 🟡 **MODERATE** (26–50)
  - 🟢 **LOW** (0–25)

#### 🎙️ Speaker Notes:
> *"Our spatial clustering algorithm connects individual ground reports into a bigger geographic picture, showing control rooms exactly where major disaster clusters are forming."*

---

## ⚡ SLIDE 9: Innovation Pillar 5 — Fail-Safe Demo Mode & Mobile PWA App

### Slide Header:
## 📱 PWA Mobile App & Fail-Safe Demo Mode

- **Progressive Web App (PWA)**: Installable on Android & iOS home screens with fullscreen app navigation.
- **Fail-Safe Demo Mode (`⚡ Simulate Emergency`)**:
  - One-click header button that executes an end-to-end incident lifecycle in 5 seconds.
  - Zero internet dependence — works 100% offline during jury presentations.

#### 🎙️ Speaker Notes:
> *"PahadRakshak runs as a native Mobile App for citizens on smartphones, and includes a built-in live simulation engine so you can see a complete emergency lifecycle right before your eyes."*

---

## 🛠️ SLIDE 10: Technical Architecture & Technology Stack

### Slide Header:
## 🏗️ Production-Grade Technology Stack

- **Backend**: Python 3.13 + FastAPI + Uvicorn ASGI Server
- **Database**: SQLite (`pahadrakshak.db`) via SQLAlchemy ORM (100% PostgreSQL Ready)
- **Frontend**: HTML5, Tailwind CSS, Glassmorphic Design System, Leaflet.js, Chart.js
- **Testing**: Automated `pytest` suite passing 100% test coverage.

#### 🎙️ Speaker Notes:
> *"We built PahadRakshak using industry-standard Python FastAPI and SQLAlchemy ORM. It's clean, modular, tested, and ready for PostgreSQL cloud deployment."*

---

## 🌍 SLIDE 11: Multi-District Coverage & Real-World Impact

### Slide Header:
## 🏔️ 13-District Uttarakhand Coverage

- **Garhwal Region**: Chamoli, Rudraprayag, Uttarkashi, Dehradun, Tehri, Pauri, Haridwar.
- **Kumaon Region**: Nainital, Almora, Pithoragarh, Bageshwar, Champawat, Udham Singh Nagar.
- **Multi-Agency Support**: Integrates SDRF, NDRF, Garhwal Medical Corps, BRO, and Uttarakhand Police.

#### 🎙️ Speaker Notes:
> *"PahadRakshak covers all 13 districts of Uttarakhand. It serves as a single source of truth for all regional disaster management authorities."*

---

## 🏆 SLIDE 12: Summary & Jury Q&A

### Slide Header:
## 🏆 Why PahadRakshak Belongs in First Place

1. **Working End-to-End MVP** (Not just a slides presentation or wireframe).
2. **Explainable AI & Smart Priority Queue** (Solves real control room bottleneck).
3. **Multi-Source Social Media Mining** (Ingests X/Twitter alerts automatically).
4. **Fail-Safe & Production Ready** (Runs seamlessly offline & online).
5. **SIH 2026 Adaptability** (Modular architecture ready for official problem statements).

### 💬 Thank You! Questions & Live Demonstration
- **Live App URL**: `http://127.0.0.1:8000/app/index.html`
- **Mobile App**: `http://192.168.31.175:8000/app/citizen.html`
