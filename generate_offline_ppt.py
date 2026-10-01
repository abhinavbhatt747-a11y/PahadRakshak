import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_offline_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    DARK_BG = RGBColor(11, 19, 41)       # #0b1329
    CARD_BG = RGBColor(21, 32, 60)       # #15203c
    BORDER_CLR = RGBColor(30, 58, 138)   # #1e3a8a
    WHITE = RGBColor(255, 255, 255)
    CYAN = RGBColor(56, 189, 248)       # #38bdf8
    GOLD = RGBColor(251, 191, 36)       # #fbbf24
    GREEN = RGBColor(52, 211, 153)      # #34d399
    RED = RGBColor(248, 113, 113)       # #f87171
    GRAY = RGBColor(148, 163, 184)      # #94a3b8

    slides_data = [
        # SLIDE 1: TITLE SLIDE
        {
            "tag": "HACKATHON JURY PRESENTATION (OFFLINE EDITION)",
            "title": "PahadRakshak (पहाड़ रक्षक)",
            "subtitle": "Next-Gen Offline AI Disaster Navigation & Emergency Mesh Response for Himalayan Highways",
            "boxes": [
                {"title": "Project Institution", "text": "Swami Rama Himalayan University (SRHU), Dehradun", "color": GREEN},
                {"title": "Engineering Team", "text": "6 BCA Student Developers (TechForge 3.0 / SIH 2026)", "color": GOLD},
                {"title": "Offline Target Scope", "text": "All 13 Mountain Districts (Zero Internet / Deep Valleys)", "color": CYAN}
            ]
        },
        # SLIDE 2: THE OFFLINE PROBLEM
        {
            "tag": "OFFLINE CHALLENGE",
            "title": "The Himalayan Cellular Blackout Dilemma",
            "subtitle": "Why Standard Apps Break Down in Mountain Disasters",
            "boxes": [
                {"title": "🔴 Cellular Signal Blackout", "text": "Cloudbursts and landslides severe optical fiber lines and knock out cell towers in deep Garhwal & Kumaon valleys, leaving travelers with 0-bar internet signal.", "color": RED},
                {"title": "🛑 Online Apps Crash Completely", "text": "Google Maps and web navigation apps stop rendering tiles, routes, or warnings the moment internet disconnects, stranding vehicles in disaster zones.", "color": RED},
                {"title": "⏳ Delayed SOS Transmission", "text": "Citizens cannot send web API requests during landslides. Without offline storage, critical emergency calls are permanently lost.", "color": RED},
                {"title": "📢 Misinformation Panic", "text": "Travelers lack local cached hazard maps, leading to chaotic turns into active rockfall zones without knowing clear bypasses.", "color": RED}
            ]
        },
        # SLIDE 3: HOW PAHADRAKSHAK WORKS OFFLINE
        {
            "tag": "OFFLINE ARCHITECTURE",
            "title": "How PahadRakshak Operates 100% Offline",
            "subtitle": "Zero-Internet Autonomous Resilience Engine",
            "boxes": [
                {"title": "📲 1. Local PWA & Cache Storage", "text": "ServiceWorker & IndexedDB pre-cache complete road networks, safe relief shelters, emergency contacts, and offline map vectors locally on the device.", "color": GREEN},
                {"title": "🔀 2. Offline Vector Routing Engine", "text": "Calculates primary vs safe bypass routes directly inside the device's browser memory without contacting an external server.", "color": GREEN},
                {"title": "📡 3. Offline SMS & Mesh Queue", "text": "Stores citizen hazard reports in local IndexedDB. Automatically dispatches via SMS protocol or Bluetooth mesh when signal drops.", "color": GREEN}
            ]
        },
        # SLIDE 4: DUAL PORTAL IN OFFLINE MODE
        {
            "tag": "OFFLINE PORTALS",
            "title": "Dual-Portal Ecosystem in Offline Mode",
            "subtitle": "Seamless Operation for Citizens & Control Rooms",
            "boxes": [
                {"title": "👥 Public Citizen Offline Portal", "text": "Frictionless PWA interface. Works without internet connection: 1-Tap SOS save, offline dialer (112, 1070, 1077, 108, BRO), cached relief shelter directory, and local weather radar.", "color": CYAN},
                {"title": "🛡️ Authority Offline Command Center", "text": "Local officer clearance verification (`UKSDMA-OFFICER-01`). Allows officers to manage triage queues and issue local broadcast bulletins even over local radio/mesh networks.", "color": GOLD}
            ]
        },
        # SLIDE 5: OFFLINE MULTI-FACTOR RISK ENGINE
        {
            "tag": "OFFLINE AI RISK ENGINE",
            "title": "On-Device Multi-Factor AI Risk Calculation",
            "subtitle": "Deterministic Local Risk Scoring Formula (0-100)",
            "boxes": [
                {"title": "🧮 Local Risk Score Formula", "text": "Risk = (Severity * 0.25) + (Rainfall * 0.20) + (History * 0.15) + (Road Blocked * 0.15) + (Affected People * 0.15) + (Density * 0.10)", "color": GOLD},
                {"title": "🔴 CRITICAL RISK (80-100)", "text": "Evaluated locally: Cloudburst, complete road blockage, life threat. Prompts immediate safe bypass routing.", "color": RED},
                {"title": "🟠 HIGH RISK (60-79)", "text": "Evaluated locally: Landslide debris, highway obstruction. Renders Route B green bypass.", "color": RED},
                {"title": "🟢 MODERATE / LOW (0-59)", "text": "Evaluated locally: Minimal road movement affected. Confirms road safe for single-line traffic.", "color": GREEN}
            ]
        },
        # SLIDE 6: OFFLINE DUAL-ROUTE NAVIGATION
        {
            "tag": "OFFLINE NAVIGATION",
            "title": "Smart Conditional Dual-Route Routing (Offline)",
            "subtitle": "Local OSRM & Haversine Vector Math",
            "boxes": [
                {"title": "✅ Primary Highway Safe (Offline)", "text": "When local cache confirms no road blockages, the map renders 1 single clean glowing blue line to destination.", "color": GREEN},
                {"title": "🔀 Primary Highway Unsafe (Offline)", "text": "When local IndexedDB records a blockage, the device renders 2 paths: Route A (Red Dashed Unsafe) vs Route B (Green Glowing Safe Bypass).", "color": RED}
            ]
        },
        # SLIDE 7: OFFLINE GOVERNMENT BULLETIN SYNC
        {
            "tag": "BULLETIN SYNC",
            "title": "Official Government Bulletin Sync & Fallbacks",
            "subtitle": "Pre-Cached State Disaster Feeds & Validated Links",
            "boxes": [
                {"title": "🏛️ Pre-Cached Government Feeds", "text": "Stores official bulletins from UKSDMA, IMD Dehradun, BRO Shivalik, and Police PCR locally so they remain accessible during internet loss.", "color": CYAN},
                {"title": "🌐 Validated Source Links", "text": "All official links point to root government domains (https://usdma.uk.gov.in/, https://bro.gov.in/) ensuring 100% uptime without 404 errors.", "color": GOLD}
            ]
        },
        # SLIDE 8: AUTOMATED ROAD CLEARANCE (OFFLINE)
        {
            "tag": "ROAD CLEARANCE",
            "title": "Automated Road Clearance & Map Purging",
            "subtitle": "Zero Ghost Markers Policy in Offline Storage",
            "boxes": [
                {"title": "🧹 Auto-Clearance Verifier", "text": "Scans local database and removes resolved hazards as soon as BRO/SDRF teams verify road clearance.", "color": GREEN},
                {"title": "⚡ Instant Map Refresh", "text": "Purges resolved red blockage lines from local device memory so travelers never see stale or fake road blockages.", "color": CYAN}
            ]
        },
        # SLIDE 9: OFFLINE LOCATION WEATHER BROADCAST
        {
            "tag": "OFFLINE WEATHER",
            "title": "Location Weather Broadcasting (Offline Sync)",
            "subtitle": "Local GPS Weather Forecasting & IMD Radar",
            "boxes": [
                {"title": "📍 User Location Weather Banner", "text": "'THIS IS YOUR LOCATION & THIS IS THE WEATHER IN YOUR AREA' — Displays live temperature, rain mm, wind speed, and humidity for exact GPS coordinates.", "color": CYAN},
                {"title": "🌤️ Offline IMD Radar Layer", "text": "Pre-renders Doppler precipitation circles and rain badges across Chamoli, Uttarkashi, Rudraprayag, and Dehradun.", "color": GOLD}
            ]
        },
        # SLIDE 10: PUBLIC CITIZEN SAFETY (OFFLINE PWA)
        {
            "tag": "CITIZEN SAFETY",
            "title": "Public Citizen Emergency Features (Offline PWA)",
            "subtitle": "1-Tap Lifesaving Tools for Mountain Travelers",
            "boxes": [
                {"title": "📢 1-Tap Offline SOS Report", "text": "Saves citizen report, hardware GPS coordinates, and photo proof locally into PWA storage for instant sync.", "color": CYAN},
                {"title": "📞 1-Tap Emergency Helplines", "text": "Direct native phone dialers for 112 (National Emergency), 1070 (UKSDMA), 1077 (District), 108 (Ambulance), and BRO.", "color": GREEN},
                {"title": "🏥 Cached Relief Shelters", "text": "Complete offline directory of open evacuation centers (SRHU Base, Chamoli GIC, Joshimath Helipad, Rishikesh Transit).", "color": GOLD}
            ]
        },
        # SLIDE 11: AUTHORITY COMMAND CENTER (OFFLINE)
        {
            "tag": "AUTHORITY TOOLS",
            "title": "Secured Command Center (Offline Operation)",
            "subtitle": "Disaster Triage & Team Dispatch via Local Mesh",
            "boxes": [
                {"title": "📡 Statewide Bulletin Broadcaster", "text": "Broadcasts emergency government warnings locally across authority terminals and citizen PWA apps.", "color": GOLD},
                {"title": "🔥 AI Priority Triage Queue", "text": "Automatically ranks incoming citizen reports descending by multi-factor risk score (0-100).", "color": RED},
                {"title": "🚒 1-Click Rescue Team Dispatch", "text": "Assigns SDRF, NDRF, BRO heavy machinery, and medical units to exact incident GPS coordinates.", "color": GREEN}
            ]
        },
        # SLIDE 12: TECHNICAL STACK & OFFLINE PWA
        {
            "tag": "TECH STACK",
            "title": "Offline-First Technical Architecture",
            "subtitle": "FastAPI, ServiceWorker, Leaflet & OSRM Engine",
            "boxes": [
                {"title": "⚡ Backend Engine", "text": "Python 3.10+, FastAPI, Uvicorn, SQLite, Asyncio Background Feeder.", "color": CYAN},
                {"title": "📱 PWA & GIS Client", "text": "HTML5 PWA ServiceWorker, Leaflet.js, OSRM Driving Engine, TailwindCSS.", "color": GREEN},
                {"title": "🔒 HTTPS Hardware GPS", "text": "Runs over HTTPS (port 8443) allowing native mobile browsers to grant hardware GPS access offline.", "color": GOLD}
            ]
        },
        # SLIDE 13: JURY DEMONSTRATION & PROOF OF WORK
        {
            "tag": "PROOF OF WORK",
            "title": "Fully Functional Live Systems & Off-Grid Verification",
            "subtitle": "Tested Across Uttarakhand Mountain Corridors",
            "boxes": [
                {"title": "🌐 Landing Portal Selector", "text": "http://127.0.0.1:8000/app/index.html — Dual-portal selector (Public vs Authority).", "color": CYAN},
                {"title": "👥 Public Citizen Portal", "text": "http://127.0.0.1:8000/app/citizen.html — 1-Tap SOS, Helplines & Shelters.", "color": GREEN},
                {"title": "🛡️ Authority Command Center", "text": "http://127.0.0.1:8000/app/dashboard.html — Officer Verification (`UKSDMA-OFFICER-01`).", "color": GOLD},
                {"title": "🗺️ Live Map & Offline GPS", "text": "https://192.168.31.175:8443/app/map.html — Hardware GPS, Dual Routing & Weather.", "color": RED}
            ]
        },
        # SLIDE 14: TEAM & CONCLUSION
        {
            "tag": "TEAM & CONCLUSION",
            "title": "PahadRakshak: Saving Lives Beyond the Grid",
            "subtitle": "Swami Rama Himalayan University (SRHU) Student Engineering Team",
            "boxes": [
                {"title": "🎓 Student Engineering Team", "text": "Developed by 6 BCA Students at Swami Rama Himalayan University (SRHU), Dehradun for TechForge 3.0 & SIH 2026.", "color": GREEN},
                {"title": "🏔️ Himalayan Mission", "text": "Transforming mountain disaster response from reactive panic to autonomous, offline-first predictive safety across Uttarakhand.", "color": GOLD}
            ]
        }
    ]

    for slide_idx, sdata in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)

        # Slide Background
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = DARK_BG
        bg_shape.line.fill.background()

        # Top Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf = tag_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"SLIDE {slide_idx+1} OF 14  |  {sdata['tag']}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CYAN

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = sdata["title"]
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = sdata["subtitle"]
        p_sub.font.size = Pt(14)
        p_sub.font.color.rgb = GRAY

        # Render Content Cards / Boxes
        boxes = sdata["boxes"]
        num_boxes = len(boxes)

        if num_boxes == 2:
            box_width = Inches(5.6)
            box_height = Inches(4.8)
            positions = [(Inches(0.8), Inches(2.1)), (Inches(6.8), Inches(2.1))]
        elif num_boxes == 3:
            box_width = Inches(3.6)
            box_height = Inches(4.8)
            positions = [(Inches(0.8), Inches(2.1)), (Inches(4.85), Inches(2.1)), (Inches(8.9), Inches(2.1))]
        elif num_boxes == 4:
            box_width = Inches(5.6)
            box_height = Inches(2.25)
            positions = [
                (Inches(0.8), Inches(2.1)), (Inches(6.8), Inches(2.1)),
                (Inches(0.8), Inches(4.65)), (Inches(6.8), Inches(4.65))
            ]
        else:
            box_width = Inches(11.7)
            box_height = Inches(4.8)
            positions = [(Inches(0.8), Inches(2.1))]

        for b_idx, binfo in enumerate(boxes):
            pos_x, pos_y = positions[b_idx]

            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pos_x, pos_y, box_width, box_height)
            card.fill.solid()
            card.fill.fore_color.rgb = CARD_BG
            card.line.color.rgb = BORDER_CLR
            card.line.width = Pt(1.5)

            # Card Header Title
            tb_hdr = slide.shapes.add_textbox(pos_x + Inches(0.2), pos_y + Inches(0.2), box_width - Inches(0.4), Inches(0.6))
            p_hdr = tb_hdr.text_frame.paragraphs[0]
            p_hdr.text = binfo["title"]
            p_hdr.font.size = Pt(16)
            p_hdr.font.bold = True
            p_hdr.font.color.rgb = binfo["color"]

            # Card Body Text
            tb_body = slide.shapes.add_textbox(pos_x + Inches(0.2), pos_y + Inches(0.8), box_width - Inches(0.4), box_height - Inches(1.0))
            tb_body.text_frame.word_wrap = True
            p_b = tb_body.text_frame.paragraphs[0]
            p_b.text = binfo["text"]
            p_b.font.size = Pt(12)
            p_b.font.color.rgb = WHITE

        # Footer
        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.3))
        p_ft = ft_box.text_frame.paragraphs[0]
        p_ft.text = "PahadRakshak Offline Emergency Deck  |  Swami Rama Himalayan University (SRHU) BCA Engineering Team"
        p_ft.font.size = Pt(10)
        p_ft.font.color.rgb = GRAY

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "PahadRakshak_Offline_Presentation.pptx")
    prs.save(output_path)
    print(f"[+] Native Offline PowerPoint Presentation Generated Successfully at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_offline_presentation()
