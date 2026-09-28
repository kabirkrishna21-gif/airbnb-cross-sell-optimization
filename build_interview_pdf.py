# build_interview_pdf.py
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
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
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        if self._pageNumber > 1:
            # Header
            self.drawString(54, letter[1] - 36, "AIRBNB STAYS-TO-EXPERIENCES CROSS-SELL | PRODUCT ANALYST INTERVIEW DOSSIER")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.6)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
            # Footer
            self.setFont("Helvetica", 8)
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 34, page_text)
            self.drawString(54, 34, "CONFIDENTIAL & PROPRIETARY | PREPARED FOR PRODUCT ANALYST INTERVIEWS")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.6)
            self.line(54, 46, letter[0] - 54, 46)
            
        self.restoreState()

def create_callout(text, style, title="PRO-TIP / INTERVIEW TAKEAWAY", border_color="#FF5A5F", bg_color="#FFF5F5", width=504):
    content = [
        Paragraph(f"<b><font color='{border_color}'>{title}</font></b>", style['CalloutTitle']),
        Spacer(1, 4),
        Paragraph(text, style['CalloutBody'])
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor(border_color)),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    return t

def create_code_block(code_text, style, width=504):
    clean_text = code_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>").replace(" ", "&nbsp;")
    p = Paragraph(f"<font face='Courier' size=7.5 color='#1A202C'>{clean_text}</font>", style['CodeText'])
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def generate_pdf():
    output_pdf = os.path.join(os.path.dirname(__file__), "Airbnb_Cross_Sell_Interview_Guide.pdf")
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Palette
    c_primary = colors.HexColor("#1A365D")   # Deep Corporate Navy
    c_accent = colors.HexColor("#FF5A5F")    # Airbnb Rausch Crimson
    c_text = colors.HexColor("#2D3748")      # Dark Slate Body
    c_muted = colors.HexColor("#718096")     # Muted Grey
    
    styles.add(ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=c_primary))
    styles.add(ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=16, textColor=c_muted))
    styles.add(ParagraphStyle('SectionH1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=c_primary, keepWithNext=True))
    styles.add(ParagraphStyle('SectionH2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=c_accent, keepWithNext=True))
    styles.add(ParagraphStyle('CustomBody', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=c_text))
    styles.add(ParagraphStyle('CustomBodyBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=13.5, textColor=c_text))
    styles.add(ParagraphStyle('BulletText', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=c_text))
    styles.add(ParagraphStyle('TableText', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=c_text))
    styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.white))
    styles.add(ParagraphStyle('CalloutTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=c_accent))
    styles.add(ParagraphStyle('CalloutBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_text))
    styles.add(ParagraphStyle('CodeText', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor("#1A202C")))
    styles.add(ParagraphStyle('QTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=c_primary, keepWithNext=True))
    styles.add(ParagraphStyle('QAnswer', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=c_text))

    story = []

    # =========================================================================
    # COVER / HEADER BANNER
    # =========================================================================
    story.append(Paragraph("Cross-Sell Conversion Optimization", styles['DocTitle']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A/B Experimentation & Funnel Diagnostics: Airbnb Stays to Experiences", styles['DocSubtitle']))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2.5, color=c_accent, spaceBefore=4, spaceAfter=10))
    
    # Metadata Pill Box
    meta_data = [
        [
            Paragraph("<b>Target Role:</b> Product Analyst / Growth Analyst", styles['TableText']),
            Paragraph("<b>Domain:</b> Consumer Tech / Travel & Hospitality", styles['TableText']),
        ],
        [
            Paragraph("<b>Primary Methodology:</b> A/B Testing & Funnel Attribution", styles['TableText']),
            Paragraph("<b>Key Tools:</b> SQL, Python (Pandas/Plotly), Z-test, Deep-Linking", styles['TableText']),
        ]
    ]
    t_meta = Table(meta_data, colWidths=[252, 252])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 1: EXECUTIVE BRIEF & ELEVATOR PITCHES
    # =========================================================================
    story.append(Paragraph("1. Executive Brief & Interview Pitches", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("<b>The 30-Second Elevator Pitch:</b>", styles['SectionH2']))
    story.append(Paragraph(
        "\"At Airbnb, I optimized the cross-sell conversion funnel from core lodging reservations (Stays) to our high-margin activities vertical (Experiences). "
        "By analyzing clickstream cohorts in SQL, I discovered that <b>78% of guests bounced</b> on the Experiences landing page due to 'context loss'—they were forced to re-enter trip dates and destination details they had already confirmed. "
        "I designed and analyzed a 14-day A/B test introducing <b>Context-Preserved Dynamic Deep-Linking</b> across 60,000+ users. "
        "This eliminated search friction, resulting in a <b>56.8% relative lift in click-to-booking conversion</b> (from 3.20% to 5.02%, p &lt; 0.01) and scaled weekly cross-sell booking revenue by <b>3.5x</b>.\"",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>The 2-Minute Structured Pitch (STAR Framework):</b>", styles['SectionH2']))
    star_points = [
        "<b>Situation:</b> Airbnb Stays is a high-volume, mature lodging product, while Experiences represents a higher-margin, under-penetrated growth vertical. While marketing cards on trip itinerary pages generated a strong 12% Click-Through Rate (CTR), booking conversion remained stagnant at 3.2%, representing a critical drop-off in user monetization.",
        "<b>Task:</b> As the Product Analyst, my responsibility was to audit the end-to-end user funnel, isolate where and why users dropped off, quantify the business impact, and design an A/B experimentation roadmap to lift multi-product cross-selling.",
        "<b>Action:</b> I joined lodging reservation logs with downstream clickstream and checkout tables using SQL window functions. I identified an acute friction point: clicking the banner routed guests to a generic search page, requiring manual date and city re-entry. In response, I proposed 'Context-Preserved Dynamic Deep-Linking,' which packaged trip metadata into URL query parameters. I defined primary, secondary, and guardrail metrics, calculated sample sizes for statistical power, and monitored a 14-day randomized controlled trial.",
        "<b>Result:</b> The variant drove an absolute conversion increase of +1.82% (from 3.20% to 5.02%, p &lt; 0.01), sliced landing page bounce rates by 44.9% (78% to 43%), and cut average search-to-checkout time by 59% (from 22 minutes to 9 minutes), with zero negative impact on lodging cancellation guardrails."
    ]
    for pt in star_points:
        story.append(Paragraph(f"• {pt}", styles['BulletText']))
        story.append(Spacer(1, 3))
    
    story.append(Spacer(1, 8))
    callout_1 = create_callout(
        "<b>Interview Pro-Tip:</b> When hiring managers ask about your role, emphasize that you didn't just 'run queries'—you identified the strategic opportunity, translated behavioral analytics into a technical product specification (deep-link parameter payloads), and proved causal impact using statistical rigor.",
        styles
    )
    story.append(callout_1)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 2: BUSINESS CONTEXT & STRATEGIC IMPORTANCE
    # =========================================================================
    story.append(Paragraph("2. Strategic Business Context & Ecosystem Economics", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "To evaluate this project credibly, you must demonstrate a firm grasp of the commercial mechanics governing multi-vertical consumer marketplaces:",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 6))

    biz_points = [
        "<b>Take-Rate & Margin Differential:</b> Lodging bookings typically yield a 14-16% platform take-rate, whereas Airbnb Experiences captures a 20% host commission. Converting existing stay guests into activity bookers expands Net Revenue without incurring additional Customer Acquisition Cost (CAC = 0).",
        "<b>Intent Priming:</b> Guests with confirmed Stays are in an active travel planning state ('trip preparation window'). Their purchase intent is peak between 7 and 30 days prior to trip check-in.",
        "<b>LTV & Retention Multiplier:</b> Historical platform data indicates that multi-category users (guests who book both Stays and Experiences) exhibit a <b>34% higher 12-month repeat booking rate</b> compared to lodging-only travelers.",
        "<b>Unit Economics of the Friction:</b> Prior to the experiment, for every 100,000 banner clicks, 96,800 guests left without booking. At an Average Order Value (AOV) of $85 and a 20% take-rate, each percentage point increase in conversion generates substantial high-margin gross profit."
    ]
    for pt in biz_points:
        story.append(Paragraph(f"• {pt}", styles['BulletText']))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 12))

    # =========================================================================
    # SECTION 3: PROBLEM DISCOVERY & FUNNEL LEAK DIAGNOSTICS
    # =========================================================================
    story.append(Paragraph("3. Problem Discovery: Isolating Context Loss", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "By structuring the problem into behavioral conversion steps, the drop-off leak became mathematically obvious:",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 6))

    # Table of Baseline Funnel
    funnel_headers = ["Funnel Stage", "Users (Cohort)", "Step Conversion", "Overall Conversion", "Behavioral Leak Diagnosis"]
    funnel_rows = [
        funnel_headers,
        ["1. Confirmed Stays Itinerary View", "850,000", "100.0%", "100.0%", "High intent travelers viewing trip details"],
        ["2. Experiences Banner Clicks", "102,000", "12.0%", "12.0%", "Strong initial interest in local tours/activities"],
        ["3. Search Page Loaded (Generic)", "22,440", "22.0%", "2.64%", "<b>78% Bounce:</b> Users faced blank search inputs"],
        ["4. Checkout Initiated", "7,180", "32.0%", "0.84%", "Friction in finding matching availability"],
        ["5. Booking Completed (Success)", "3,264", "45.5%", "0.38%", "<b>Baseline Click-to-Booking: 3.20%</b>"]
    ]
    t_funnel = Table([[Paragraph(c, styles['TableHeader'] if i==0 else styles['TableText']) for c in r] for i, r in enumerate(funnel_rows)], colWidths=[120, 75, 75, 75, 159])
    t_funnel.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (1,1), (3,-1), 'CENTER'),
    ]))
    story.append(t_funnel)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Root Cause Analysis:</b> Qualitative session replays and query data revealed that users who clicked the itinerary banner were directed to the generic <code>/experiences</code> root directory. Because the user was forced to re-enter their arrival/departure dates, destination city, and guest count, cognitive load spiked, triggering an immediate bounce.",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: DATA ENGINEERING & SQL COHORTING DEEP-DIVE
    # =========================================================================
    story.append(Paragraph("4. Production SQL Funnel Query & Logic Breakdown", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "Interviewers will probe how you modeled event streams. The SQL query below tracks a 30-day cohort across disparate logging schemas using rigorous session windows:",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 6))

    sql_code = """-- Production-Grade Funnel Attribution Query
WITH confirmed_stays AS (
  SELECT 
    booking_id, guest_user_id, destination_city,
    check_in_date, check_out_date, guest_count,
    created_at AS stay_booking_time
  FROM lodging_bookings.reservations
  WHERE check_in_date BETWEEN '2026-04-01' AND '2026-04-30'
    AND status = 'CONFIRMED'
),
banner_clicks AS (
  SELECT 
    cs.guest_user_id, cs.destination_city, cs.check_in_date,
    cs.check_out_date, cs.guest_count, e.event_timestamp AS click_time
  FROM confirmed_stays cs
  JOIN clickstream.events e 
    ON cs.guest_user_id = e.user_id 
    AND e.event_timestamp BETWEEN cs.stay_booking_time 
                              AND cs.stay_booking_time + INTERVAL '7' DAY
  WHERE e.element_id = 'itinerary_experiences_cross_sell'
),
experience_searches AS (
  SELECT bc.guest_user_id, s.event_timestamp AS search_time
  FROM banner_clicks bc
  JOIN experiences.search_events s 
    ON bc.guest_user_id = s.user_id 
    AND s.event_timestamp BETWEEN bc.click_time 
                              AND bc.click_time + INTERVAL '30' MINUTE
),
checkout_initiations AS (
  SELECT es.guest_user_id, c.event_timestamp AS checkout_time
  FROM experience_searches es
  JOIN experiences.checkout_funnel c 
    ON es.guest_user_id = c.user_id 
    AND c.event_timestamp BETWEEN es.search_time 
                              AND es.search_time + INTERVAL '60' MINUTE
  WHERE c.step_name = 'initiated_checkout'
),
completed_bookings AS (
  SELECT ci.guest_user_id, t.event_timestamp AS transaction_time
  FROM checkout_initiations ci
  JOIN experiences.transactions t 
    ON ci.guest_user_id = t.user_id 
    AND t.event_timestamp BETWEEN ci.checkout_time 
                              AND ci.checkout_time + INTERVAL '30' MINUTE
  WHERE t.payment_status = 'SUCCESS'
)
SELECT 
  COUNT(DISTINCT cs.guest_user_id) AS step_1_confirmed_stays,
  COUNT(DISTINCT bc.guest_user_id) AS step_2_banner_clicks,
  COUNT(DISTINCT es.guest_user_id) AS step_3_search_page_opens,
  COUNT(DISTINCT ci.guest_user_id) AS step_4_checkout_initiated,
  COUNT(DISTINCT cb.guest_user_id) AS step_5_booking_completed,
  ROUND(COUNT(DISTINCT cb.guest_user_id)*100.0 / COUNT(DISTINCT bc.guest_user_id), 2) AS click_to_booking_pct
FROM confirmed_stays cs
LEFT JOIN banner_clicks bc ON cs.guest_user_id = bc.guest_user_id
LEFT JOIN experience_searches es ON bc.guest_user_id = es.guest_user_id
LEFT JOIN checkout_initiations ci ON es.guest_user_id = ci.guest_user_id
LEFT JOIN completed_bookings cb ON ci.guest_user_id = cb.guest_user_id;"""
    
    story.append(create_code_block(sql_code, styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Key SQL Technical Nuances to Highlight in Interviews:</b>", styles['SectionH2']))
    sql_nuances = [
        "<b>Attribution Windows:</b> Click-to-search window was capped at 30 minutes, and checkout-to-booking at 30 minutes. This prevents misattributing organic Experience browsing from days later to the banner click.",
        "<b>LEFT JOIN Hierarchy:</b> Preserved cohort attrition from Step 1 through Step 5 without discarding dropped-off users.",
        "<b>Deduplication:</b> Used <code>COUNT(DISTINCT guest_user_id)</code> instead of counting raw events to avoid inflating conversion rates due to users clicking multiple times in a single session."
    ]
    for n in sql_nuances:
        story.append(Paragraph(f"• {n}", styles['BulletText']))
        story.append(Spacer(1, 2))
    
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 5: EXPERIMENTATION DESIGN & A/B TEST FRAMEWORK
    # =========================================================================
    story.append(Paragraph("5. Experimentation Framework & Statistical Rigor", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "<b>Hypothesis:</b> Dynamically pre-populating destination geo-coordinates, dates, and party size into deep-linked Experience catalog pages will eliminate context-loss friction, increasing Click-to-Booking conversion by at least +1.2% absolute (from 3.2% to 4.4%).",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 8))

    # Experiment parameters table
    exp_headers = ["Parameter", "Design Specification", "Technical & Statistical Justification"]
    exp_rows = [
        exp_headers,
        ["Unit of Diversion", "Guest User ID (Hashed)", "Ensures consistent experience across web, iOS, and Android clients."],
        ["Control (Variant A)", "Static URL (/experiences)", "Standard promotional banner linking to unauthenticated root catalog."],
        ["Variant B", "Context-Preserved Dynamic Link", "Deep-link appending ?city=...&check_in=...&check_out=...&guests=..."],
        ["Primary Metric", "Click-to-Booking Conversion Rate", "Total distinct converting users divided by distinct banner clickers."],
        ["Secondary Metrics", "Landing Bounce Rate, Time-to-Checkout", "Diagnostic metrics to validate if reduced friction drove the primary lift."],
        ["Guardrail Metrics", "Stay Cancellation Rate, Unsubscribe Rate", "Ensures promo banner does not distract from or cannibalize lodging revenue."],
        ["Significance Level (alpha)", "0.05 (95% Confidence)", "Standard threshold to control Type I error (false positive rate)."],
        ["Statistical Power (1-beta)", "0.80 (80% Power)", "Controls Type II error (beta = 0.20), ensuring 80% chance of detecting MDE."],
        ["Min. Detectable Effect (MDE)", "1.2% Absolute Lift (37.5% Relative)", "Derived from commercial viability and traffic velocity constraints."],
        ["Sample Size Required", "~30,000 clicked users per variant", "Calculated via two-proportion Z-test formula based on baseline p=0.032."],
        ["Duration", "14 Days", "Full 2-week cycle to normalize weekday vs weekend booking variations."]
    ]
    t_exp = Table([[Paragraph(c, styles['TableHeader'] if i==0 else styles['TableText']) for c in r] for i, r in enumerate(exp_rows)], colWidths=[115, 140, 249])
    t_exp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_exp)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 6: STATISTICAL RESULTS & BUSINESS IMPACT
    # =========================================================================
    story.append(Paragraph("6. Statistical Results & Economic Impact", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    # Results Table
    res_headers = ["Funnel Metric", "Control (A)", "Variant (B)", "Absolute Delta", "Relative Lift", "Stat. Sig. (p-value)"]
    res_rows = [
        res_headers,
        ["Itinerary Banner CTR", "12.00%", "14.10%", "+2.10%", "+17.5%", "p < 0.01 (Significant)"],
        ["Landing Page Bounce Rate", "78.00%", "43.00%", "-35.00%", "-44.9%", "p < 0.01 (Significant)"],
        ["Checkout Initiation Rate", "7.04%", "15.52%", "+8.48%", "+120.5%", "p < 0.01 (Significant)"],
        ["Click-to-Booking Conversion", "3.20%", "5.02%", "+1.82%", "+56.9%", "p < 0.01 (Significant)"],
        ["Avg. Search-to-Checkout Time", "22.4 mins", "9.1 mins", "-13.3 mins", "-59.4%", "p < 0.01 (Significant)"],
        ["Lodging Cancellation Rate (Guardrail)", "1.42%", "1.41%", "-0.01%", "-0.7%", "p = 0.84 (No Harm)"]
    ]
    t_res = Table([[Paragraph(c, styles['TableHeader'] if i==0 else styles['TableText']) for c in r] for i, r in enumerate(res_rows)], colWidths=[130, 68, 68, 75, 75, 88])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Quantified Economic Return:</b>", styles['SectionH2']))
    econ_points = [
        "<b>Incremental Volume:</b> With 100,000 monthly itinerary banner clicks, lifting conversion from 3.20% to 5.02% creates <b>1,820 additional activity bookings per month</b>.",
        "<b>Gross Merchandise Value (GMV):</b> At an average ticket value of $85 per guest experience, this equates to <b>$154,700 in incremental monthly GMV</b> ($1.85M annualized).",
        "<b>Net Revenue:</b> At Airbnb's 20% experience take-rate, this single feature drives <b>~$370,000 in annualized high-margin platform profit</b> with zero customer acquisition expense."
    ]
    for ep in econ_points:
        story.append(Paragraph(f"• {ep}", styles['BulletText']))
        story.append(Spacer(1, 2))
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 7: TOP 10 INTERVIEW QUESTIONS & MODEL ANSWERS
    # =========================================================================
    story.append(Paragraph("7. Interview Battleground: Top 10 Questions & Answers", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    qa_list = [
        (
            "Q1: Why did you prioritize in-app itinerary banners instead of post-booking email or push notifications?",
            "\"While push notifications and transactional emails generate reach, their open-to-conversion rates suffer from high latency. An itinerary banner captures users in an active 'trip organization mindset' inside the session where their lodging reservation is visually fresh. Furthermore, push notifications risk notification fatigue and app uninstalls if sent too aggressively. Our strategy was to establish high-intent conversion inside the product first, before building external notification triggers.\""
        ),
        (
            "Q2: How did you test for Sample Ratio Mismatch (SRM) during the experiment?",
            "\"Sample Ratio Mismatch is a critical threat to experiment validity. Because traffic was split 50/50, I performed a Chi-Square Goodness-of-Fit test on observed user assignments daily (Control: 30,120 vs. Variant: 30,085). With a p-value of 0.88, there was no evidence of SRM (threshold p &lt; 0.001). If SRM had been detected, it would have signaled upstream diversion bugs, such as redirects breaking on older Android app builds.\""
        ),
        (
            "Q3: How did you calculate your sample size and prevent early-stopping bias?",
            "\"I used the standard two-sample proportion Z-test formula parameterized by our baseline conversion of 3.2%, an alpha of 0.05, power of 0.80, and a Minimum Detectable Effect of 1.2% absolute. This yielded ~30,000 clicked users per arm. Crucially, I locked the duration to 14 days beforehand to avoid 'peeking'—evaluating p-values continuously and stopping prematurely when significance is achieved by chance introduces massive Type I error inflation.\""
        ),
        (
            "Q4: What if a guest's booked destination had low or zero Experiences inventory?",
            "\"This was our most critical edge case. If a guest booked a secluded cabin in rural Montana where zero experiences existed within a 25km radius, pre-filtering would return an empty state ('No experiences found'), which is worse than the generic homepage. We engineered fallback logic: if local inventory was under 3 listings, the deep-link expanded the radius to 50km or fell back to regional 'Top-Rated Online Experiences' to prevent zero-result dead ends.\""
        ),
        (
            "Q5: How did you ensure this didn't cannibalize lodging revenue or cause trip cancellations?",
            "\"We set 14-day Stays Cancellation Rate and Customer Support Contact Rate as non-negotiable guardrail metrics. The hypothesis was tested with two-sided equivalence bounds. The Stays cancellation rate was 1.42% in Control and 1.41% in Variant B (p = 0.84), confirming that promoting activities on the itinerary did not distract guests or create booking confusion.\""
        ),
        (
            "Q6: How did you define and defend your attribution window?",
            "\"Attribution window selection balances capturing genuine delayed conversions against false positives from organic exploration. We implemented a 30-minute click-to-search session window and a 24-hour click-to-booking window tagged with a campaign token. If a user booked an experience 5 days later via organic search without re-clicking the banner, it was credited to organic, not the banner. This conservative attribution ensured business stakeholders trusted the reported lift.\""
        ),
        (
            "Q7: Did you observe any novelty effect, and how did you verify long-term retention?",
            "\"Novelty effects frequently inflate initial CTR when UI components change. To guard against this, we tracked week 1 vs. week 2 conversion consistency and monitored 7-day post-experience review submission rates. The conversion lift held steady (+57.2% in week 1 vs +56.5% in week 2), and post-trip review rates were identical across cohorts, proving that user experience quality was preserved post-booking.\""
        ),
        (
            "Q8: How did you collaborate across Engineering, Design, and Product teams?",
            "\"Product analytics is a leadership role without direct authority. When proposing dynamic deep-linking, engineering initially resisted due to concerns about deep-link payload failures across iOS/Android/Web. I built a Python prototype and mapped the revenue impact ($370k net profit), proving that the engineering investment had a 10x ROI. I collaborated with UX on seamless loading skeletons and with mobile engineers on URL query schemas.\""
        ),
        (
            "Q9: What statistical test did you run to determine significance for binary conversion vs. time-to-checkout?",
            "\"For binary conversion (booking completed: 1 or 0), I ran a two-sample proportion Z-test (Z = 11.4, p &lt; 0.0001). For time-to-checkout (continuous, highly skewed metric), normal distribution assumptions fail, so I ran a non-parametric Mann-Whitney U test (Wilcoxon rank-sum) to compare median search-to-checkout durations, which confirmed a statistically significant drop from 22.4 to 9.1 minutes.\""
        ),
        (
            "Q10: If given another quarter to expand this feature, what would you test next?",
            "\"Three high-leverage iterations: 1) Persona-Based Recommendation Ranking: Using the stay's guest count to filter romantic dining for couples vs. family-friendly tours for groups. 2) Temporal Cadence: Shifting banner copy from 'Book Activities' 30 days prior to 'Last Chance Tickets for This Weekend' 48 hours before check-in. 3) Cross-App Bundling: Testing a single-click checkout that bundles airport transfers directly onto the lodging invoice.\""
        )
    ]

    for q, a in qa_list:
        card = [
            Paragraph(f"<b>{q}</b>", styles['QTitle']),
            Spacer(1, 3),
            Paragraph(a, styles['QAnswer'])
        ]
        t_card = Table([[card]], colWidths=[504])
        t_card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('LINELEFT', (0,0), (-1,-1), 3, c_accent if "Q1:" in q or "Q2:" in q or "Q4:" in q else c_primary),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_card)
        story.append(Spacer(1, 7))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 8: RESUME-READY BULLETS & WHITEBOARD CHECKLIST
    # =========================================================================
    story.append(Paragraph("8. Resume Bullet Points & Whiteboard Checklist", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    cv_bullets = [
        "<b>Engineered and executed a cross-sell funnel optimization</b> from Stays to Experiences, diagnosing a 78% search-page drop-off in SQL caused by lack of destination/date context.",
        "<b>Designed and analyzed a 14-day A/B experiment (N=60,000+)</b> testing context-preserved deep-linking against a static catalog link, lifting click-to-booking conversion by <b>56.8% relative</b> (from 3.20% to 5.02%, p &lt; 0.01).",
        "<b>Modeled downstream behavioral velocity in Python</b>, proving that pre-filtered routing slashed average search-to-checkout time by <b>59%</b> (from 22.4 to 9.1 mins) and cut bounce rates by <b>44.9%</b>.",
        "<b>Partnered with Mobile Engineering and UX teams</b> to implement URL query payload passing and zero-inventory fallbacks, driving <b>$154,700 in incremental monthly GMV</b> with zero lodging cancellation harm."
    ]
    for b in cv_bullets:
        story.append(Paragraph(f"• {b}", styles['BulletText']))
        story.append(Spacer(1, 3))
    
    story.append(Spacer(1, 10))
    callout_final = create_callout(
        "<b>Whiteboard Readiness Checklist:</b> Before your interview, ensure you can draw the 5-step funnel on paper, sketch the Z-curve / distribution split, write the CTE structure of the SQL query from memory, and state the core numbers without hesitation: 3.20% to 5.02% conversion, 78% to 43% bounce, and 22 to 9 minute checkout.",
        styles,
        title="INTERVIEW WHITEBOARD CHECKLIST",
        border_color="#1A365D",
        bg_color="#EBF8FF"
    )
    story.append(callout_final)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_pdf}")

if __name__ == "__main__":
    generate_pdf()
