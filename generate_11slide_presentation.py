import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, TableStyle
from reportlab.pdfgen import canvas

# --- 1. SLIDE DATA FOR 11 SLIDES ---
slides_11_data = [
    # SLIDE 1
    {
        "tag": "36-HOUR COLLEGE HACKATHON BUILD",
        "title": "PahadRakshak (पहाड़ रक्षक)",
        "subtitle": "Next-Gen AI Mountain Disaster Navigation & Emergency Response System for Uttarakhand Highways",
        "boxes": [
            {"title": "Institution & Team", "text": "Swami Rama Himalayan University (SRHU) — 6 BCA 1st-Year Freshers Team.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')},
            {"title": "36-Hour Build Story", "text": "Architected & built inside college campus in 36 hours using Google Antigravity AI + Rapid Team Testing.", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')},
            {"title": "Target Region", "text": "All 13 Mountain Districts of Uttarakhand (Char Dham Highway Corridors).", "color": RGBColor(56, 189, 248), "pdf_color": colors.HexColor('#38bdf8')}
        ]
    },
    # SLIDE 2
    {
        "tag": "PROBLEM STATEMENT",
        "title": "The Himalayan Mountain Disaster Crisis",
        "subtitle": "Why Standard Commercial Apps Fail During Landslides & Cloudbursts",
        "boxes": [
            {"title": "🔴 Frequent Landslides & Cloudbursts", "text": "Heavy monsoons trigger slope failures on NH-07 (Badrinath) and NH-109 (Kedarnath), stranding thousands of travelers.", "color": RGBColor(248, 113, 113), "pdf_color": colors.HexColor('#f87171')},
            {"title": "🛑 Blind Commercial Navigation", "text": "Google Maps relies on passive traffic slowing and blindly routes vehicles into active landslide debris without hazard alerts.", "color": RGBColor(248, 113, 113), "pdf_color": colors.HexColor('#f87171')},
            {"title": "⏳ Delayed Emergency Triage", "text": "Distress calls lack hardware GPS coordinates and verified photos, delaying SDRF, NDRF, and BRO heavy machinery dispatch.", "color": RGBColor(248, 113, 113), "pdf_color": colors.HexColor('#f87171')},
            {"title": "📢 Rumors & Ghost Blockages", "text": "Unverified social media rumors cause panic, while solved road clearance updates take hours to reach travelers on the road.", "color": RGBColor(248, 113, 113), "pdf_color": colors.HexColor('#f87171')}
        ]
    },
    # SLIDE 3
    {
        "tag": "OUR SOLUTION",
        "title": "PahadRakshak: Intelligent Disaster Ecosystem",
        "subtitle": "Autonomous Safety, Live Bulletin Ingestion & Smart Navigation",
        "boxes": [
            {"title": "🔀 Conditional Dual-Route Bypass", "text": "Renders 1 clean blue line when safe; 2 distinct paths (Red Unsafe vs Green Safe Bypass) ONLY when primary route is blocked.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')},
            {"title": "🏛️ Live Government Bulletin Sync", "text": "Scans and ingests live bulletins directly from UKSDMA, IMD Dehradun, BRO Shivalik, and Police PCR with 1-click source proof links.", "color": RGBColor(56, 189, 248), "pdf_color": colors.HexColor('#38bdf8')},
            {"title": "🛡️ Dual-Portal Architecture", "text": "Frictionless Public Citizen Portal for travelers + Secured Authority Command Center with Officer ID (`UKSDMA-OFFICER-01`).", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')}
        ]
    },
    # SLIDE 4
    {
        "tag": "SYSTEM ARCHITECTURE",
        "title": "End-to-End Data Pipeline & AI GIS Engine",
        "subtitle": "High-Performance Data Flow & Geo-Spatial Calculation Engine",
        "boxes": [
            {"title": "1. Data Ingestion", "text": "Citizen SOS + Hardware GPS + Live Web Crawlers (UKSDMA / IMD / BRO / Police).", "color": RGBColor(56, 189, 248), "pdf_color": colors.HexColor('#38bdf8')},
            {"title": "2. AI Risk Calculator", "text": "Multi-Factor Risk Score Engine (0-100) + Spatial Clustering + Duplicate Detector.", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')},
            {"title": "3. FastAPI Backend", "text": "Python FastAPI + SQLite/PostgreSQL + ResolutionChecker Background Feeder.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')},
            {"title": "4. Interactive Clients", "text": "Leaflet.js GIS Map + OSRM Driving Engine + Progressive Web App (PWA).", "color": RGBColor(248, 113, 113), "pdf_color": colors.HexColor('#f87171')}
        ]
    },
    # SLIDE 5
    {
        "tag": "ROLE SEGMENTATION",
        "title": "Dual-Portal Ecosystem Architecture",
        "subtitle": "Frictionless Public Portal vs Secured Control Room Command",
        "boxes": [
            {"title": "👥 Public Citizen Portal", "text": "No login required. Features 1-tap SOS reporting, verified photo upload, 1-tap emergency helplines (112, 1070, 1077, 108, BRO), relief shelter finder, and weather warnings.", "color": RGBColor(56, 189, 248), "pdf_color": colors.HexColor('#38bdf8')},
            {"title": "🛡️ Authority Command Center", "text": "Secured by Officer Badge Verification (`UKSDMA-OFFICER-01`). Broadcasts disaster bulletins, manages AI priority queue, dispatches rescue teams (SDRF, NDRF, BRO).", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')}
        ]
    },
    # SLIDE 6
    {
        "tag": "AI RISK ENGINE",
        "title": "Multi-Factor AI Risk Engine (0-100)",
        "subtitle": "Deterministic Multi-Variable Risk Formula",
        "boxes": [
            {"title": "🧮 Risk Score Formula", "text": "Risk Score = (Severity * 0.25) + (Rainfall * 0.20) + (History * 0.15) + (Road Blocked * 0.15) + (Affected People * 0.15) + (Density * 0.10)", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')},
            {"title": "🔴 CRITICAL (80-100)", "text": "Cloudburst, complete road blockage, life threat. Prompts immediate green bypass routing.", "color": RGBColor(248, 113, 113), "pdf_color": colors.HexColor('#f87171')},
            {"title": "🟠 HIGH (60-79)", "text": "Landslide debris, highway obstruction. Renders Route B safe bypass.", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')},
            {"title": "🟢 MODERATE / LOW (0-59)", "text": "Minimal road movement affected. Confirms road safe for single-line traffic.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')}
        ]
    },
    # SLIDE 7
    {
        "tag": "SMART ROUTING",
        "title": "Conditional Dual-Route Bypass System",
        "subtitle": "Smart Geometry Rendering for Mountain Highways",
        "boxes": [
            {"title": "✅ Primary Highway Safe Scenario", "text": "When no road blockages exist along the highway, the map renders 1 single clean glowing blue line without screen clutter.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')},
            {"title": "🔀 Primary Highway Unsafe Scenario", "text": "When a blockage is detected, the engine renders 2 paths: Route A (Red Dashed Unsafe) vs Route B (Green Glowing Safe Bypass).", "color": RGBColor(248, 113, 113), "pdf_color": colors.HexColor('#f87171')}
        ]
    },
    # SLIDE 8
    {
        "tag": "GOVT SYNC & CLEARANCE",
        "title": "Live Government Bulletin Sync & Auto-Clearance",
        "subtitle": "Official Ingestion & Zero Ghost Markers Policy",
        "boxes": [
            {"title": "🏛️ Live Government Bulletin Sync", "text": "Direct REST crawlers syncing UKSDMA, IMD Dehradun, BRO Shivalik, and Police PCR updates with 1-click source verification links.", "color": RGBColor(56, 189, 248), "pdf_color": colors.HexColor('#38bdf8')},
            {"title": "🧹 Auto-Clearance Map Purging", "text": "ResolutionCheckerService scans BRO clearance logs and purges resolved road blockages from live maps automatically.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')}
        ]
    },
    # SLIDE 9
    {
        "tag": "LIVE WEATHER BROADCAST",
        "title": "IMD Weather Broadcasting & User Location Weather",
        "subtitle": "Exact GPS Location Weather & Statewide IMD Radar Layer",
        "boxes": [
            {"title": "📍 User Location Weather Card", "text": "'THIS IS YOUR LOCATION & THIS IS THE WEATHER IN YOUR AREA' — Live temperature, rain mm, wind speed, humidity for exact GPS position.", "color": RGBColor(56, 189, 248), "pdf_color": colors.HexColor('#38bdf8')},
            {"title": "🌤️ Statewide IMD Radar Layer", "text": "Precipitation Doppler circles & rainfall mm badges across Chamoli, Uttarkashi, Rudraprayag, Dehradun, and Nainital.", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')}
        ]
    },
    # SLIDE 10
    {
        "tag": "36-HOUR TEAM WORKFLOW",
        "title": "36-Hour College Hackathon Team & Roles",
        "subtitle": "How 6 BCA Freshers Worked Together Inside College Campus",
        "boxes": [
            {"title": "💻 1 AI Developer (Team Lead)", "text": "Directed Google Antigravity AI, architected FastAPI backend, database schemas, and dual routing math.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')},
            {"title": "🔍 5 QA, Data & Testing Teammates", "text": "Conducted Uttarakhand disaster data gathering, verified helplines, tested hardware GPS over HTTPS, and hunted UI bugs across campus.", "color": RGBColor(251, 191, 36), "pdf_color": colors.HexColor('#fbbf24')}
        ]
    },
    # SLIDE 11
    {
        "tag": "LIVE DEMO & CONCLUSION",
        "title": "PahadRakshak: Saving Lives in the Himalayas",
        "subtitle": "Tested & Fully Working Prototype Built in 36 Hours",
        "boxes": [
            {"title": "🌐 Live System Demo Endpoints", "text": "Landing Portal (8000/app/index.html) | Public Portal (citizen.html) | Command Center (dashboard.html) | Mobile GPS (8443/app/map.html).", "color": RGBColor(56, 189, 248), "pdf_color": colors.HexColor('#38bdf8')},
            {"title": "🏆 Team Mission & Vision", "text": "Built by 6 BCA Freshers at SRHU Dehradun for TechForge 3.0 & SIH 2026 to safeguard mountain travelers across Uttarakhand.", "color": RGBColor(52, 211, 153), "pdf_color": colors.HexColor('#34d399')}
        ]
    }
]

# --- 2. GENERATE NATIVE POWERPOINT (.PPTX) ---
def generate_pptx(output_pptx_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    DARK_BG = RGBColor(11, 19, 41)       # #0b1329
    CARD_BG = RGBColor(21, 32, 60)       # #15203c
    BORDER_CLR = RGBColor(30, 58, 138)   # #1e3a8a
    WHITE = RGBColor(255, 255, 255)
    CYAN = RGBColor(56, 189, 248)
    GRAY = RGBColor(148, 163, 184)

    for slide_idx, sdata in enumerate(slides_11_data):
        slide = prs.slides.add_slide(blank_layout)

        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()

        # Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        p = tag_box.text_frame.paragraphs[0]
        p.text = f"SLIDE {slide_idx+1} OF 11  |  {sdata['tag']}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        p_t = title_box.text_frame.paragraphs[0]
        p_t.text = sdata["title"]
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5))
        p_s = sub_box.text_frame.paragraphs[0]
        p_s.text = sdata["subtitle"]
        p_s.font.size = Pt(14)
        p_s.font.color.rgb = GRAY

        # Cards Layout
        boxes = sdata["boxes"]
        num_boxes = len(boxes)

        if num_boxes == 2:
            box_w, box_h = Inches(5.6), Inches(4.8)
            positions = [(Inches(0.8), Inches(2.1)), (Inches(6.8), Inches(2.1))]
        elif num_boxes == 3:
            box_w, box_h = Inches(3.6), Inches(4.8)
            positions = [(Inches(0.8), Inches(2.1)), (Inches(4.85), Inches(2.1)), (Inches(8.9), Inches(2.1))]
        elif num_boxes == 4:
            box_w, box_h = Inches(5.6), Inches(2.25)
            positions = [
                (Inches(0.8), Inches(2.1)), (Inches(6.8), Inches(2.1)),
                (Inches(0.8), Inches(4.65)), (Inches(6.8), Inches(4.65))
            ]
        else:
            box_w, box_h = Inches(11.7), Inches(4.8)
            positions = [(Inches(0.8), Inches(2.1))]

        for b_idx, binfo in enumerate(boxes):
            px, py = positions[b_idx]
            card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, py, box_w, box_h)
            card.fill.solid()
            card.fill.fore_color.rgb = CARD_BG
            card.line.color.rgb = BORDER_CLR
            card.line.width = Pt(1.5)

            tb_h = slide.shapes.add_textbox(px + Inches(0.2), py + Inches(0.2), box_w - Inches(0.4), Inches(0.6))
            ph = tb_h.text_frame.paragraphs[0]
            ph.text = binfo["title"]
            ph.font.size = Pt(16)
            ph.font.bold = True
            ph.font.color.rgb = binfo["color"]

            tb_b = slide.shapes.add_textbox(px + Inches(0.2), py + Inches(0.8), box_w - Inches(0.4), box_h - Inches(1.0))
            tb_b.text_frame.word_wrap = True
            pb = tb_b.text_frame.paragraphs[0]
            pb.text = binfo["text"]
            pb.font.size = Pt(12)
            pb.font.color.rgb = WHITE

        # Footer
        ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.3))
        pf = ft_box.text_frame.paragraphs[0]
        pf.text = "PahadRakshak 11-Slide Deck  |  Built in 36 Hours at SRHU by 6 BCA Freshers using Google Antigravity AI"
        pf.font.size = Pt(10)
        pf.font.color.rgb = GRAY

    prs.save(output_pptx_path)
    print(f"[+] 11-Slide PPTX Created: {output_pptx_path}")

# --- 3. GENERATE PRINTABLE PDF ---
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.setFillColor(colors.HexColor('#0b1329'))
        self.rect(0, 0, 792, 612, fill=True, stroke=False)

        self.setStrokeColor(colors.HexColor('#1e3a8a'))
        self.setLineWidth(1)
        self.line(40, 565, 752, 565)
        self.line(40, 45, 752, 45)

        self.setFillColor(colors.HexColor('#94a3b8'))
        self.setFont("Helvetica", 9)
        self.drawString(40, 30, "PahadRakshak 11-Slide Deck  |  Swami Rama Himalayan University (SRHU) 6 BCA Freshers")
        self.drawRightString(752, 30, f"Slide {self._pageNumber} of {page_count}")

def generate_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    styles = getSampleStyleSheet()

    style_category = ParagraphStyle('CatTag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#38bdf8'), spaceAfter=4)
    style_title = ParagraphStyle('SlideT', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=colors.HexColor('#ffffff'), spaceAfter=6)
    style_subtitle = ParagraphStyle('SlideSub', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=16, textColor=colors.HexColor('#94a3b8'), spaceAfter=15)
    style_box_body = ParagraphStyle('BoxB', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#e2e8f0'))

    story = []

    for s_idx, sdata in enumerate(slides_11_data):
        story.append(Paragraph(f"SLIDE {s_idx+1} OF 11  |  {sdata['tag']}", style_category))
        story.append(Paragraph(sdata["title"], style_title))
        story.append(Paragraph(sdata["subtitle"], style_subtitle))

        boxes = sdata["boxes"]
        num_boxes = len(boxes)
        table_data = []

        if num_boxes == 2:
            row = []
            for b in boxes:
                st_hdr = ParagraphStyle('BH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=b["pdf_color"], spaceAfter=4)
                row.append([Paragraph(b["title"], st_hdr), Paragraph(b["text"], style_box_body)])
            table_data.append(row)
            t = Table(table_data, colWidths=[350, 350])
        elif num_boxes == 3:
            row = []
            for b in boxes:
                st_hdr = ParagraphStyle('BH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=b["pdf_color"], spaceAfter=4)
                row.append([Paragraph(b["title"], st_hdr), Paragraph(b["text"], style_box_body)])
            table_data.append(row)
            t = Table(table_data, colWidths=[230, 230, 230])
        elif num_boxes == 4:
            row1, row2 = [], []
            for b in boxes[:2]:
                st_hdr = ParagraphStyle('BH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=b["pdf_color"], spaceAfter=4)
                row1.append([Paragraph(b["title"], st_hdr), Paragraph(b["text"], style_box_body)])
            for b in boxes[2:]:
                st_hdr = ParagraphStyle('BH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=b["pdf_color"], spaceAfter=4)
                row2.append([Paragraph(b["title"], st_hdr), Paragraph(b["text"], style_box_body)])
            table_data = [row1, row2]
            t = Table(table_data, colWidths=[350, 350])
        else:
            row = []
            for b in boxes:
                st_hdr = ParagraphStyle('BH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=b["pdf_color"], spaceAfter=4)
                row.append([Paragraph(b["title"], st_hdr), Paragraph(b["text"], style_box_body)])
            table_data.append(row)
            t = Table(table_data, colWidths=[700])

        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#15203c')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#1e3a8a')),
            ('PADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t)

        if s_idx < len(slides_11_data) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] 11-Slide PDF Created: {output_pdf_path}")

if __name__ == "__main__":
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend"))
    os.makedirs(frontend_dir, exist_ok=True)
    
    pptx_path = os.path.join(frontend_dir, "PahadRakshak_11Slide_Presentation.pptx")
    pdf_path = os.path.join(frontend_dir, "PahadRakshak_11Slide_Presentation.pdf")
    
    generate_pptx(pptx_path)
    generate_pdf(pdf_path)
