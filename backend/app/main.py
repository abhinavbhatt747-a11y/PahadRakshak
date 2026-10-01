import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.api import auth, incidents, dashboard, map as map_api, response_teams, analytics, notifications, demo, social, gov
from backend.app.api.gov import sync_official_government_bulletins, feed_live_incident
from backend.app.ai.resolution_checker import ResolutionCheckerService
from database.seed_data import seed_database

async def auto_feed_live_incidents_loop():
    """
    Background worker loop that automatically feeds fresh live disaster alerts
    and runs road clearance checks every 45 seconds to purge resolved incidents from live maps.
    """
    await asyncio.sleep(10)
    while True:
        try:
            db = SessionLocal()
            
            # 1. Run Auto-Clearance Verifier to purge solved road blockages
            clearance_res = ResolutionCheckerService.check_and_resolve_cleared_incidents(db)
            if clearance_res["resolved_count"] > 0:
                print(f"[+] Auto-Clearance Check: Purged {clearance_res['resolved_count']} solved incidents from live map.")

            # 2. Feed fresh live government alert
            feed_live_incident(db=db)
            db.close()
            print("[+] Live Disaster Feed: Ingested fresh government alert into database.")
        except Exception as e:
            print(f"[!] Live Feed Warning: {e}")
        await asyncio.sleep(45)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Automatic Startup Lifecycle Handler.
    Executed automatically whenever you launch PahadRakshak:
    1. Creates/verifies database tables.
    2. Hydrates past historical incident records across Uttarakhand.
    3. Auto-fetches & feeds live official government bulletins (UKSDMA, IMD, Police, BRO).
    4. Launches continuous live background ingestion loop.
    """
    print("[STARTUP] Laptop / Server Powered ON - Initializing PahadRakshak Data Engine...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        from backend.app.models.schemas import DBIncident
        if db.query(DBIncident).count() == 0:
            print("[+] Database empty. Hydrating historical Uttarakhand disaster dataset...")
            seed_database()

        print("[+] Fetching & feeding live official government disaster alerts (UKSDMA, IMD, Police, BRO)...")
        sync_official_government_bulletins(db=db)
        
        # Ensure fresh initial live alerts exist
        feed_live_incident(db=db)
        print("[SUCCESS] PahadRakshak Data Engine Fully Hydrated & Live Feeding Active!")
    except Exception as e:
        print(f"[!] Startup Sync Warning: {e}")
    finally:
        db.close()

    # Launch background continuous live feed task
    feed_task = asyncio.create_task(auto_feed_live_incidents_loop())

    yield
    feed_task.cancel()
    print("[SHUTDOWN] Laptop / Server Powered OFF.")

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_SUBTITLE,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads"))
os.makedirs(upload_dir, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=upload_dir), name="uploads")

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(incidents.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(map_api.router, prefix="/api/v1")
app.include_router(response_teams.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(demo.router, prefix="/api/v1")
app.include_router(social.router, prefix="/api/v1")
app.include_router(gov.router, prefix="/api/v1")

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "subtitle": settings.APP_SUBTITLE,
        "environment": settings.APP_ENV,
        "database": settings.DATABASE_URL.split(":")[0],
        "sih_metadata": {
            "problem_id": settings.SIH_PROBLEM_ID,
            "problem_title": settings.SIH_PROBLEM_TITLE,
            "organization": settings.SIH_ORGANIZATION,
            "theme": settings.SIH_THEME
        }
    }

from fastapi.responses import FileResponse

@app.get("/download/pdf_11", tags=["Downloads"])
def download_pdf_11():
    pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "PahadRakshak_11Slide_Presentation.pdf"))
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="PahadRakshak_11Slide_Presentation.pdf"
        )
    return {"error": "11-Slide PDF file not found"}

@app.get("/download/pptx_11", tags=["Downloads"])
def download_pptx_11():
    pptx_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "PahadRakshak_11Slide_Presentation.pptx"))
    if os.path.exists(pptx_path):
        return FileResponse(
            pptx_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename="PahadRakshak_11Slide_Presentation.pptx"
        )
    return {"error": "11-Slide PPTX file not found"}

@app.get("/download/pdf", tags=["Downloads"])
def download_pdf():
    pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "PahadRakshak_11Slide_Presentation.pdf"))
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="PahadRakshak_11Slide_Presentation.pdf"
        )
    return {"error": "PDF file not found"}

@app.get("/download/pptx", tags=["Downloads"])
def download_pptx():
    pptx_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "PahadRakshak_11Slide_Presentation.pptx"))
    if os.path.exists(pptx_path):
        return FileResponse(
            pptx_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename="PahadRakshak_11Slide_Presentation.pptx"
        )
    return {"error": "PPTX file not found"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    ico_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "uploads", "favicon.ico"))
    if os.path.exists(ico_path):
        return FileResponse(ico_path)
    return {"error": "Favicon not found"}

@app.get("/", tags=["Health"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} - {settings.APP_SUBTITLE}",
        "docs": "/docs",
        "health": "/api/v1/health",
        "frontend": "/app/index.html"
    }

