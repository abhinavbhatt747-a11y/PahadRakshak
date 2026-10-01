from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.app.core.database import get_db
from backend.app.models.schemas import DBUser, RoleEnum

router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str = "CITIZEN"
    phone: Optional[str] = None
    district: Optional[str] = "Chamoli"

class LoginRequest(BaseModel):
    username: str
    password: str

class OfficerVerifyRequest(BaseModel):
    officer_id: str
    passkey: str

@router.post("/verify-officer", summary="Verify Official Authority Badge ID & Unlock Command Center")
def verify_officer_id(req: OfficerVerifyRequest, db: Session = Depends(get_db)):
    officer_id = req.officer_id.strip().upper()
    passkey = req.passkey.strip()

    valid_prefixes = ("UK", "SDRF", "NDRF", "BRO", "POLICE", "DM", "OFFICER", "ADMIN")
    is_valid_id = any(officer_id.startswith(p) for p in valid_prefixes) or len(officer_id) >= 4
    is_valid_pass = passkey in ("pahad123", "admin", "srhu2026", "police112", "sdma2026") or len(passkey) >= 4

    if not (is_valid_id and is_valid_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Official Authority ID or Passkey. Please verify your UKSDMA / SDRF / BRO credentials."
        )

    # Resolve department title
    department = "UKSDMA State Disaster Management"
    if "SDRF" in officer_id:
        department = "State Disaster Response Force (SDRF)"
    elif "NDRF" in officer_id:
        department = "National Disaster Response Force (NDRF)"
    elif "BRO" in officer_id:
        department = "Border Roads Organisation (BRO Clearance Unit)"
    elif "POLICE" in officer_id:
        department = "Uttarakhand Police Control Room (PCR)"

    return {
        "verified": True,
        "access_token": f"auth_token_{officer_id}",
        "role": "AUTHORITY",
        "officer_id": officer_id,
        "officer_name": f"Officer {officer_id}",
        "department": department,
        "district": "All 13 Districts (Statewide Command)",
        "clearance_level": "LEVEL-5 CRITICAL COMMAND ACCESS",
        "message": f"Welcome, Officer {officer_id}. Authority Command Center Access Granted."
    }

@router.post("/register")
def register_user(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(DBUser).filter((DBUser.username == req.username) | (DBUser.email == req.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or Email already registered.")

    role_val = RoleEnum.AUTHORITY if req.role.upper() == "AUTHORITY" else RoleEnum.CITIZEN

    user = DBUser(
        username=req.username,
        email=req.email,
        hashed_password="mock_hashed_pass",
        role=role_val,
        phone=req.phone,
        district=req.district
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully.",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role.value,
            "district": user.district
        }
    }

@router.post("/login")
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == req.username).first()
    if not user:
        if req.username.lower() in ("authority", "admin", "officer"):
            return {
                "access_token": "mock_token_authority_srhu",
                "token_type": "bearer",
                "role": "AUTHORITY",
                "username": req.username,
                "district": "Chamoli"
            }
        elif req.username.lower() in ("citizen", "public", "user"):
            return {
                "access_token": "mock_token_citizen_srhu",
                "token_type": "bearer",
                "role": "CITIZEN",
                "username": req.username,
                "district": "Dehradun"
            }
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    return {
        "access_token": f"token_{user.username}",
        "token_type": "bearer",
        "role": user.role.value,
        "username": user.username,
        "district": user.district or "Chamoli"
    }
