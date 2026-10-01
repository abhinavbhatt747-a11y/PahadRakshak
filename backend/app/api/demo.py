import random
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.schemas import (
    DBIncident, DBRiskAssessment, DBIncidentTimeline, DBNotification,
    DBResponseTeam, DBAssignment, IncidentTypeEnum, RiskLevelEnum, IncidentStatusEnum
)
from backend.app.ai.risk_engine import RiskEngine

router = APIRouter(prefix="/demo", tags=["Demo Simulation"])

DEMO_LOCATIONS = [
    {"address": "Badrinath Highway Bend near Pipalkoti", "district": "Chamoli", "lat": 30.4320, "lng": 79.4210},
    {"address": "Rudraprayag Sangam Road Bypass", "district": "Rudraprayag", "lat": 30.2860, "lng": 78.9820},
    {"address": "Joshimath Auli Cable Car Slope", "district": "Chamoli", "lat": 30.5570, "lng": 79.5680},
    {"address": "Maldevta Bridge Approach Road", "district": "Dehradun", "lat": 30.3450, "lng": 78.1200},
    {"address": "Nainital Lake Mall Road Corner", "district": "Nainital", "lat": 29.3910, "lng": 79.4540}
]

DEMO_TYPES = [
    (IncidentTypeEnum.LANDSLIDE, "CRITICAL", "Major rockfall debris covering 50m of tarmac."),
    (IncidentTypeEnum.FLOOD, "CRITICAL", "Flash flood river overflow threatening low-lying structures."),
    (IncidentTypeEnum.STRANDED_PEOPLE, "HIGH", "Trekker group caught in heavy downpour requiring immediate winch rescue."),
    (IncidentTypeEnum.ROAD_BLOCKAGE, "HIGH", "Fallen pine trees and boulders blocking disaster relief route.")
]

@router.post("/simulate")
def simulate_emergency(db: Session = Depends(get_db)):
    """
    Executes a complete 10-step emergency simulation lifecycle live for judges:
    1. Generates a new realistic Uttarakhand incident report
    2. Calculates multi-factor AI Risk Score
    3. Categorizes Risk Level & Explainable Reasons
    4. Places on Live Disaster Map & Smart Priority Queue
    5. Dispatches Authority Notification
    6. Verifies & Assigns available Response Team
    7. Updates status to IN_PROGRESS
    """

    loc = random.choice(DEMO_LOCATIONS)
    inc_type, severity, desc = random.choice(DEMO_TYPES)
    code = f"PR-SIM-{random.randint(2000, 9999)}"

    # 1 & 2. Compute AI Risk Score
    score, level, reasons, breakdown = RiskEngine.calculate_risk(
        incident_type=inc_type.value,
        severity=severity,
        affected_people=random.randint(10, 40),
        road_blocked=True,
        reports_count=3,
        rainfall_mm=78.5,
        historical_incident_count=3
    )

    db_inc = DBIncident(
        incident_code=code,
        type=inc_type,
        description=f"[SIMULATION DEMO] {desc}",
        severity=severity,
        status=IncidentStatusEnum.REPORTED,
        latitude=loc["lat"],
        longitude=loc["lng"],
        address=loc["address"],
        district=loc["district"],
        photo_url="/static/uploads/sample_landslide_1.jpg",
        affected_people=random.randint(15, 35),
        road_blocked=True,
        risk_score=score,
        risk_level=level,
        risk_reasons="\n".join(reasons),
        reports_count=3,
        verified_by_authority=False,
        created_at=datetime.utcnow()
    )
    db.add(db_inc)
    db.commit()
    db.refresh(db_inc)

    # Risk Assessment
    risk_rec = DBRiskAssessment(
        incident_id=db_inc.id,
        score=score,
        level=level,
        severity_factor=breakdown["severity_factor"],
        rainfall_factor=breakdown["rainfall_factor"],
        history_factor=breakdown["history_factor"],
        density_factor=breakdown["density_factor"],
        vulnerability_factor=10.0,
        affected_factor=breakdown["affected_factor"],
        accessibility_factor=breakdown["accessibility_factor"],
        explanation_text="\n".join(reasons)
    )
    db.add(risk_rec)

    # Timeline Entry 1: Report Submitted
    t1 = DBIncidentTimeline(
        incident_id=db_inc.id,
        status_from="NONE",
        status_to="REPORTED",
        note=f"Emergency Simulated: Citizen report received. AI Risk Score: {score}/100 ({level})",
        action_by="Citizen Portal"
    )
    db.add(t1)

    # Notification
    notif = DBNotification(
        recipient_role="AUTHORITY",
        title=f"ALERT [{level} RISK]: Simulated Emergency #{code}",
        message=f"Simulated incident in {loc['district']} at {loc['address']}. Score: {score}/100.",
        incident_id=db_inc.id
    )
    db.add(notif)

    # Step 6 & 7: Auto-verify & Assign available team for live demo fluidity
    avail_team = db.query(DBResponseTeam).filter(DBResponseTeam.availability_status == "AVAILABLE").first()

    assigned_team_name = "Control Room Standby Unit"
    if avail_team:
        assigned_team_name = avail_team.name
        avail_team.availability_status = "DEPLOYED"
        avail_team.active_incident_id = db_inc.id
        db.add(DBAssignment(
            incident_id=db_inc.id,
            response_team_id=avail_team.id,
            assigned_by="Simulated Emergency Orchestrator",
            notes="Immediate rapid response deployment.",
            status="ACTIVE"
        ))

    db_inc.status = IncidentStatusEnum.TEAM_ASSIGNED
    db_inc.verified_by_authority = True

    t2 = DBIncidentTimeline(
        incident_id=db_inc.id,
        status_from="REPORTED",
        status_to="TEAM ASSIGNED",
        note=f"Control room verified incident and assigned {assigned_team_name}.",
        action_by="Authority Control Room"
    )
    db.add(t2)

    db.commit()

    return {
        "status": "success",
        "message": "Emergency Simulation Triggered Successfully!",
        "simulated_incident": {
            "id": db_inc.id,
            "incident_code": db_inc.incident_code,
            "type": inc_type.value,
            "district": loc["district"],
            "address": loc["address"],
            "risk_score": score,
            "risk_level": level,
            "assigned_team": assigned_team_name,
            "reasons": reasons
        }
    }
