# PahadRakshak — 3-Minute Hackathon Demo Script (TechForge 3.0)

## Overview
This pitch is designed to captivate judges in **the first 30 seconds** by showing a live working workflow from citizen incident report to AI risk scoring, map placement, priority queue ranking, authority dispatch, and resolution.

---

## ⏱️ Minute 0:00 – 0:30 | Problem & Hook
- **Speaker**: *"Respected Judges, in high-altitude mountain terrain like Uttarakhand, landslides, cloudbursts, and flash floods occur without warning. Traditional disaster portals are static report forms where reports sit in queues without real-time prioritization.*
- **Solution**: *"Presenting **PahadRakshak** — an AI-powered disaster risk intelligence and emergency response platform that combines citizen ground reports, rainfall telemetry, and historical vulnerability to score, prioritize, and dispatch help in real time."*

---

## ⏱️ Minute 0:30 – 1:30 | Live Citizen Incident Submission
1. Navigate to **Citizen Portal** (`/app/citizen.html`).
2. Select **Landslide** at *NH-07 Helang Stretch, Chamoli*, set Severity to **CRITICAL**, affected count to **25**, check **Road Blocked**.
3. Upload sample photo (`sample_landslide_1.jpg`) and click **🚀 Submit Incident Report**.
4. Point out the instant result:
   - **AI Risk Score**: `87/100 (CRITICAL RISK)`
   - **Explainable Reasons**: *"Heavy precipitation signal, 25 affected individuals, confirmed road blockage, historical slope instability."*

---

## ⏱️ Minute 1:30 – 2:30 | Authority Control Room & Live Map
1. Switch to **Authority Dashboard** (`/app/dashboard.html`).
2. Show the **Smart Priority Queue**:
   - The newly submitted incident automatically jumps to the **top (#1 spot)** because of its 87/100 risk score!
3. Open **Live Disaster Map** (`/app/map.html`):
   - Show the red critical pulsing marker over Chamoli and the **Spatial Cluster Circle Overlay** linking reports in the area.
4. On the Dashboard, click **Assign Response Team**:
   - Select **SDRF Chamoli Battalion Alpha**.
   - Show the **Suggested Route**: *"Distance: 4.2km | Est. Travel Time: 8.4 mins."*
   - Click **Deploy Team**.

---

## ⏱️ Minute 2:30 – 3:00 | Live Simulation Mode & Impact
1. Click the **`⚡ Simulate Emergency`** button in the header.
2. Demonstrate how the system dynamically generates a new emergency, calculates risk, updates counters, and sends notifications live in 5 seconds without internet reliance!
3. **Closing**: *"PahadRakshak transforms chaotic citizen reports into actionable, explainable emergency intelligence. It's working live, production-ready, and adaptable for SIH 2026."*
