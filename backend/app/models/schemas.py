import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import Optional, List
from backend.app.core.database import Base

class RoleEnum(str, enum.Enum):
    CITIZEN = "CITIZEN"
    AUTHORITY = "AUTHORITY"
    ADMIN = "ADMIN"

class IncidentTypeEnum(str, enum.Enum):
    LANDSLIDE = "Landslide"
    FLOOD = "Flood"
    ROAD_BLOCKAGE = "Road Blockage"
    HEAVY_RAINFALL = "Heavy Rainfall"
    INFRASTRUCTURE_DAMAGE = "Infrastructure Damage"
    ACCIDENT = "Accident"
    STRANDED_PEOPLE = "Stranded People"
    OTHER = "Other"

class RiskLevelEnum(str, enum.Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IncidentStatusEnum(str, enum.Enum):
    REPORTED = "REPORTED"
    UNDER_REVIEW = "UNDER REVIEW"
    VERIFIED = "VERIFIED"
    TEAM_ASSIGNED = "TEAM ASSIGNED"
    IN_PROGRESS = "IN PROGRESS"
    RESOLVED = "RESOLVED"

class TeamTypeEnum(str, enum.Enum):
    RESCUE = "Rescue"
    MEDICAL = "Medical"
    POLICE = "Police"
    ROAD_MAINTENANCE = "Road Maintenance"
    FIRE = "Fire"
    DISASTER_RESPONSE = "Disaster Response"

class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.CITIZEN)
    phone = Column(String, nullable=True)
    district = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DBIncident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    incident_code = Column(String, unique=True, index=True)
    type = Column(SQLEnum(IncidentTypeEnum), default=IncidentTypeEnum.LANDSLIDE)
    description = Column(Text)
    severity = Column(String, default="HIGH")
    status = Column(SQLEnum(IncidentStatusEnum), default=IncidentStatusEnum.REPORTED)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    district = Column(String, default="Chamoli")
    photo_url = Column(String, nullable=True)
    affected_people = Column(Integer, default=1)
    road_blocked = Column(Boolean, default=False)
    risk_score = Column(Float, default=50.0)
    risk_level = Column(SQLEnum(RiskLevelEnum), default=RiskLevelEnum.MODERATE)
    risk_reasons = Column(Text, nullable=True)
    reports_count = Column(Integer, default=1)
    verified_by_authority = Column(Boolean, default=False)
    
    # Social Media Verification Metadata
    source_platform = Column(String, default="CITIZEN_APP")
    source_author = Column(String, nullable=True)
    source_url = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reports = relationship("DBIncidentReport", back_populates="incident")
    timeline = relationship("DBIncidentTimeline", back_populates="incident")
    assignments = relationship("DBAssignment", back_populates="incident")

class DBIncidentReport(Base):
    __tablename__ = "incident_reports"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    reporter_name = Column(String, default="Anonymous Citizen")
    reporter_contact = Column(String, nullable=True)
    description = Column(Text)
    photo_url = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    incident = relationship("DBIncident", back_populates="reports")

class DBRiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    score = Column(Float)
    level = Column(SQLEnum(RiskLevelEnum))
    severity_factor = Column(Float)
    rainfall_factor = Column(Float)
    history_factor = Column(Float)
    density_factor = Column(Float)
    vulnerability_factor = Column(Float)
    affected_factor = Column(Float)
    accessibility_factor = Column(Float)
    explanation_text = Column(Text)
    calculated_at = Column(DateTime, default=datetime.utcnow)

class DBResponseTeam(Base):
    __tablename__ = "response_teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    team_type = Column(SQLEnum(TeamTypeEnum), default=TeamTypeEnum.DISASTER_RESPONSE)
    base_location = Column(String)
    current_lat = Column(Float)
    current_lng = Column(Float)
    availability_status = Column(String, default="AVAILABLE")
    contact_number = Column(String)
    active_incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)

class DBAssignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    response_team_id = Column(Integer, ForeignKey("response_teams.id"))
    assigned_by = Column(String, default="District Control Room")
    notes = Column(Text, nullable=True)
    status = Column(String, default="ACTIVE")
    assigned_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    incident = relationship("DBIncident", back_populates="assignments")

class DBNotification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    recipient_role = Column(String, default="ALL")
    recipient_user_id = Column(Integer, nullable=True)
    title = Column(String)
    message = Column(Text)
    incident_id = Column(Integer, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DBIncidentTimeline(Base):
    __tablename__ = "incident_timeline"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status_from = Column(String)
    status_to = Column(String)
    note = Column(Text)
    action_by = Column(String, default="System")

    incident = relationship("DBIncident", back_populates="timeline")

class DBHistoricalIncident(Base):
    __tablename__ = "historical_incidents"
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String)
    district = Column(String)
    incident_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    risk_weight = Column(Float, default=1.0)

# Pydantic Schemas
class IncidentCreateSchema(BaseModel):
    type: IncidentTypeEnum
    description: str
    severity: str = "HIGH"
    latitude: float
    longitude: float
    address: str
    district: str = "Chamoli"
    affected_people: int = 1
    road_blocked: bool = False
    reporter_name: Optional[str] = "Anonymous Citizen"
    reporter_contact: Optional[str] = None
    photo_url: Optional[str] = None

class IncidentResponseSchema(BaseModel):
    id: int
    incident_code: str
    type: str
    description: str
    severity: str
    status: str
    latitude: float
    longitude: float
    address: str
    district: str
    photo_url: Optional[str] = None
    affected_people: int
    road_blocked: bool
    risk_score: float
    risk_level: str
    risk_reasons: Optional[str] = None
    reports_count: int
    verified_by_authority: bool
    source_platform: Optional[str] = "CITIZEN_APP"
    source_author: Optional[str] = None
    source_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
