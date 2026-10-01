from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.core.database import get_db
from backend.app.models.schemas import DBIncident, DBResponseTeam, RiskLevelEnum, IncidentStatusEnum

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    incidents = db.query(DBIncident).all()

    active_incidents = [i for i in incidents if i.status != IncidentStatusEnum.RESOLVED]
    critical_count = sum(1 for i in active_incidents if i.risk_level == RiskLevelEnum.CRITICAL)
    high_count = sum(1 for i in active_incidents if i.risk_level == RiskLevelEnum.HIGH)
    resolved_count = sum(1 for i in incidents if i.status == IncidentStatusEnum.RESOLVED)
    total_affected = sum(i.affected_people for i in active_incidents)

    teams = db.query(DBResponseTeam).all()
    teams_deployed = sum(1 for t in teams if t.availability_status == "DEPLOYED")

    return {
        "total_active": len(active_incidents),
        "critical_count": critical_count,
        "high_count": high_count,
        "resolved_count": resolved_count,
        "total_affected_people": total_affected,
        "teams_deployed": teams_deployed,
        "avg_response_minutes": 18.5
    }

@router.get("/priority-queue")
def get_priority_queue(db: Session = Depends(get_db)):
    """
    Returns live incidents sorted strictly by AI Risk Score descending.
    Powers the Smart Priority Queue in the Authority Dashboard.
    """
    active_incidents = (
        db.query(DBIncident)
        .filter(DBIncident.status != IncidentStatusEnum.RESOLVED)
        .order_by(DBIncident.risk_score.desc())
        .all()
    )

    result = []
    for inc in active_incidents:
        reasons_list = inc.risk_reasons.split("\n") if inc.risk_reasons else []
        result.append({
            "id": inc.id,
            "incident_code": inc.incident_code,
            "type": inc.type.value if hasattr(inc.type, 'value') else inc.type,
            "risk_score": inc.risk_score,
            "risk_level": inc.risk_level.value if hasattr(inc.risk_level, 'value') else inc.risk_level,
            "severity": inc.severity,
            "address": inc.address,
            "district": inc.district,
            "affected_people": inc.affected_people,
            "road_blocked": inc.road_blocked,
            "status": inc.status.value if hasattr(inc.status, 'value') else inc.status,
            "top_reason": reasons_list[0] if reasons_list else "High priority emergency alert.",
            "created_at": inc.created_at
        })

    return result
