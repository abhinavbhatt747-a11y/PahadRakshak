import random
from datetime import datetime
from typing import List, Dict, Any

class GovAlertCrawlerService:
    """
    Official Government Disaster & Alert Ingestion Crawler.
    Monitors official state emergency feeds:
    1. UKSDMA (Uttarakhand State Disaster Management Authority)
    2. IMD Meteorological Centre Dehradun (Weather Warnings)
    3. Uttarakhand State Police Emergency Control Room (Traffic & Accident Alerts)
    4. BRO (Border Roads Organisation Highway Clearance Bulletins)
    """

    OFFICIAL_GOV_SOURCES = [
        {
            "code": "UKSDMA",
            "name": "Uttarakhand State Disaster Management Authority (USDMA)",
            "portal_url": "https://usdma.uk.gov.in/",
            "agency_type": "STATE_DISASTER_AGENCY"
        },
        {
            "code": "IMD_DEHRADUN",
            "name": "IMD Meteorological Centre Dehradun",
            "portal_url": "https://mausam.imd.gov.in/dehradun/",
            "agency_type": "METEOROLOGICAL_DEPT"
        },
        {
            "code": "UK_POLICE",
            "name": "Uttarakhand State Police Control Room",
            "portal_url": "https://uttarakhandpolice.uk.gov.in/",
            "agency_type": "LAW_ENFORCEMENT"
        },
        {
            "code": "BRO_UTTARAKHAND",
            "name": "Border Roads Organisation (Project Shivalik / Hirak)",
            "portal_url": "https://bro.gov.in/",
            "agency_type": "ROAD_INFRASTRUCTURE"
        }
    ]

    MOCK_LIVE_GOV_BULLETINS = [
        {
            "source_code": "UKSDMA",
            "bulletin_id": "UKSDMA-ALERT-2026-891",
            "title": "UKSDMA Official Red Warning: Flash Flood Alert in Alaknanda Basin",
            "description": "[OFFICIAL GOVT BULLETIN - UKSDMA] State Emergency Operation Centre issues RED ALERT for Alaknanda river basin near Joshimath & Helang due to rapid upstream water level rise.",
            "district": "Chamoli",
            "location": "Alaknanda Basin, Joshimath-Helang Corridor",
            "incident_type": "Flood",
            "severity": "CRITICAL",
            "affected_people": 50,
            "road_blocked": True,
            "latitude": 30.5570,
            "longitude": 79.5680,
            "official_url": "https://usdma.uk.gov.in/"
        },
        {
            "source_code": "IMD_DEHRADUN",
            "bulletin_id": "IMD-DDN-CW-402",
            "title": "IMD Dehradun Heavy Cloudburst & Landslide Warning",
            "description": "[OFFICIAL GOVT BULLETIN - IMD DEHRADUN] Severe localized cloudburst and slope instability forecast over Yamunotri Highway stretch in Uttarkashi district.",
            "district": "Uttarkashi",
            "location": "Yamunotri Highway Corridor, Barkot-Syana Chatti",
            "incident_type": "Heavy Rainfall",
            "severity": "HIGH",
            "affected_people": 20,
            "road_blocked": True,
            "latitude": 30.9830,
            "longitude": 78.4350,
            "official_url": "https://mausam.imd.gov.in/dehradun/"
        },
        {
            "source_code": "UK_POLICE",
            "bulletin_id": "UKP-TRAFFIC-1049",
            "title": "Uttarakhand Police Control Room: Clement Town Dehradun Highway Collision",
            "description": "[OFFICIAL GOVT BULLETIN - UTTARAKHAND POLICE] Traffic PCR reports heavy commercial vehicle crash near Graphic Era Clement Town corridor. Traffic diverted.",
            "district": "Dehradun",
            "location": "Near Graphic Era University, Clement Town, Dehradun",
            "incident_type": "Accident",
            "severity": "HIGH",
            "affected_people": 5,
            "road_blocked": True,
            "latitude": 30.2688,
            "longitude": 78.0076,
            "official_url": "https://uttarakhandpolice.uk.gov.in/"
        },
        {
            "source_code": "BRO_UTTARAKHAND",
            "bulletin_id": "BRO-SHIVALIK-774",
            "title": "BRO Highway Advisory: Badrinath National Highway NH-07 Landslide Clearance",
            "description": "[OFFICIAL GOVT BULLETIN - BRO] Project Shivalik heavy bulldozers deployed for slope clearance at Lambagarh landslide zone on NH-07.",
            "district": "Chamoli",
            "location": "Lambagarh Landslide Stretch, NH-07 Badrinath Highway",
            "incident_type": "Landslide",
            "severity": "CRITICAL",
            "affected_people": 35,
            "road_blocked": True,
            "latitude": 30.6321,
            "longitude": 79.5284,
            "official_url": "https://bro.gov.in/"
        }
    ]

    @classmethod
    def fetch_latest_official_alerts(cls) -> List[Dict[str, Any]]:
        """
        Simulates fetching live official government bulletins from UKSDMA, IMD, UK Police, and BRO servers.
        In production, this executes real-time HTTP webhooks and RSS/REST crawlers against gov portal endpoints.
        """
        return cls.MOCK_LIVE_GOV_BULLETINS
