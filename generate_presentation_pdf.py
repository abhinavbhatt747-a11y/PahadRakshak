import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Draw Background Fill
        self.setFillColor(colors.HexColor('#0b1329'))
        self.rect(0, 0, 792, 612, fill=True, stroke=False)

        # Draw Top Header Bar Line
        self.setStrokeColor(colors.HexColor('#1e3a8a'))
        self.setLineWidth(1)
        self.line(40, 565, 752, 565)

        # Draw Footer Line & Text
        self.line(40, 45, 752, 45)
        self.setFillColor(colors.HexColor('#94a3b8'))
        self.setFont("Helvetica", 9)
        self.drawString(40, 30, "PahadRakshak Hackathon Presentation  |  Swami Rama Himalayan University (SRHU) BCA Team")
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(752, 30, page_str)

def create_presentation_pdf():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend"))
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "PahadRakshak_Presentation.pdf")

    # 11 x 8.5 inches landscape (792 x 612 pt)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    style_category = ParagraphStyle(
        'CategoryTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#38bdf8'),
        spaceAfter=4
    )

    style_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#ffffff'),
        spaceAfter=6
    )

    style_subtitle = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#94a3b8'),
        spaceAfter=15
    )

    style_box_hdr_cyan = ParagraphStyle('BoxHdrCyan', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#38bdf8'), spaceAfter=4)
    style_box_hdr_gold = ParagraphStyle('BoxHdrGold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#fbbf24'), spaceAfter=4)
    style_box_hdr_green = ParagraphStyle('BoxHdrGreen', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#34d399'), spaceAfter=4)
    style_box_hdr_red = ParagraphStyle('BoxHdrRed', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#f87171'), spaceAfter=4)

    style_box_body = ParagraphStyle(
        'BoxBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#e2e8f0')
    )

    slides_content = [
        # SLIDE 1
        {
            "tag": "HACKATHON JURY PRESENTATION (TEAM PDF EDITION)",
            "title": "PahadRakshak (पहाड़ रक्षक)",
            "subtitle": "Next-Gen AI Mountain Disaster Navigation, Live Government Sync & Emergency Response System",
            "boxes": [
                {"hdr_style": style_box_hdr_green, "title": "Project Institution", "body": "Swami Rama Himalayan University (SRHU), Dehradun, Uttarakhand."},
                {"hdr_style": style_box_hdr_gold, "title": "Engineering Team", "body": "6 BCA Student Developers (TechForge 3.0 / SIH 2026 Adaptation)."},
                {"hdr_style": style_box_hdr_cyan, "title": "Target Scope", "body": "All 13 Mountain Districts of Uttarakhand (Char Dham Highways)."}
            ]
        },
        # SLIDE 2
        {
            "tag": "PROBLEM STATEMENT",
            "title": "The Himalayan Mountain Disaster Crisis",
            "subtitle": "Why Standard Commercial Apps Fail During Mountain Landslides & Cloudbursts",
            "boxes": [
                {"hdr_style": style_box_hdr_red, "title": "🔴 Frequent Slope Failures", "body": "Monsoons trigger landslides on NH-07 (Badrinath) and NH-109 (Kedarnath), stranding thousands of pilgrims without warning."},
                {"hdr_style": style_box_hdr_red, "title": "🛑 Blind Commercial Navigation", "body": "Google Maps blindly directs vehicles into active landslide debris because it lacks live UKSDMA/BRO disaster alerts."},
                {"hdr_style": style_box_hdr_red, "title": "⏳ Delayed Emergency Triage", "body": "Distress calls lack hardware GPS coordinates and verified photos, delaying SDRF, NDRF, and BRO heavy machinery dispatch."},
                {"hdr_style": style_box_hdr_red, "title": "📢 Rumors & Ghost Blockages", "body": "Unverified social media rumors cause panic, while solved road clearance updates take hours to reach travelers."}
            ]
        },
        # SLIDE 3
        {
            "tag": "OUR SOLUTION",
            "title": "PahadRakshak: Intelligent Disaster Ecosystem",
            "subtitle": "Autonomous Safety & Response System for Mountain Travelers",
            "boxes": [
                {"hdr_style": style_box_hdr_green, "title": "🔀 Conditional Dual-Route Bypass", "body": "Renders 1 clean blue line when safe; 2 paths (Red Unsafe vs Green Safe Bypass) ONLY when primary route is blocked."},
                {"hdr_style": style_box_hdr_cyan, "title": "🏛️ Live Government Bulletin Sync", "body": "Direct web/REST crawlers syncing UKSDMA, IMD Dehradun, BRO Shivalik, and Police PCR bulletins with source proof links."},
                {"hdr_style": style_box_hdr_gold, "title": "🛡️ Dual-Portal Architecture", "body": "Frictionless Public Citizen Portal for travelers + Secured Command Center with Officer ID (`UKSDMA-OFFICER-01`)."}
            ]
        },
        # SLIDE 4
        {
            "tag": "SYSTEM ARCHITECTURE",
            "title": "End-to-End Data Pipeline & GIS Engine",
            "subtitle": "High-Performance Data Flow & Geo-Spatial Calculation Engine",
            "boxes": [
                {"hdr_style": style_box_hdr_cyan, "title": "1. Data Ingestion", "body": "Citizen SOS + Hardware GPS + Live UKSDMA / IMD / BRO / Police Crawlers."},
                {"hdr_style": style_box_hdr_gold, "title": "2. AI Risk Engine", "body": "Multi-Factor Risk Calculator (0-100) + Geo-Spatial Cluster Detector."},
                {"hdr_style": style_box_hdr_green, "title": "3. FastAPI Backend", "body": "Asynchronous REST Endpoints + SQLite/PostgreSQL + Auto-Clearance Feeder."},
                {"hdr_style": style_box_hdr_red, "title": "4. Interactive Clients", "body": "Leaflet.js GIS Map + OSRM Driving Engine + Progressive Web App (PWA)."}
            ]
        },
        # SLIDE 5
        {
            "tag": "ROLE SEGMENTATION",
            "title": "Dual-Portal Access System",
            "subtitle": "Frictionless Public Portal vs Secured Control Room Command",
            "boxes": [
                {"hdr_style": style_box_hdr_cyan, "title": "👥 Public Citizen Portal", "body": "No login required. Features 1-tap SOS reporting, verified photo upload, 1-tap emergency helplines (112, 1070, 1077, 108, BRO), relief shelter finder, and weather warnings."},
                {"hdr_style": style_box_hdr_gold, "title": "🛡️ Authority Command Center", "body": "Secured by Officer Badge Verification (`UKSDMA-OFFICER-01`). Broadcasts disaster bulletins, manages AI priority queue, dispatches rescue teams (SDRF, NDRF, BRO)."}
            ]
        },
        # SLIDE 6
        {
            "tag": "AI RISK ENGINE",
            "title": "Multi-Factor Risk Calculation Engine (0-100)",
            "subtitle": "Deterministic Multi-Variable Risk Formula",
            "boxes": [
                {"hdr_style": style_box_hdr_gold, "title": "🧮 Multi-Factor Risk Formula", "body": "Risk Score = (Severity * 0.25) + (Rainfall * 0.20) + (History * 0.15) + (Road Blocked * 0.15) + (Affected People * 0.15) + (Density * 0.10)"},
                {"hdr_style": style_box_hdr_red, "title": "🔴 CRITICAL (80-100)", "body": "Cloudburst, complete road blockage, life threat. Prompts immediate green bypass routing."},
                {"hdr_style": style_box_hdr_gold, "title": "🟠 HIGH (60-79)", "body": "Landslide debris, highway obstruction. Renders Route B safe bypass."},
                {"hdr_style": style_box_hdr_green, "title": "🟢 MODERATE / LOW (0-59)", "body": "Minimal road movement affected. Confirms road safe for single-line traffic."}
            ]
        },
        # SLIDE 7
        {
            "tag": "SMART ROUTING",
            "title": "Conditional Dual-Route Bypass System",
            "subtitle": "Smart Geometry Rendering for Mountain Highways",
            "boxes": [
                {"hdr_style": style_box_hdr_green, "title": "✅ Primary Highway Safe Scenario", "body": "When no road blockages exist along the highway, the map renders 1 single clean glowing blue line without screen clutter."},
                {"hdr_style": style_box_hdr_red, "title": "🔀 Primary Highway Unsafe Scenario", "body": "When a blockage is detected, the engine renders 2 paths: Route A (Red Dashed Unsafe) vs Route B (Green Glowing Safe Bypass)."}
            ]
        },
        # SLIDE 8
        {
            "tag": "GOVT INTEGRATION",
            "title": "Live Government Bulletin Ingestion",
            "subtitle": "Direct Synchronization with State Disaster Authorities",
            "boxes": [
                {"hdr_style": style_box_hdr_cyan, "title": "🏛️ UKSDMA", "body": "State Disaster Management Bulletins (https://usdma.uk.gov.in/)."},
                {"hdr_style": style_box_hdr_gold, "title": "🌤️ IMD Dehradun", "body": "Meteorological Centre Cloudburst Warnings (https://mausam.imd.gov.in/dehradun/)."},
                {"hdr_style": style_box_hdr_green, "title": "🚜 BRO Shivalik", "body": "Border Roads Organisation Clearance Logs (https://bro.gov.in/)."},
                {"hdr_style": style_box_hdr_red, "title": "🚓 Police PCR", "body": "Uttarakhand Police Highway PCR Updates (https://uttarakhandpolice.uk.gov.in/)."}
            ]
        },
        # SLIDE 9
        {
            "tag": "AUTO CLEARANCE",
            "title": "Automated Road Clearance & Map Purging",
            "subtitle": "Zero Ghost Markers Policy on Live Map",
            "boxes": [
                {"hdr_style": style_box_hdr_green, "title": "🧹 Auto-Clearance Service", "body": "ResolutionCheckerService continuously scans BRO heavy machinery updates and field reports."},
                {"hdr_style": style_box_hdr_cyan, "title": "⚡ Instant Marker Purge", "body": "When an incident is marked RESOLVED, it is instantly purged from live map markers and navigation route calculations."}
            ]
        },
        # SLIDE 10
        {
            "tag": "LOCATION WEATHER",
            "title": "IMD Weather Broadcasting & User Location Weather",
            "subtitle": "Exact GPS Location Weather & Statewide IMD Radar",
            "boxes": [
                {"hdr_style": style_box_hdr_cyan, "title": "📍 User Location Weather Card", "body": "'THIS IS YOUR LOCATION & THIS IS THE WEATHER IN YOUR AREA' — Live temperature, rain mm, wind speed, humidity for exact GPS position."},
                {"hdr_style": style_box_hdr_gold, "title": "🌤️ Statewide IMD Radar Layer", "body": "Precipitation Doppler circles & rainfall mm badges across Chamoli, Uttarkashi, Rudraprayag, Dehradun, and Nainital."}
            ]
        },
        # SLIDE 11
        {
            "tag": "CITIZEN PORTAL",
            "title": "Public Citizen Emergency Safety Tools",
            "subtitle": "1-Tap Safety Features for Mountain Travelers",
            "boxes": [
                {"hdr_style": style_box_hdr_cyan, "title": "📢 1-Tap SOS Reporting", "body": "Upload ground reports with photo proof and hardware GPS coordinates."},
                {"hdr_style": style_box_hdr_green, "title": "📞 1-Tap Emergency Dialers", "body": "Direct quick dialers for 112 (National Emergency), 1070 (UKSDMA), 1077 (District), 108 (Ambulance), and BRO."},
                {"hdr_style": style_box_hdr_gold, "title": "🏥 Relief Shelter Directory", "body": "Verified directory of open evacuation camps (SRHU Base, Chamoli Camp, Joshimath Helipad, Rishikesh Transit)."}
            ]
        },
        # SLIDE 12
        {
            "tag": "AUTHORITY COMMAND",
            "title": "Secured State Command Center Tools",
            "subtitle": "Disaster Triage & Emergency Team Dispatch",
            "boxes": [
                {"hdr_style": style_box_hdr_gold, "title": "📡 Bulletin Broadcaster", "body": "Issue official government disaster bulletins pushing to citizen apps in under 1 second."},
                {"hdr_style": style_box_hdr_red, "title": "🔥 AI Priority Queue", "body": "Auto-ranked incident queue prioritizing life-threatening hazards descending by risk score."},
                {"hdr_style": style_box_hdr_green, "title": "🚒 1-Click Team Dispatch", "body": "Deploy SDRF, NDRF, BRO heavy machinery, and medical units to exact incident coordinates."}
            ]
        },
        # SLIDE 13
        {
            "tag": "TECH STACK",
            "title": "Robust Technical Stack & Infrastructure",
            "subtitle": "Production-Grade Engineering & PWA Architecture",
            "boxes": [
                {"hdr_style": style_box_hdr_cyan, "title": "⚡ Backend Engine", "body": "Python 3.10+, FastAPI, Uvicorn, SQLite, Asyncio Background Feeder."},
                {"hdr_style": style_box_hdr_green, "title": "🗺️ GIS & PWA Client", "body": "Leaflet.js, OSRM Routing Engine, TailwindCSS, HTML5 PWA ServiceWorker."},
                {"hdr_style": style_box_hdr_gold, "title": "🔒 HTTPS Hardware GPS", "body": "Runs on HTTPS (port 8443) allowing native mobile browsers to grant hardware GPS access."}
            ]
        },
        # SLIDE 14
        {
            "tag": "TEAM & CONCLUSION",
            "title": "PahadRakshak: Saving Lives in the Himalayas",
            "subtitle": "Swami Rama Himalayan University (SRHU) Student Engineering Team",
            "boxes": [
                {"hdr_style": style_box_hdr_green, "title": "🎓 Student Engineering Team", "body": "Built by 6 BCA Students at Swami Rama Himalayan University (SRHU), Dehradun for TechForge 3.0 & SIH 2026."},
                {"hdr_style": style_box_hdr_gold, "title": "🏔️ Himalayan Mission", "body": "Transforming mountain disaster response from reactive panic to autonomous predictive safety across Uttarakhand."}
            ]
        }
    ]

    story = []

    for s_idx, sdata in enumerate(slides_content):
        # Category Tag
        story.append(Paragraph(f"SLIDE {s_idx+1} OF 14  |  {sdata['tag']}", style_category))
        # Title
        story.append(Paragraph(sdata["title"], style_title))
        # Subtitle
        story.append(Paragraph(sdata["subtitle"], style_subtitle))

        # Render Cards Layout Table
        boxes = sdata["boxes"]
        num_boxes = len(boxes)

        table_data = []
        if num_boxes == 2:
            row = []
            for b in boxes:
                cell_content = [Paragraph(b["title"], b["hdr_style"]), Paragraph(b["body"], style_box_body)]
                row.append(cell_content)
            table_data.append(row)
            t = Table(table_data, colWidths=[350, 350])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#15203c')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
                ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
                ('PADDING', (0,0), (-1,-1), 12),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            story.append(t)
        elif num_boxes == 3:
            row = []
            for b in boxes:
                cell_content = [Paragraph(b["title"], b["hdr_style"]), Paragraph(b["body"], style_box_body)]
                row.append(cell_content)
            table_data.append(row)
            t = Table(table_data, colWidths=[230, 230, 230])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#15203c')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
                ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
                ('PADDING', (0,0), (-1,-1), 10),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            story.append(t)
        elif num_boxes == 4:
            row1 = []
            for b in boxes[:2]:
                cell_content = [Paragraph(b["title"], b["hdr_style"]), Paragraph(b["body"], style_box_body)]
                row1.append(cell_content)
            table_data.append(row1)

            row2 = []
            for b in boxes[2:]:
                cell_content = [Paragraph(b["title"], b["hdr_style"]), Paragraph(b["body"], style_box_body)]
                row2.append(cell_content)
            table_data.append(row2)

            t = Table(table_data, colWidths=[350, 350])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#15203c')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
                ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
                ('PADDING', (0,0), (-1,-1), 10),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            story.append(t)

        if s_idx < len(slides_content) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] PDF Presentation Deck Generated Successfully at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_presentation_pdf()
