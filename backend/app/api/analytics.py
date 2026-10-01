from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.core.database import get_db
from backend.app.models.schemas import DBIncident, DBResponseTeam, DBRiskAssessment

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    incidents = db.query(DBIncident).all()

    category_counts = {}
    district_counts = {}
    risk_distribution = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}

    for inc in incidents:
        type_str = inc.type.value if hasattr(inc.type, 'value') else inc.type
        risk_str = inc.risk_level.value if hasattr(inc.risk_level, 'value') else inc.risk_level

        category_counts[type_str] = category_counts.get(type_str, 0) + 1
        district_counts[inc.district] = district_counts.get(inc.district, 0) + 1
        if risk_str in risk_distribution:
            risk_distribution[risk_str] += 1

    return {
        "total_incidents_logged": len(incidents),
        "by_category": category_counts,
        "by_district": district_counts,
        "risk_distribution": risk_distribution,
        "response_metrics": {
            "avg_verification_minutes": 2.4,
            "avg_team_dispatch_minutes": 5.1,
            "resolution_rate_percent": 82.5
        }
    }
