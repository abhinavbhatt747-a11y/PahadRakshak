import random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.core.database import get_db
from backend.app.models.schemas import (
    DBIncident, DBIncidentReport, DBRiskAssessment, DBIncidentTimeline,
    DBNotification, IncidentCreateSchema, IncidentResponseSchema,
    IncidentTypeEnum, RiskLevelEnum, IncidentStatusEnum
)
from backend.app.ai.risk_engine import RiskEngine
from backend.app.ai.duplicate_detector import DuplicateDetector
from backend.app.ai.image_analysis import ImageAnalysisService
from backend.app.ai.resolution_checker import ResolutionCheckerService

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=List[IncidentResponseSchema])
def get_incidents(
    status: Optional[str] = None,
    district: Optional[str] = None,
    risk_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(DBIncident)

    if status:
        query = query.filter(DBIncident.status == status)
    if district:
        query = query.filter(DBIncident.district == district)
    if risk_level:
        query = query.filter(DBIncident.risk_level == risk_level)

    incidents = query.order_by(DBIncident.risk_score.desc(), DBIncident.created_at.desc()).all()
    return incidents

@router.post("/auto-clearance-check", summary="Run automated road clearance and resolution verification")
def trigger_auto_clearance_check(db: Session = Depends(get_db)):
    """
    Executes automated road clearance verification.
    Solves completed road blockages and purges resolved incidents from live map.
    """
    res = ResolutionCheckerService.check_and_resolve_cleared_incidents(db)
    return res

@router.get("/{incident_id}", response_model=IncidentResponseSchema)
def get_incident_by_id(incident_id: int, db: Session = Depends(get_db)):
    inc = db.query(DBIncident).filter(DBIncident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found.")
    return inc

@router.post("")
def create_incident(
    type: str = Form(...),
    description: str = Form(...),
    severity: str = Form("HIGH"),
    latitude: float = Form(...),
    longitude: float = Form(...),
    address: str = Form(...),
    district: str = Form("Chamoli"),
    affected_people: int = Form(1),
    road_blocked: bool = Form(False),
    reporter_name: Optional[str] = Form("Anonymous Citizen"),
    reporter_contact: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    photo_url = None
    image_analysis_res = None

    if file:
        photo_url = f"/static/uploads/{file.filename}"
        image_analysis_res = ImageAnalysisService.analyze_image(file.filename, type)

    # 1. Duplicate Check against existing active incidents
    all_active = [
        {
            "id": inc.id,
            "incident_code": inc.incident_code,
            "type": inc.type.value if hasattr(inc.type, 'value') else inc.type,
            "latitude": inc.latitude,
            "longitude": inc.longitude,
            "address": inc.address,
            "status": inc.status.value if hasattr(inc.status, 'value') else inc.status
        }
        for inc in db.query(DBIncident).filter(DBIncident.status != IncidentStatusEnum.RESOLVED).all()
    ]

    new_inc_dict = {
        "type": type,
        "latitude": latitude,
        "longitude": longitude
    }

    duplicates = DuplicateDetector.find_duplicates(new_inc_dict, all_active)

    # 2. Compute AI Risk Score
    score, level, reasons, breakdown = RiskEngine.calculate_risk(
        incident_type=type,
        severity=severity,
        affected_people=affected_people,
        road_blocked=road_blocked,
        reports_count=1 + (len(duplicates) if duplicates else 0),
        rainfall_mm=62.0 if severity == "CRITICAL" else 35.0,
        historical_incident_count=2
    )

    if image_analysis_res:
        reasons.append(f"AI Visual Evidence: {image_analysis_res['summary']}")

    code = f"PR-UK-{random.randint(1000, 9999)}"

    # Handle type enum mapping safely
    enum_type = IncidentTypeEnum.OTHER
    for e in IncidentTypeEnum:
        if e.value.lower() == type.lower():
            enum_type = e
            break

    db_inc = DBIncident(
        incident_code=code,
        type=enum_type,
        description=description,
        severity=severity.upper(),
        status=IncidentStatusEnum.REPORTED,
        latitude=latitude,
        longitude=longitude,
        address=address,
        district=district,
        photo_url=photo_url,
        affected_people=affected_people,
        road_blocked=road_blocked,
        risk_score=score,
        risk_level=level,
        risk_reasons="\n".join(reasons),
        reports_count=1,
        verified_by_authority=False
    )
    db.add(db_inc)
    db.commit()
    db.refresh(db_inc)

    # Save Risk Assessment Breakdown
    risk_record = DBRiskAssessment(
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
    db.add(risk_record)

    # Add Incident Timeline Entry
    timeline = DBIncidentTimeline(
        incident_id=db_inc.id,
        status_from="NONE",
        status_to="REPORTED",
        note=f"Incident registered. AI Risk Score: {score}/100 ({level})",
        action_by=reporter_name or "Citizen"
    )
    db.add(timeline)

    # Create Notification for Authorities
    notif = DBNotification(
        recipient_role="AUTHORITY",
        title=f"New {level} Risk Incident: {type}",
        message=f"Incident #{code} reported at {address} (Risk Score: {score}/100). Access blocked: {'YES' if road_blocked else 'NO'}.",
        incident_id=db_inc.id
    )
    db.add(notif)
    db.commit()

    return {
        "status": "success",
        "incident_id": db_inc.id,
        "incident_code": db_inc.incident_code,
        "risk_score": score,
        "risk_level": level,
        "risk_reasons": reasons,
        "potential_duplicates": duplicates,
        "image_analysis": image_analysis_res
    }

@router.put("/{incident_id}/status")
def update_incident_status(
    incident_id: int,
    status: str,
    note: Optional[str] = "Status updated by authority",
    action_by: Optional[str] = "Control Room Officer",
    db: Session = Depends(get_db)
):
    inc = db.query(DBIncident).filter(DBIncident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found.")

    old_status = inc.status.value if hasattr(inc.status, 'value') else inc.status
    new_status = status.upper()
    inc.status = new_status

    if new_status in ["VERIFIED", "TEAM ASSIGNED", "IN PROGRESS"]:
        inc.verified_by_authority = True

    if new_status == "RESOLVED":
        inc.road_blocked = False
        note = f"HAZARD RESOLVED: Road cleared and verified safe for traffic. Purged from live map."

    timeline = DBIncidentTimeline(
        incident_id=inc.id,
        status_from=old_status,
        status_to=new_status,
        note=note,
        action_by=action_by
    )
    db.add(timeline)

    # Send Notification to Citizen
    notif = DBNotification(
        recipient_role="CITIZEN",
        title=f"Incident #{inc.incident_code} Update",
        message=f"Your reported incident status changed to {new_status}. Note: {note}",
        incident_id=inc.id
    )
    db.add(notif)

    db.commit()
    return {"message": f"Incident #{inc.incident_code} status updated to {new_status}. Live map updated.", "incident_code": inc.incident_code}
