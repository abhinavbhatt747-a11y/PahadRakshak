import random
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.schemas import DBIncident, DBRiskAssessment, DBIncidentTimeline, DBNotification, IncidentTypeEnum, IncidentStatusEnum
from backend.app.ai.social_mining import SocialMediaMiningService
from backend.app.ai.risk_engine import RiskEngine

router = APIRouter(prefix="/social", tags=["Social Media Mining"])

class SocialWebhookSchema(BaseModel):
    post_text: str
    platform: str = "X (Twitter)"
    author_handle: str = "@DehradunNewsNow"
    media_url: str = None
    post_url: str = "https://x.com/DehradunNewsNow/status/182399120391"

@router.post("/ingest")
def ingest_social_post(payload: SocialWebhookSchema, db: Session = Depends(get_db)):
    parsed = SocialMediaMiningService.parse_social_post(payload.post_text, payload.platform, payload.media_url)

    if not parsed["is_disaster_alert"]:
        return {"status": "ignored", "reason": "No disaster keywords detected in social post."}

    code = f"PR-SOC-{random.randint(1000, 9999)}"
    
    # Map type safely
    enum_type = IncidentTypeEnum.ACCIDENT
    for e in IncidentTypeEnum:
        if e.value.lower() == parsed["inferred_type"].lower():
            enum_type = e
            break

    score, level, reasons, breakdown = RiskEngine.calculate_risk(
        incident_type=parsed["inferred_type"],
        severity="CRITICAL",
        affected_people=1,
        road_blocked=True,
        reports_count=2,
        rainfall_mm=10.0
    )

    reasons.append(f"Ingested via Social Media Mining ({payload.platform} by {payload.author_handle})")

    # Set exact lat/lng for Graphic Era Dehradun (30.2688, 78.0076) if mentioned
    lat = 30.2688 if "graphic era" in payload.post_text.lower() else 30.3165
    lng = 78.0076 if "graphic era" in payload.post_text.lower() else 78.0322

    db_inc = DBIncident(
        incident_code=code,
        type=enum_type,
        description=f"[SOURCE: {payload.platform} {payload.author_handle}] {payload.post_text}",
        severity="CRITICAL",
        status=IncidentStatusEnum.REPORTED,
        latitude=lat,
        longitude=lng,
        address=parsed["inferred_location"],
        district="Dehradun",
        photo_url=payload.media_url or "/static/uploads/sample_roadblock.jpg",
        affected_people=1,
        road_blocked=True,
        risk_score=score,
        risk_level=level,
        risk_reasons="\n".join(reasons),
        reports_count=1,
        verified_by_authority=False,
        source_platform=payload.platform,
        source_author=payload.author_handle,
        source_url=payload.post_url or "https://x.com/search?q=Graphic%20Era%20Dehradun"
    )
    db.add(db_inc)
    db.commit()

    db.add(DBIncidentTimeline(
        incident_id=db_inc.id,
        status_from="NONE",
        status_to="REPORTED",
        note=f"Accident report ingested from {payload.platform} post by {payload.author_handle}.",
        action_by="Social Mining Crawler"
    ))
    db.add(DBNotification(
        recipient_role="AUTHORITY",
        title=f"CRITICAL ACCIDENT ALERT [{payload.platform}]: Dehradun",
        message=f"Fatal accident alert near Graphic Era Dehradun from {payload.author_handle}.",
        incident_id=db_inc.id
    ))
    db.commit()

    return {
        "status": "success",
        "message": "Accident report ingested into PahadRakshak Risk Pipeline!",
        "parsed": parsed,
        "incident_code": code,
        "risk_score": score,
        "risk_level": level,
        "source_author": payload.author_handle
    }
