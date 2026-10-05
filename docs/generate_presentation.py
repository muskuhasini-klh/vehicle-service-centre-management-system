import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_review4_presentation():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette matching Review 3 slides: Forest Green & Mint
    C_DARK = RGBColor(13, 56, 48)       # #0d3830
    C_BRAND = RGBColor(19, 78, 66)      # #134e42
    C_MINT = RGBColor(45, 212, 191)     # #2dd4bf
    C_BG = RGBColor(244, 247, 246)      # #f4f7f6
    C_CARD_BG = RGBColor(255, 255, 255) # white
    C_TEXT = RGBColor(19, 36, 32)       # dark slate
    C_MUTED = RGBColor(100, 116, 139)   # slate grey
    C_WHITE = RGBColor(255, 255, 255)
    C_LIGHT_GREEN = RGBColor(220, 252, 231)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="PBL REVIEW 4 - RESULTS & ANALYSIS"):
        # Header background banner
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.2))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_DARK
        top_bar.line.fill.background()

        # Mint accent strip
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.08))
        accent.fill.solid()
        accent.fill.fore_color.rgb = C_MINT
        accent.line.fill.background()

        # Category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.18), Inches(11.5), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_MINT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(11.5), Inches(0.6))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_DARK
    bg1.line.fill.background()

    # Title box
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
    tf1 = t_box.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "PROJECT-BASED LEARNING – REVIEW 4"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = C_MINT

    p2 = tf1.add_paragraph()
    p2.text = "Vehicle Service Centre Management System"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    p3 = tf1.add_paragraph()
    p3.text = "Final Results, Functional Working Demonstration & Performance Analysis"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(203, 213, 225)

    # Details Box (Card)
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.333), Inches(2.8))
    card1.fill.solid()
    card1.fill.fore_color.rgb = RGBColor(19, 78, 66)
    card1.line.color.rgb = C_MINT

    details_box = slide1.shapes.add_textbox(Inches(1.3), Inches(4.0), Inches(10.7), Inches(2.4))
    dtf = details_box.text_frame
    dtf.word_wrap = True

    dp1 = dtf.paragraphs[0]
    dp1.text = "Project Team Members:"
    dp1.font.size = Pt(14)
    dp1.font.bold = True
    dp1.font.color.rgb = C_MINT

    dp2 = dtf.add_paragraph()
    dp2.text = "• M. Vedasri Reddy (2510030094)           • M. Hasini (2510030098)\n• G. Rishitha (2510030100)               • M. Niharika Reddy (2510030141)"
    dp2.font.size = Pt(14)
    dp2.font.color.rgb = C_WHITE

    dp3 = dtf.add_paragraph()
    dp3.text = "\nFaculty Mentor: Rafeeq Mohammed"
    dp3.font.size = Pt(14)
    dp3.font.bold = True
    dp3.font.color.rgb = C_MINT

    dp4 = dtf.add_paragraph()
    dp4.text = "Department: Department of Computer Science & Engineering | Academic Year: 2026-2027"
    dp4.font.size = Pt(13)
    dp4.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------
    # SLIDE 2: PROJECT OBJECTIVES
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Slide 2 – Project Objectives")

    objectives = [
        ("Digitize End-to-End Operations", "Eliminate traditional manual paper logs with a centralized, relational database management system for all service center tasks."),
        ("Appointment & Schedule Automation", "Enable seamless booking, status tracking, and mechanic allocation to eliminate customer wait times and scheduling conflicts."),
        ("Dynamic Job & Service Tracking", "Provide real-time visibility into repair progress across four structured stages: Inspection, In-Progress, Pending Parts, and Completed."),
        ("Automated Spare Parts Inventory", "Maintain real-time component counts, track unit pricing, and trigger automated low-stock warnings when inventory hits reorder thresholds."),
        ("Accurate Billing & Tax Invoicing", "Auto-generate transparent itemized invoices summing spare parts, labor charges, and GST with instant receipt generation.")
    ]

    for i, (title, desc) in enumerate(objectives):
        top_pos = 1.6 + (i * 1.08)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.92))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(240, 253, 250)
        card.line.color.rgb = RGBColor(204, 251, 241)

        tb = slide2.shapes.add_textbox(Inches(1.1), Inches(top_pos + 0.08), Inches(11.2), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{i+1}. {title}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        p_sub = tf.add_paragraph()
        p_sub.text = desc
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = C_TEXT

    # -------------------------------------------------------------
    # SLIDE 3: DEVELOPMENT APPROACH
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Slide 3 – Project Development Approach")

    phases = [
        ("Phase 1: Analysis", "Problem identification, domain research, and operational requirement gathering."),
        ("Phase 2: DB Design", "9-table relational schema, primary/foreign keys, ER modeling, and constraints."),
        ("Phase 3: Backend API", "FastAPI async REST endpoints, Pydantic validation, and SQLAlchemy ORM."),
        ("Phase 4: Frontend UI", "Responsive single-page web dashboard, modal forms, and invoice printing."),
        ("Phase 5: Testing & QA", "Automated test suite (11 test cases), latency benchmarking, and verification.")
    ]

    for i, (p_title, p_desc) in enumerate(phases):
        left_pos = 0.8 + (i * 2.4)
        box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(2.2), Inches(2.2), Inches(4.0))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BRAND if i % 2 == 0 else RGBColor(15, 118, 110)
        box.line.color.rgb = C_MINT

        tb = slide3.shapes.add_textbox(Inches(left_pos + 0.15), Inches(2.4), Inches(1.9), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"Step 0{i+1}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_MINT

        p2 = tf.add_paragraph()
        p2.text = p_title
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE

        p3 = tf.add_paragraph()
        p3.text = f"\n{p_desc}"
        p3.font.size = Pt(11)
        p3.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------
    # SLIDE 4: PROJECT IMPLEMENTATION
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Slide 4 – Project Implementation Technologies")

    tech_stacks = [
        ("Frontend Layer", "HTML5, CSS3, Modern JavaScript (ES6+)", "Responsive Single Page Application with tabbed views, KPI statistics cards, interactive booking modals, and CSS print-optimized invoices."),
        ("Backend Layer", "Python 3.11, FastAPI, Uvicorn, Pydantic", "High-performance asynchronous REST API handling data serialization, input validation, authentication, and HTTP request routing."),
        ("Database Layer", "PostgreSQL (Primary) & SQLite (Fallback)", "9 normalized relational tables, ER constraints, foreign keys with ON DELETE CASCADE, and dual-engine auto-connection resilience."),
        ("APIs & Documentation", "RESTful Architecture & OpenAPI / Swagger", "Standardized REST endpoints for CRUD operations across all entities with interactive Swagger UI testing at /docs."),
        ("Development Environment", "Visual Studio Code, Git, Windows 11", "Equipped with Python virtual environments, PowerShell scripting, and automated test runners.")
    ]

    for i, (layer, tools, detail) in enumerate(tech_stacks):
        top_pos = 1.6 + (i * 1.08)
        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.95))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(248, 250, 252)
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide4.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.08), Inches(11.3), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"• {layer}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        run_tools = p.add_run()
        run_tools.text = tools
        run_tools.font.bold = True
        run_tools.font.color.rgb = RGBColor(13, 148, 136)

        p_det = tf.add_paragraph()
        p_det.text = detail
        p_det.font.size = Pt(11)
        p_det.font.color.rgb = C_TEXT

    # -------------------------------------------------------------
    # SLIDE 5: SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Slide 5 – System Architecture Diagram")

    arch_steps = [
        ("User / Client", "Customer, Technician, or Workshop Manager via Web Browser"),
        ("Frontend UI", "HTML5/CSS3 Dashboard + Async Fetch API"),
        ("FastAPI Backend", "Pydantic Validation, Routing & Business Logic"),
        ("Database Engine", "PostgreSQL / SQLite with 9 Relational Tables"),
        ("Response Delivery", "JSON Serialization, Live Metrics & Printable PDF")
    ]

    for i, (title, sub) in enumerate(arch_steps):
        left_pos = 0.8 + (i * 2.45)
        box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(2.5), Inches(2.2), Inches(3.2))
        box.fill.solid()
        box.fill.fore_color.rgb = C_BRAND
        box.line.color.rgb = C_MINT

        tb = slide5.shapes.add_textbox(Inches(left_pos + 0.1), Inches(2.8), Inches(2.0), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"Tier 0{i+1}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_MINT

        p2 = tf.add_paragraph()
        p2.text = f"\n{title}"
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE

        p3 = tf.add_paragraph()
        p3.text = f"\n{sub}"
        p3.font.size = Pt(11)
        p3.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------
    # SLIDE 6: SCREENS / WORKING DEMONSTRATION
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Slide 6 – Working Application Screens")

    screens = [
        ("1. Login & Auth Portal", "Role-based authentication for system administrators, service technicians, and registered vehicle owners with session token generation."),
        ("2. Operations Dashboard", "Real-time summary counters: registered customers, active repair jobs, revenue earned, and automated low-stock inventory alerts."),
        ("3. Service Booking Form", "Interactive modal allowing customer selection, vehicle registration mapping, desired service package, date, and technician assignment."),
        ("4. Service Job Tracking", "Job card tracking system displaying inspection notes, repair details, technician status, and completion timeline."),
        ("5. Spare Parts Inventory", "Component catalog tracking unit price, current in-stock counts, and visual indicators for items reaching reorder thresholds."),
        ("6. Tax Invoice & Results", "Automated billing calculator generating itemized invoices summing spare parts, labor, and GST with 1-click printable receipt.")
    ]

    for i, (title, desc) in enumerate(screens):
        row = i // 3
        col = i % 3
        left = 0.8 + (col * 3.95)
        top = 1.8 + (row * 2.6)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(3.7), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(240, 253, 250)
        card.line.color.rgb = C_BRAND

        tb = slide6.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(3.4), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        p2 = tf.add_paragraph()
        p2.text = f"\n{desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT

    # -------------------------------------------------------------
    # SLIDE 7: FUNCTIONAL RESULTS
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Slide 7 – Functional Results & Capabilities")

    features = [
        ("User Registration & Login", "Customers can sign up and login; supervisors authenticate to manage workshops and track multi-bay capacity."),
        ("Full CRUD Operations", "Add, read, update, and delete records across all 9 relational entities (customers, vehicles, appointments, parts, bills)."),
        ("Live Search & Filtering", "Dynamic real-time table filtering by customer name, registration number, and appointment status without page reload."),
        ("API Communication", "Asynchronous HTTP communication with JSON serialization and HTTP error status validation (200, 201, 400, 404)."),
        ("Database Relational Integrity", "Enforces foreign keys, unique constraints (emails & license plates), and cascading deletions across relational tables."),
        ("Automated Report Generation", "Instant generation of itemized tax receipts and printable job records with labor charges, parts costs, and GST.")
    ]

    for i, (title, desc) in enumerate(features):
        top_pos = 1.6 + (i * 0.92)
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.82))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(248, 250, 252)
        card.line.color.rgb = RGBColor(203, 213, 225)

        tb = slide7.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.05), Inches(11.3), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"✔ {title}: "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT

    # -------------------------------------------------------------
    # SLIDE 8: TESTING RESULTS TABLE
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Slide 8 – Testing Results & Verification")

    rows = 12
    cols = 4
    table_shape = slide8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    table = table_shape.table
    table.columns[0].width = Inches(3.6)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.5)
    table.columns[3].width = Inches(1.633)

    headers = ["Test Case", "Expected Result", "Actual Result", "Status"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_DARK
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.alignment = PP_ALIGN.CENTER if j == 3 else PP_ALIGN.LEFT

    test_data = [
        ("System Health API", "Correct response (Status 200)", "Correct response (200 OK)", "Pass"),
        ("User Login Authentication", "Successful login & token", "Successful login (Token returned)", "Pass"),
        ("Add Record (Customer)", "Record added (Status 201)", "Record added with ID", "Pass"),
        ("Add Record (Vehicle)", "Record added with FK constraint", "Record added and linked", "Pass"),
        ("Add Record (Appointment)", "Appointment created & job started", "Record added & job card started", "Pass"),
        ("Update Record (Appointment)", "Status updated to Confirmed", "Status updated successfully", "Pass"),
        ("Update Record (Service Record)", "Status updated to Completed", "Service record updated", "Pass"),
        ("Add Record (Spare Part)", "Inventory item added", "Part added to database", "Pass"),
        ("Delete Record (Spare Part)", "Record removed successfully", "Part deleted (200 OK)", "Pass"),
        ("Analytics / Dashboard API", "Summary metrics dictionary", "Correct response with KPIs", "Pass"),
        ("Invoice Generation API", "Itemized invoice & calculations", "Correct response & breakdown", "Pass"),
    ]

    for i, row in enumerate(test_data):
        for j in range(4):
            cell = table.cell(i + 1, j)
            cell.text = row[j]
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if i % 2 == 0 else C_WHITE
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                if j == 3:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(16, 185, 129)
                    p.alignment = PP_ALIGN.CENTER
                else:
                    p.font.color.rgb = C_TEXT

    # -------------------------------------------------------------
    # SLIDE 9: PERFORMANCE ANALYSIS
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Slide 9 – Performance Analysis & Metrics")

    metrics = [
        ("Average Response Time", "45.28 ms", "Measured across all asynchronous REST endpoints under concurrent test load."),
        ("Number of Test Cases", "11 Test Cases", "Full test coverage including authentication, CRUD operations, and reporting."),
        ("Successful Test Cases", "11 / 11 (100%)", "All executed test cases passed with expected status codes and valid schemas."),
        ("System Error Rate", "0.0% Error Rate", "Zero unhandled exceptions or transaction rollbacks during end-to-end execution."),
        ("Database Response Time", "< 5.0 ms", "Sub-millisecond query execution enabled by indexed primary and foreign keys."),
        ("Throughput Engine", "FastAPI + Uvicorn", "High-throughput asynchronous ASGI server with non-blocking I/O event loops.")
    ]

    for i, (label, val, desc) in enumerate(metrics):
        row = i // 3
        col = i % 3
        left = 0.8 + (col * 3.95)
        top = 1.8 + (row * 2.6)

        card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(3.7), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(248, 250, 252)
        card.line.color.rgb = C_BRAND

        tb = slide9.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(3.4), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = label.upper()
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_MUTED

        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = C_BRAND

        p3 = tf.add_paragraph()
        p3.text = f"\n{desc}"
        p3.font.size = Pt(11)
        p3.font.color.rgb = C_TEXT

    # -------------------------------------------------------------
    # SLIDE 10: RESULTS & ANALYSIS SUMMARY
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Slide 10 – Results & Impact Analysis")

    results = [
        ("100% Digital Workflow", "Replaced slow, error-prone paper job cards with instantaneous digital records accessible across all workshop terminals."),
        ("Zero Scheduling Overlaps", "Automated appointment validation prevents double-booking vehicles or technicians during service bays."),
        ("Proactive Inventory Alerts", "Real-time reorder thresholds ensure essential lubricants and filters are replenished before inventory reaches zero."),
        ("Accurate Financial Accounting", "Eliminated calculation discrepancies in parts, labor, and GST, ensuring total transparency on customer invoices."),
        ("Exceptional Performance", "Under 50ms average latency guarantees a snappy, responsive experience for front-desk staff and service advisors.")
    ]

    for i, (title, desc) in enumerate(results):
        top_pos = 1.6 + (i * 1.08)
        card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.92))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(240, 253, 250)
        card.line.color.rgb = RGBColor(204, 251, 241)

        tb = slide10.shapes.add_textbox(Inches(1.1), Inches(top_pos + 0.08), Inches(11.2), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"✔ {title}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        p_sub = tf.add_paragraph()
        p_sub.text = desc
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = C_TEXT

    # -------------------------------------------------------------
    # SLIDE 11: CONCLUSION & FUTURE SCOPE
    # -------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Slide 11 – Conclusion & Future Scope")

    # Left: Conclusion
    c_card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = RGBColor(240, 253, 250)
    c_card.line.color.rgb = C_BRAND

    c_tb = slide11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    c_tf = c_tb.text_frame
    c_tf.word_wrap = True
    cp1 = c_tf.paragraphs[0]
    cp1.text = "Conclusion"
    cp1.font.size = Pt(20)
    cp1.font.bold = True
    cp1.font.color.rgb = C_DARK

    cp2 = c_tf.add_paragraph()
    cp2.text = (
        "\n• Project Objectives Achieved:\n"
        "  - The Vehicle Service Centre Management System successfully integrates database engineering with a modern, high-performance web dashboard.\n\n"
        "• Core Accomplishments:\n"
        "  - Complete 9-table normalized relational schema.\n"
        "  - High-throughput asynchronous FastAPI backend.\n"
        "  - Full CRUD operations with 100% test pass rate.\n"
        "  - Dual-engine resilience (PostgreSQL + SQLite).\n"
        "  - Zero-latency automated invoice generation."
    )
    cp2.font.size = Pt(12)
    cp2.font.color.rgb = C_TEXT

    # Right: Future Scope
    f_card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    f_card.fill.solid()
    f_card.fill.fore_color.rgb = RGBColor(248, 250, 252)
    f_card.line.color.rgb = RGBColor(14, 116, 144)

    f_tb = slide11.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    f_tf = f_tb.text_frame
    f_tf.word_wrap = True
    fp1 = f_tf.paragraphs[0]
    fp1.text = "Future Scope"
    fp1.font.size = Pt(20)
    fp1.font.bold = True
    fp1.font.color.rgb = RGBColor(14, 116, 144)

    fp2 = f_tf.add_paragraph()
    fp2.text = (
        "\n• Future Enhancements Planned:\n"
        "  1. Cloud Deployment:\n"
        "     - Containerize with Docker and deploy on AWS / Render.\n\n"
        "  2. Customer Mobile App:\n"
        "     - Build a cross-platform Flutter/React Native application.\n\n"
        "  3. SMS & WhatsApp Notifications:\n"
        "     - Integrate Twilio to send live repair milestones to owners.\n\n"
        "  4. Telemetry & Unstructured Logs:\n"
        "     - Add MongoDB for storing OBD-II sensor diagnostic logs.\n\n"
        "  5. Online Payment Gateway:\n"
        "     - Integrate Razorpay / Stripe for instant online settlements."
    )
    fp2.font.size = Pt(12)
    fp2.font.color.rgb = C_TEXT

    # Save output
    output_path = Path(__file__).resolve().parent / "Vehicle_Service_Centre_Review_4.pptx"
    prs.save(str(output_path))
    print(f"--> PowerPoint Presentation saved at: {output_path}")

if __name__ == "__main__":
    create_review4_presentation()
