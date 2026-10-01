# PahadRakshak — System Architecture Documentation

## Overview

**PahadRakshak** is built on a clean, decoupled client-server architecture designed for high availability, zero-latency emergency decision support, and self-contained execution without reliance on unstable external networks during field deployments or hackathon demonstrations.

---

## High-Level Architecture Diagram

```text
+-----------------------------------------------------------------------+
|                            FRONTEND LAYER                             |
|  - Landing Page (index.html)                                          |
|  - Citizen Incident Reporting Portal (citizen.html)                   |
|  - Authority Command Center & Priority Queue (dashboard.html)          |
|  - Leaflet.js Interactive Disaster Map (map.html)                     |
|  - Chart.js Operational Analytics (analytics.html)                    |
+-----------------------------------------------------------------------+
                                   |
                             HTTP / REST API
                                   v
+-----------------------------------------------------------------------+
|                            BACKEND LAYER                              |
|                          (Python + FastAPI)                           |
|  - API Routers: /auth, /incidents, /dashboard, /map, /demo, etc.      |
|  - Middleware: CORS, Request Validation, Static Asset Server          |
+-----------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
+-----------------------------------+   +-----------------------------------+
|            AI ENGINE              |   |          DATABASE LAYER           |
| - Multi-Factor Risk Engine        |   | - SQLAlchemy ORM                  |
| - Explainable Reason Generator    |   | - SQLite (Zero-config local MVP)  |
| - Geo-Haversine Cluster Detector  |   | - PostgreSQL Ready                |
| - Duplicate Report Detector       |   +-----------------------------------+
| - Safe Image Evidence Analyzer    |
+-----------------------------------+
```

---

## Component Details

### 1. Backend Service (`/backend`)
- **Framework**: FastAPI (Python 3.13) + Uvicorn ASGI server
- **API Standards**: OpenAPI / Swagger compliant (`/docs`)
- **Data Access**: SQLAlchemy ORM with thread-safe session management

### 2. AI Intelligence Engine (`/backend/app/ai`)
- **Multi-Factor Risk Engine**: Calculates a normalized 0–100 score based on 6 weighted environmental & crowd factors:
  $$\text{Risk Score} = \min\left(100, f(\text{Severity}) + f(\text{Rainfall}) + f(\text{History}) + f(\text{Density}) + f(\text{Affected}) + f(\text{Accessibility})\right)$$
- **Geo-Spatial Clustering**: Uses the Haversine formula to identify incident clusters within a 3.5 km radius.
- **Duplicate Detector**: Evaluates spatial distance (< 1.5 km), category matching, and description similarity to flag duplicate reports.
- **Image Evidence Analyzer**: Safe heuristic computer vision evaluation service for uploaded photo evidence.

### 3. Database Layer (`/database`)
- Default SQLite storage file: `pahadrakshak.db`
- Fully schema-compatible with PostgreSQL for cloud deployment.
