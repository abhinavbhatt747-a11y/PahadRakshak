import os
import sys
from datetime import datetime, timedelta

# Ensure parent directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.core.database import SessionLocal, Base, engine
from backend.app.models.schemas import (
    DBUser, DBIncident, DBIncidentReport, DBRiskAssessment,
    DBResponseTeam, DBAssignment, DBNotification, DBIncidentTimeline,
    DBHistoricalIncident, RoleEnum, IncidentTypeEnum, RiskLevelEnum,
    IncidentStatusEnum, TeamTypeEnum
)
from backend.app.ai.risk_engine import RiskEngine

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    print("[*] Seeding PahadRakshak Database with Uttarakhand Demonstration Dataset...")

    # 1. Users
    users = [
        DBUser(
            username="authority",
            email="controlroom@srhu.edu.in",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # password: "password123"
            role=RoleEnum.AUTHORITY,
            phone="+91-9876543210",
            district="Chamoli"
        ),
        DBUser(
            username="citizen1",
            email="citizen@gmail.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            role=RoleEnum.CITIZEN,
            phone="+91-9876543211",
            district="Dehradun"
        )
    ]
    db.add_all(users)

    # 2. Response Teams
    teams = [
        DBResponseTeam(
            name="SDRF Chamoli Battalion Alpha",
            team_type=TeamTypeEnum.RESCUE,
            base_location="Gopeshwar, Chamoli",
            current_lat=30.4124,
            current_lng=79.3245,
            availability_status="AVAILABLE",
            contact_number="+91-1372-252100"
        ),
        DBResponseTeam(
            name="Garhwal Medical Rapid Unit 4",
            team_type=TeamTypeEnum.MEDICAL,
            base_location="AIIMS Rishikesh / District Hosp Chamoli",
            current_lat=30.4089,
            current_lng=79.3299,
            availability_status="AVAILABLE",
            contact_number="+91-1372-252102"
        ),
        DBResponseTeam(
            name="BRO Heavy Road Clearance Team 2",
            team_type=TeamTypeEnum.ROAD_MAINTENANCE,
            base_location="Pipalkoti Heavy Eq Depot",
            current_lat=30.4312,
            current_lng=79.4188,
            availability_status="DEPLOYED",
            contact_number="+91-1372-252105"
        ),
        DBResponseTeam(
            name="NDRF Flash Flood Response Taskforce 8",
            team_type=TeamTypeEnum.DISASTER_RESPONSE,
            base_location="Rishikesh Camp",
            current_lat=30.0869,
            current_lng=78.2676,
            availability_status="AVAILABLE",
            contact_number="+91-135-243210"
        ),
        DBResponseTeam(
            name="Uttarakhand Police PCR Patrol 09",
            team_type=TeamTypeEnum.POLICE,
            base_location="Joshimath Police Station",
            current_lat=30.5562,
            current_lng=79.5667,
            availability_status="AVAILABLE",
            contact_number="112"
        )
    ]
    db.add_all(teams)
    db.commit()

    # 3. Historical Incidents (for risk engine lookups)
    historical = [
        DBHistoricalIncident(location_name="Helang Badrinath Highway", district="Chamoli", incident_type="Landslide", latitude=30.521, longitude=79.510, risk_weight=1.4),
        DBHistoricalIncident(location_name="Joshimath Subsidence Zone", district="Chamoli", incident_type="Infrastructure Damage", latitude=30.556, longitude=79.567, risk_weight=1.5),
        DBHistoricalIncident(location_name="Rudraprayag Sangam Road", district="Rudraprayag", incident_type="Flood", latitude=30.285, longitude=78.981, risk_weight=1.3),
        DBHistoricalIncident(location_name="Govindghat Track", district="Chamoli", incident_type="Landslide", latitude=30.622, longitude=79.619, risk_weight=1.2),
        DBHistoricalIncident(location_name="Maldevta Dehradun", district="Dehradun", incident_type="Heavy Rainfall", latitude=30.342, longitude=78.118, risk_weight=1.1)
    ]
    db.add_all(historical)

    # 4. Realistic Demonstration Incidents (Uttarakhand locations)
    sample_incidents_data = [
        {
            "code": "PR-UK-1001",
            "type": IncidentTypeEnum.LANDSLIDE,
            "desc": "[OFFICIAL GOVT BULLETIN - UKSDMA] Massive rockfall and earth slide blocking National Highway 07 near Helang. Vehicles stranded on both sides.",
            "severity": "CRITICAL",
            "lat": 30.5214, "lng": 79.5102,
            "address": "NH-07 Helang Stretch, Chamoli",
            "district": "Chamoli",
            "affected": 45,
            "road_blocked": True,
            "status": IncidentStatusEnum.REPORTED,
            "photo_url": "/static/uploads/sample_landslide_1.jpg",
            "rainfall": 65.0,
            "history_count": 3,
            "source_url": "https://usdma.uk.gov.in/"
        },
        {
            "code": "PR-UK-1002",
            "type": IncidentTypeEnum.FLOOD,
            "desc": "[SOURCE: @GarhwalTraveler via Twitter/X] Alaknanda water level rising dangerously above warning mark near Badrinath main bridge.",
            "severity": "CRITICAL",
            "lat": 30.5580, "lng": 79.5690,
            "address": "Alaknanda Ghat, Joshimath",
            "district": "Chamoli",
            "affected": 80,
            "road_blocked": False,
            "status": IncidentStatusEnum.VERIFIED,
            "photo_url": "/static/uploads/sample_flood_1.jpg",
            "rainfall": 82.0,
            "history_count": 4,
            "source_url": "https://x.com/search?q=Uttarakhand%20disaster%20Joshimath&f=live"
        },
        {
            "code": "PR-UK-1003",
            "type": IncidentTypeEnum.ROAD_BLOCKAGE,
            "desc": "[OFFICIAL GOVT BULLETIN - BRO] Boulders collapsed on Gopeshwar-Mandal road blocking emergency ambulance route.",
            "severity": "HIGH",
            "lat": 30.4200, "lng": 79.3350,
            "address": "Gopeshwar-Mandal Route, Chamoli",
            "district": "Chamoli",
            "affected": 12,
            "road_blocked": True,
            "status": IncidentStatusEnum.TEAM_ASSIGNED,
            "photo_url": "/static/uploads/sample_roadblock.jpg",
            "rainfall": 48.0,
            "history_count": 2,
            "source_url": "https://bro.gov.in/"
        },
        {
            "code": "PR-UK-1004",
            "type": IncidentTypeEnum.STRANDED_PEOPLE,
            "desc": "[SOURCE: Citizen SOS Upload] Group of 15 pilgrims stranded due to sudden stream swell near Govindghat.",
            "severity": "HIGH",
            "lat": 30.6225, "lng": 79.6190,
            "address": "Govindghat Trek Route, Chamoli",
            "district": "Chamoli",
            "affected": 15,
            "road_blocked": True,
            "status": IncidentStatusEnum.IN_PROGRESS,
            "photo_url": "/static/uploads/sample_stranded.jpg",
            "rainfall": 52.0,
            "history_count": 1,
            "source_url": "https://usdma.uk.gov.in/"
        },
        {
            "code": "PR-UK-1005",
            "type": IncidentTypeEnum.HEAVY_RAINFALL,
            "desc": "[OFFICIAL GOVT BULLETIN - IMD DEHRADUN] Continuous cloudburst-like precipitation causing localized waterlogging near Sahastradhara Road.",
            "severity": "MODERATE",
            "lat": 30.3850, "lng": 78.0820,
            "address": "Sahastradhara Road, Dehradun",
            "district": "Dehradun",
            "affected": 8,
            "road_blocked": False,
            "status": IncidentStatusEnum.REPORTED,
            "photo_url": None,
            "rainfall": 55.0,
            "history_count": 1,
            "source_url": "https://mausam.imd.gov.in/dehradun/"
        },
        {
            "code": "PR-UK-1006",
            "type": IncidentTypeEnum.INFRASTRUCTURE_DAMAGE,
            "desc": "[OFFICIAL GOVT BULLETIN - UTTARAKHAND POLICE] Retaining wall cracks widening on Rishikesh-Badrinath bypass road.",
            "severity": "MODERATE",
            "lat": 30.1020, "lng": 78.2980,
            "address": "Bypass Road, Rishikesh",
            "district": "Dehradun",
            "affected": 4,
            "road_blocked": False,
            "status": IncidentStatusEnum.RESOLVED,
            "photo_url": None,
            "rainfall": 20.0,
            "history_count": 1,
            "source_url": "https://uttarakhandpolice.uk.gov.in/"
        },
        {
            "code": "PR-UK-1007",
            "type": IncidentTypeEnum.LANDSLIDE,
            "desc": "Minor mudslide reported near Helang petrol pump. Traffic moving slowly.",
            "severity": "HIGH",
            "lat": 30.5230, "lng": 79.5120,
            "address": "Helang Market Bypass, Chamoli",
            "district": "Chamoli",
            "affected": 10,
            "road_blocked": False,
            "status": IncidentStatusEnum.REPORTED,
            "photo_url": None,
            "rainfall": 60.0,
            "history_count": 3,
            "source_url": "https://usdma.uk.gov.in/"
        }
    ]

    for item in sample_incidents_data:
        score, level, reasons, breakdown = RiskEngine.calculate_risk(
            incident_type=item["type"].value,
            severity=item["severity"],
            affected_people=item["affected"],
            road_blocked=item["road_blocked"],
            reports_count=1,
            rainfall_mm=item["rainfall"],
            historical_incident_count=item["history_count"]
        )

        inc = DBIncident(
            incident_code=item["code"],
            type=item["type"],
            description=item["desc"],
            severity=item["severity"],
            status=item["status"],
            latitude=item["lat"],
            longitude=item["lng"],
            address=item["address"],
            district=item["district"],
            photo_url=item["photo_url"],
            affected_people=item["affected"],
            road_blocked=item["road_blocked"],
            risk_score=score,
            risk_level=level,
            risk_reasons="\n".join(reasons),
            reports_count=1,
            verified_by_authority=(item["status"] != IncidentStatusEnum.REPORTED),
            source_platform="GOVT_BULLETIN" if "[OFFICIAL GOVT BULLETIN" in item["desc"] else "SOCIAL_MEDIA",
            source_author="UKSDMA Control" if "[OFFICIAL GOVT BULLETIN" in item["desc"] else "@GarhwalTraveler",
            source_url=item["source_url"],
            created_at=datetime.utcnow() - timedelta(minutes=15)
        )
        db.add(inc)
        db.flush()

        # Add initial risk assessment entry
        assessment = DBRiskAssessment(
            incident_id=inc.id,
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
        db.add(assessment)

        # Timeline
        t = DBIncidentTimeline(
            incident_id=inc.id,
            status_from="INITIAL",
            status_to=inc.status.value,
            note=f"Incident registered via PahadRakshak AI Risk Score: {score}/100 ({level})",
            action_by="AI Risk Engine"
        )
        db.add(t)

    # Assign team 3 to PR-UK-1003
    inc3 = db.query(DBIncident).filter(DBIncident.incident_code == "PR-UK-1003").first()
    if inc3:
        assign = DBAssignment(
            incident_id=inc3.id,
            response_team_id=3,
            assigned_by="Chamoli District Disaster Control Room",
            notes="Deploy JCB heavy earthmover for road clearance immediately.",
            status="ACTIVE"
        )
        db.add(assign)
        teams[2].availability_status = "DEPLOYED"
        teams[2].active_incident_id = inc3.id

    db.commit()
    print("[+] PahadRakshak Database Seeded Successfully with real working government source URLs!")
    db.close()

if __name__ == "__main__":
    seed_database()
