from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.schemas import DBIncident, DBHistoricalIncident, IncidentStatusEnum
from backend.app.ai.clustering import ClusterDetector

router = APIRouter(prefix="/map", tags=["Disaster Map"])

@router.get("/incidents")
def get_map_incidents(db: Session = Depends(get_db)):
    incidents = db.query(DBIncident).filter(DBIncident.status != IncidentStatusEnum.RESOLVED).all()

    markers = []
    inc_dicts = []

    for inc in incidents:
        type_str = inc.type.value if hasattr(inc.type, 'value') else inc.type
        risk_str = inc.risk_level.value if hasattr(inc.risk_level, 'value') else inc.risk_level
        status_str = inc.status.value if hasattr(inc.status, 'value') else inc.status

        markers.append({
            "id": inc.id,
            "incident_code": inc.incident_code,
            "type": type_str,
            "description": inc.description,
            "latitude": inc.latitude,
            "longitude": inc.longitude,
            "address": inc.address,
            "district": inc.district,
            "risk_score": inc.risk_score,
            "risk_level": risk_str,
            "severity": inc.severity,
            "affected_people": inc.affected_people,
            "road_blocked": inc.road_blocked,
            "status": status_str,
            "photo_url": inc.photo_url,
            "reports_count": inc.reports_count or 1,
            "reasons": inc.risk_reasons.split("\n") if inc.risk_reasons else [],
            "created_at": inc.created_at
        })

        inc_dicts.append({
            "id": inc.id,
            "incident_code": inc.incident_code,
            "type": type_str,
            "latitude": inc.latitude,
            "longitude": inc.longitude,
            "district": inc.district,
            "risk_score": inc.risk_score,
            "affected_people": inc.affected_people
        })

    # Geo-spatial Cluster Detection
    clusters = ClusterDetector.detect_clusters(inc_dicts, radius_km=3.5)

    # Historical Hotspots
    historical = db.query(DBHistoricalIncident).all()
    hotspots = [
        {
            "id": h.id,
            "name": h.location_name,
            "district": h.district,
            "type": h.incident_type,
            "latitude": h.latitude,
            "longitude": h.longitude,
            "weight": h.risk_weight
        }
        for h in historical
    ]

    return {
        "markers": markers,
        "clusters": clusters,
        "historical_hotspots": hotspots
    }
