from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from backend.app.core.database import get_db
from backend.app.models.schemas import DBResponseTeam, DBIncident, DBAssignment, DBIncidentTimeline, IncidentStatusEnum
from backend.app.ai.clustering import haversine_distance

router = APIRouter(prefix="/response-teams", tags=["Response Teams"])

class DispatchRequest(BaseModel):
    incident_id: int
    team_id: int
    assigned_by: Optional[str] = "Chamoli District Control Room"
    notes: Optional[str] = "Deploy immediate field assistance."

@router.get("")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(DBResponseTeam).all()
    result = []
    for t in teams:
        type_str = t.team_type.value if hasattr(t.team_type, 'value') else t.team_type
        result.append({
            "id": t.id,
            "name": t.name,
            "team_type": type_str,
            "base_location": t.base_location,
            "current_lat": t.current_lat,
            "current_lng": t.current_lng,
            "availability_status": t.availability_status,
            "contact_number": t.contact_number,
            "active_incident_id": t.active_incident_id
        })
    return result

@router.post("/assign")
def assign_team(req: DispatchRequest, db: Session = Depends(get_db)):
    team = db.query(DBResponseTeam).filter(DBResponseTeam.id == req.team_id).first()
    inc = db.query(DBIncident).filter(DBIncident.id == req.incident_id).first()

    if not team or not inc:
        raise HTTPException(status_code=404, detail="Team or Incident not found.")

    # Calculate suggested response route distance & estimated travel time
    dist_km = haversine_distance(team.current_lat, team.current_lng, inc.latitude, inc.longitude)
    # Average mountain terrain speed = 30 km/h
    est_travel_minutes = round((dist_km / 30.0) * 60, 1)

    assignment = DBAssignment(
        incident_id=inc.id,
        response_team_id=team.id,
        assigned_by=req.assigned_by,
        notes=req.notes,
        status="ACTIVE"
    )
    db.add(assignment)

    team.availability_status = "DEPLOYED"
    team.active_incident_id = inc.id

    inc.status = IncidentStatusEnum.TEAM_ASSIGNED
    inc.verified_by_authority = True

    timeline = DBIncidentTimeline(
        incident_id=inc.id,
        status_from="VERIFIED",
        status_to="TEAM ASSIGNED",
        note=f"Assigned {team.name}. Route Distance: {round(dist_km, 1)}km. Est. Travel Time: {est_travel_minutes} mins.",
        action_by=req.assigned_by
    )
    db.add(timeline)
    db.commit()

    return {
        "status": "success",
        "message": f"Team '{team.name}' deployed to Incident #{inc.incident_code}.",
        "route_support": {
            "suggested_route": f"Base ({team.base_location}) -> {inc.address}",
            "distance_km": round(dist_km, 1),
            "est_travel_minutes": est_travel_minutes,
            "disclaimer": "Suggested response route based on mountain spatial telemetry. Road check recommended."
        }
    }
