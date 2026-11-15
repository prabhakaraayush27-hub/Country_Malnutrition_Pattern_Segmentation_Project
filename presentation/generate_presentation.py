"""
Generate 16:9 Professional PowerPoint Presentation for
Country Malnutrition Pattern Segmentation Project
Bill & Melinda Gates Foundation Nutrition Analytics
Course: Unsupervised Learning (Units II, III & IV)
Submission Deadline: 15 November 2026
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # Set 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Color Palette Definitions
    C_BG_PAGE = RGBColor(248, 250, 252)      # #F8FAFC
    C_CARD_BG = RGBColor(255, 255, 255)      # #FFFFFF
    C_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0
    C_NAVY = RGBColor(15, 23, 42)            # #0F172A
    C_SLATE = RGBColor(51, 65, 85)           # #334155
    C_MUTED = RGBColor(100, 116, 139)        # #64748B
    C_INDIGO = RGBColor(79, 70, 229)         # #4F46E5
    C_CYAN = RGBColor(2, 132, 199)           # #0284C7
    C_ROSE = RGBColor(225, 29, 72)           # #E11D48
    C_EMERALD = RGBColor(5, 150, 105)        # #059669
    C_AMBER = RGBColor(217, 119, 6)          # #D97706
    C_LIGHT_INDIGO = RGBColor(238, 242, 255) # #EEF2FF
    C_LIGHT_EMERALD = RGBColor(236, 253, 245)# #ECFDF5
    C_LIGHT_AMBER = RGBColor(254, 243, 199)  # #FEF3C7

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_PAGE
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        # Header tag pill
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(9.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_INDIGO

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

        # Subtitle / Key Takeaway if present
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_MUTED

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    def add_footer(slide, current_slide, total_slides=13):
        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf = foot_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"Bill & Melinda Gates Foundation Nutrition Analytics • Unsupervised Learning • Slide {current_slide} of {total_slides}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1)

    # Accent decorative banner
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_INDIGO
    banner.line.fill.background()

    # Title Card
    c1 = add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.4))

    # Super-tag
    t1_box = s1.shapes.add_textbox(Inches(1.6), Inches(1.4), Inches(10.133), Inches(0.4))
    tf1 = t1_box.text_frame
    p = tf1.paragraphs[0]
    p.text = "BILL & MELINDA GATES FOUNDATION NUTRITION ANALYTICS • UNIVERSITY CAPSTONE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO

    # Main Project Title
    t2_box = s1.shapes.add_textbox(Inches(1.6), Inches(1.85), Inches(10.133), Inches(1.5))
    tf2 = t2_box.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Country Malnutrition Pattern Segmentation\nUsing Health Indicators and Clustering"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    # Subtitle
    t3_box = s1.shapes.add_textbox(Inches(1.6), Inches(3.45), Inches(10.133), Inches(0.8))
    tf3 = t3_box.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "Unsupervised Machine Learning Typologies Across 166 Sovereign States: Partition Clustering (K-Means/K-Medians), Hierarchical Linkage Comparison, and 2D Factor Visualisation"
    p.font.size = Pt(13)
    p.font.color.rgb = C_SLATE

    # Metadata Grid
    meta_box = s1.shapes.add_textbox(Inches(1.6), Inches(4.5), Inches(10.133), Inches(1.5))
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True
    
    p = tf_meta.paragraphs[0]
    p.text = "Course: Unsupervised Learning (Units II, III & IV)  •  Course Outcomes: CO2 (Partitioning), CO3 (Hierarchical), CO5 (Dimensionality Reduction)"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    p2 = tf_meta.add_paragraph()
    p2.text = "Primary Data: World Bank Open Data API & UNICEF/WHO Joint Malnutrition Estimates (100% Real Empirical Data)"
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    p3 = tf_meta.add_paragraph()
    p3.text = "Submission Date: 15 November 2026  •  Research Paper Extended Deadline: 24 November 2026"
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_INDIGO

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Context & Global Health Motivation", "The Complex Real-World Malnutrition Landscape", "Malnutrition is no longer a simple problem of caloric deficit, but a multifaceted global crisis.")
    add_footer(s2, 2)

    # Left Card: Problem Formulation
    add_card(s2, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.9))
    b2_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf2_l = b2_left.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "The Triple Burden of Malnutrition"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets = [
        ("Acute Undernutrition: ", "Child stunting (linear growth failure) and wasting (acute starvation) threaten infant survival in rural and developing economies."),
        ("Emerging Overnutrition: ", "Accelerated urbanisation and ultra-processed food markets trigger skyrocketing adult and child obesity across middle and high-income states."),
        ("The 'Double Burden': ", "Simultaneous presence of child undernutrition and maternal/adult obesity within the same country, community, or household."),
        ("Failure of National Averages: ", "Traditional national health metrics obscure deep systemic patterns, leading to flawed blanket policy interventions.")
    ]
    for b_title, b_desc in bullets:
        p = tf2_l.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = C_INDIGO
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = C_SLATE

    # Right Card: ML Project Mission
    add_card(s2, Inches(6.8), Inches(1.85), Inches(5.733), Inches(4.9))
    b2_right = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.333), Inches(4.5))
    tf2_r = b2_right.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "Machine Learning Project Objectives"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    objs = [
        ("Unsupervised Segmentation: ", "Group sovereign nations strictly by physiological health outcomes using partition and hierarchical clustering without subjective labeling."),
        ("Non-Circular Profiling: ", "Deliberately isolate GDP and World Bank Income Group from clustering features to prevent economic determinism."),
        ("Empirical Robustness: ", "Benchmark Euclidean vs. Manhattan metrics across K=3..8, evaluated under a common Euclidean ruler and 20-round bootstrap stability."),
        ("Actionable Policy Support: ", "Deliver an interactive decision-support system featuring live client-side 'What-If' simulation for Gates Foundation resource allocation.")
    ]
    for o_title, o_desc in objs:
        p = tf2_r.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = "✔ " + o_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = C_EMERALD
        run2 = p.add_run()
        run2.text = o_desc
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 3: DATA INGESTION & AUDIT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Data Provenance & Ingestion", "100% Real Empirical Health Indicators", "World Bank Open Data API + UNICEF / WHO Joint Malnutrition Estimates (Zero Synthetic Data)")
    add_footer(s3, 3)

    add_card(s3, Inches(0.8), Inches(1.85), Inches(4.8), Inches(4.9))
    b3_l = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.4), Inches(4.5))
    tf3_l = b3_l.text_frame
    tf3_l.word_wrap = True

    p = tf3_l.paragraphs[0]
    p.text = "Ingestion Pipeline Integrity"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    notes = [
        ("Source Authority: ", "World Bank API republishing UNICEF/WHO Joint Malnutrition Estimates (JME) and WHO/NCD-RisC."),
        ("Dual Ingestion Mode: ", "Primary JSON API with automatic fallback to static bulk CSV zip endpoints with exponential backoff."),
        ("Cohort Ingestion: ", "217 Sovereign states initially fetched; regional aggregates (e.g. 'World', 'Sub-Saharan Africa') identified and removed."),
        ("Missingness Audit: ", "10 candidate indicators evaluated. 'low_birthweight' had 0 reporting countries in the latest window and was dropped. 9 indicators kept (>68% coverage)."),
        ("Final Cohort: ", "166 sovereign states retained after country completeness pruning (>50% data available).")
    ]
    for n_t, n_d in notes:
        p = tf3_l.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + n_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_INDIGO
        r2 = p.add_run()
        r2.text = n_d
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_SLATE

    # Right Card: Indicator Table
    add_card(s3, Inches(5.9), Inches(1.85), Inches(6.633), Inches(4.9))
    b3_r = s3.shapes.add_textbox(Inches(6.1), Inches(2.0), Inches(6.233), Inches(4.5))
    tf3_r = b3_r.text_frame
    tf3_r.word_wrap = True

    p = tf3_r.paragraphs[0]
    p.text = "Retained Health Indicators (9 Dimensions)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    ind_data = [
        ("Child Stunting (% under-5)", "SH.STA.STNT.ZS", "75.1%", "Undernutrition"),
        ("Child Wasting (% under-5)", "SH.STA.WAST.ZS", "75.6%", "Undernutrition"),
        ("Child Underweight (% under-5)", "SH.STA.MALN.ZS", "74.7%", "Undernutrition"),
        ("Prevalence of Undernourishment", "SN.ITK.DEFC.ZS", "77.4%", "Caloric Deficit"),
        ("Anaemia in Children (% 6-59m)", "SH.ANM.CHLD.ZS", "87.6%", "Micronutrient"),
        ("Anaemia in Women (% 15-49y)", "SH.ANM.ALLW.ZS", "88.5%", "Maternal Health"),
        ("Exclusive Breastfeeding (% <6m)", "SH.STA.BFED.ZS", "68.2%", "Protective Practice"),
        ("Child Overweight (% under-5)", "SH.STA.OWGH.ZS", "76.0%", "Early Overnutrition"),
        ("Adult Obesity Prevalence (% 18+)", "SH.STA.OB18.ZS", "90.3%", "Adult Overnutrition")
    ]
    for name, code, cov, cat in ind_data:
        p = tf3_r.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = f"{name}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = f"{cov} global coverage  [{cat}]"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 4: 7-STEP PREPROCESSING PIPELINE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "Methodological Rigor", "7-Step Preprocessing & Quality Assurance", "Controlled transformations ensuring feature independence and mathematical reproducibility")
    add_footer(s4, 4)

    # Left: Steps breakdown
    add_card(s4, Inches(0.8), Inches(1.85), Inches(6.8), Inches(4.9))
    b4_l = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(6.4), Inches(4.5))
    tf4 = b4_l.text_frame
    tf4.word_wrap = True

    p = tf4.paragraphs[0]
    p.text = "Mathematical Pipeline Steps"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    steps = [
        ("Step 1 - Missingness Filter: ", "Dropped indicators with >40% missingness (low birthweight dropped)."),
        ("Step 2 - Completeness Filter: ", "Dropped 51 states with >50% missing indicators (166 retained)."),
        ("Step 3 - Collinearity Pruning: ", "Audited pairwise Pearson |r| > 0.92. Max observed r = 0.88 (Stunting vs Underweight); all 9 dimensions retained as independent."),
        ("Step 4 - Regional Imputation: ", "Imputed remaining NaNs using regional medians (Sub-Saharan Africa, Latin America, etc.) to preserve geo-demographic variance."),
        ("Step 5 - Winsorization: ", "Clipped heavy-tailed distributions at 1st and 99th percentiles to eliminate extreme national leverage points."),
        ("Step 6 - Categorical Isolation: ", "Income Group (1-4) and Region kept strictly for post-clustering profiling — NEVER fed to models (avoids circularity)."),
        ("Step 7 - StandardScaler: ", "Normalized all 9 health indicators to zero mean (μ = 0) and unit variance (σ = 1).")
    ]
    for s_t, s_d in steps:
        p = tf4.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = s_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_INDIGO
        r2 = p.add_run()
        r2.text = s_d
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE

    # Right: Embedded Correlation Matrix
    add_card(s4, Inches(7.9), Inches(1.85), Inches(4.633), Inches(4.9))
    fig_corr = os.path.join("backend", "outputs", "figures", "correlation_matrix.png")
    if os.path.exists(fig_corr):
        s4.shapes.add_picture(fig_corr, Inches(8.05), Inches(2.0), Inches(4.333), Inches(4.5))

    # =========================================================================
    # SLIDE 5: PARTITION CLUSTERING BENCHMARK
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Unit II: Partition Clustering Evaluation", "Euclidean K-Means vs. Manhattan K-Medians", "Comparing L2 centroid variance against custom L1 coordinate-wise median minimization across K=3..8")
    add_footer(s5, 5)

    add_card(s5, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.9))
    b5_l = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf5_l = b5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.text = "Mathematical Formulations"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    f_notes = [
        ("Euclidean K-Means (L2 Norm): ", "Minimizes within-cluster sum of squares: J = Σ Σ ||x_i - μ_k||_2^2. Uses k-means++ initialization with 20 random restarts."),
        ("Custom Manhattan K-Medians (L1 Norm): ", "Minimizes absolute Manhattan distance: J_L1 = Σ Σ ||x_i - m_k||_1. Centroids updated as coordinate-wise medians. Implemented with L1-adapted k-means++ init and empty cluster re-seeding."),
        ("Common Euclidean Ruler: ", "To fairly benchmark Manhattan vs Euclidean models without bias, all candidate partitions are evaluated under a common Euclidean ruler, while also reporting own-metric values."),
        ("Hyperparameter Sweep: ", "Systematic sweep across K = {3, 4, 5, 6, 7, 8} evaluated on Silhouette, Davies-Bouldin, and 20-round bootstrap stability.")
    ]
    for fn_t, fn_d in f_notes:
        p = tf5_l.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = fn_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_INDIGO
        r2 = p.add_run()
        r2.text = fn_d
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_SLATE

    # Right: Benchmark Summary Table
    add_card(s5, Inches(6.7), Inches(1.85), Inches(5.833), Inches(4.9))
    b5_r = s5.shapes.add_textbox(Inches(6.9), Inches(2.0), Inches(5.433), Inches(4.5))
    tf5_r = b5_r.text_frame
    tf5_r.word_wrap = True

    p = tf5_r.paragraphs[0]
    p.text = "Key Model Comparison Results"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    rows = [
        ("Euclidean K=3 ★", "0.2726", "1.7209", "0.8324 ± 0.102", "#1 (OPTIMAL)"),
        ("Euclidean K=4", "0.2079", "1.7610", "0.5025 ± 0.116", "#7"),
        ("Euclidean K=5", "0.2185", "1.6967", "0.5513 ± 0.089", "#5"),
        ("Euclidean K=6", "0.2079", "1.6425", "0.4851 ± 0.095", "#8"),
        ("Manhattan K=3", "0.2319", "1.9790", "0.8090 ± 0.086", "#3"),
        ("Manhattan K=4", "0.1983", "1.8973", "0.4908 ± 0.134", "#10"),
        ("Manhattan K=5", "0.1994", "1.7656", "0.5367 ± 0.104", "#9")
    ]

    p = tf5_r.add_paragraph()
    p.text = "Model | Silhouette | DB Index | Stability ARI | Rank"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_INDIGO

    for m_id, sil, db, stab, rnk in rows:
        p = tf5_r.add_paragraph()
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = f"• {m_id:15} | Sil: {sil} | DB: {db} | ARI: {stab} | {rnk}"
        r.font.size = Pt(9.5)
        if "OPTIMAL" in rnk:
            r.font.bold = True
            r.font.color.rgb = C_EMERALD
        else:
            r.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 6: MODEL VALIDATION & SELECTION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "Hyperparameter Validation & Selection", "Why Euclidean K = 3 Was Selected by Composite Rank", "Balancing Cluster Cohesion, Separation, and 20-Round Bootstrap Reproducibility")
    add_footer(s6, 6)

    # Left: Narrative
    add_card(s6, Inches(0.8), Inches(1.85), Inches(5.2), Inches(4.9))
    b6 = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.5))
    tf6 = b6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    p.text = "Analytical Selection Criteria"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    sel_points = [
        ("Composite Ranking Rule: ", "Rank = (Silhouette Rank + DB Rank + Stability Rank) / 3. Prevents bias towards overfitted partitions."),
        ("Optimal Stability at K=3: ", "Achieved mean ARI of 0.8324 across 20 bootstrap runs (80% subsampling without replacement), indicating an exceptionally robust core taxonomy."),
        ("Cohesion & Separation: ", "Delivers peak silhouette score (0.2726) and well-balanced cluster sizes (minimum cluster: 37 countries)."),
        ("Why Not K=4 or K=5? ", "At K=4, bootstrap stability drops sharply from 0.83 to 0.50 as transitional countries alternate between the obesity cluster and a nascent double-burden cluster."),
        ("Epidemiological Honesty: ", "K=3 captures the definitive macro-typologies; K=4 and K=5 provide valuable exploratory sub-clusters accessible via our interactive dashboard.")
    ]
    for sp_t, sp_d in sel_points:
        p = tf6.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "✔ " + sp_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_INDIGO
        r2 = p.add_run()
        r2.text = sp_d
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_SLATE

    # Right: Embedded Model Selection Panels Figure
    add_card(s6, Inches(6.3), Inches(1.85), Inches(6.233), Inches(4.9))
    fig_msp = os.path.join("backend", "outputs", "figures", "model_selection_panels.png")
    if os.path.exists(fig_msp):
        s6.shapes.add_picture(fig_msp, Inches(6.45), Inches(2.0), Inches(5.933), Inches(4.5))

    # =========================================================================
    # SLIDE 7: HIERARCHICAL CLUSTERING COMPARISON
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "Unit III: Hierarchical Comparison", "Agglomerative Linkages & Dendrogram Validation", "Verifying partition boundary validity through hierarchical tree construction and cophenetic correlation")
    add_footer(s7, 7)

    # Left: Embedded Dendrogram
    add_card(s7, Inches(0.8), Inches(1.85), Inches(6.4), Inches(4.9))
    fig_dend = os.path.join("backend", "outputs", "figures", "dendrogram.png")
    if os.path.exists(fig_dend):
        s7.shapes.add_picture(fig_dend, Inches(0.95), Inches(2.0), Inches(6.1), Inches(4.5))

    # Right: Hierarchical Benchmark Insights
    add_card(s7, Inches(7.5), Inches(1.85), Inches(5.033), Inches(4.9))
    b7 = s7.shapes.add_textbox(Inches(7.7), Inches(2.0), Inches(4.633), Inches(4.5))
    tf7 = b7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "Hierarchical Benchmark Findings"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    h_points = [
        ("Linkages Evaluated: ", "Ward (variance minimization), Complete (maximum distance), Average (mean distance), and Single (minimum distance) under Euclidean & Manhattan metrics."),
        ("Ward Linkage Superiority: ", "Ward linkage produced the highest structural agreement with K-Means (ARI = 0.7109, Silhouette = 0.2520)."),
        ("Tree Cut Height = 12.52: ", "Cutting the dendrogram at merge height 12.52 yields exactly 3 primary branches matching the optimal K=3 partition."),
        ("Cophenetic Correlation: ", "Average linkage achieved cophenetic correlation c = 0.7427, confirming strong preservation of original pairwise pairwise distances."),
        ("Theoretical Takeaway: ", "Hierarchical clustering strongly cross-validates the partition clustering boundaries, confirming natural separation rather than forced algorithmic artifacts.")
    ]
    for hp_t, hp_d in h_points:
        p = tf7.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + hp_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_INDIGO
        r2 = p.add_run()
        r2.text = hp_d
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 8: PCA FACTOR SPACE & LOADINGS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Unit IV: PCA Visualisation & Factor Loadings", "2D Principal Component Factor Space", "65.80% of total multi-indicator variance captured across two fundamental epidemiological axes")
    add_footer(s8, 8)

    # Left: Embedded PCA Scatter
    add_card(s8, Inches(0.8), Inches(1.85), Inches(6.6), Inches(4.9))
    fig_pca = os.path.join("backend", "outputs", "figures", "pca_scatter.png")
    if os.path.exists(fig_pca):
        s8.shapes.add_picture(fig_pca, Inches(0.95), Inches(2.0), Inches(6.3), Inches(4.5))

    # Right: Factor Interpretation Card
    add_card(s8, Inches(7.7), Inches(1.85), Inches(4.833), Inches(4.9))
    b8 = s8.shapes.add_textbox(Inches(7.9), Inches(2.0), Inches(4.433), Inches(4.5))
    tf8 = b8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "Factor Loading Interpretation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    pca_points = [
        ("PC1: 54.03% Variance Explained: ", "The 'Nutrition Transition Axis'. Highly positive loadings for child stunting (+0.42), underweight (+0.42), child anaemia (+0.38), and undernourishment (+0.37). Highly negative for adult obesity (-0.32). Spans the continuum from acute undernutrition to high obesity."),
        ("PC2: 11.77% Variance Explained: ", "The 'Infant Care vs. Acute Stress Axis'. Strong positive loading for exclusive breastfeeding (+0.62) vs. negative loading for child wasting (-0.48). Disentangles infant feeding behavior from acute wasting crises."),
        ("Biplot Vectors: ", "Vector angles reflect true correlation: stunting and wasting point northeast; obesity and overweight point southwest, visualizing the double burden divergence.")
    ]
    for pp_t, pp_d in pca_points:
        p = tf8.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + pp_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_INDIGO
        r2 = p.add_run()
        r2.text = pp_d
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 9: CLUSTER PROFILES & EPIDEMIOLOGICAL TYPOLOGIES
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Actionable Insights", "Epidemiological Taxonomy of the 3 Global Clusters", "Data-driven nomenclature based on standardized undernutrition and overnutrition indices")
    add_footer(s9, 9)

    # 3 Column Cards
    col_w = Inches(3.75)
    gap = Inches(0.25)

    # Card 1: Cluster 0
    c_c0 = add_card(s9, Inches(0.8), Inches(1.85), col_w, Inches(4.9))
    b9_1 = s9.shapes.add_textbox(Inches(0.95), Inches(2.0), col_w - Inches(0.3), Inches(4.5))
    tf9_1 = b9_1.text_frame
    tf9_1.word_wrap = True

    p = tf9_1.paragraphs[0]
    p.text = "🔴 Cluster 0: High Undernutrition"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_ROSE

    p = tf9_1.add_paragraph()
    p.text = "37 Sovereign States (22.3% of cohort)"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED

    c0_items = [
        ("Child Stunting: ", "33.4% (Z: +1.28)"),
        ("Child Wasting: ", "9.2% (Z: +1.17)"),
        ("Child Anaemia: ", "61.3% (Z: +1.38)"),
        ("Adult Obesity: ", "11.4% (Z: -0.92)"),
        ("Median GDP: ", "$1,193 (Low/Lower-Mid)"),
        ("Geography: ", "Sub-Saharan Africa (Chad, Niger, Nigeria, Angola, Burundi) and South Asia (Afghanistan)."),
        ("Policy Action: ", "Therapeutic refeeding (RUTF), WASH infrastructure, maternal micronutrients.")
    ]
    for ci_t, ci_v in c0_items:
        p = tf9_1.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = ci_t
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = ci_v
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_SLATE

    # Card 2: Cluster 1
    c_c1 = add_card(s9, Inches(0.8) + col_w + gap, Inches(1.85), col_w, Inches(4.9))
    b9_2 = s9.shapes.add_textbox(Inches(0.95) + col_w + gap, Inches(2.0), col_w - Inches(0.3), Inches(4.5))
    tf9_2 = b9_2.text_frame
    tf9_2.word_wrap = True

    p = tf9_2.paragraphs[0]
    p.text = "🔵 Cluster 1: High Overweight & Obesity"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    p = tf9_2.add_paragraph()
    p.text = "92 Sovereign States (55.4% of cohort)"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED

    c1_items = [
        ("Adult Obesity: ", "29.7% (Z: +0.53)"),
        ("Child Overweight: ", "8.6% (Z: +0.49)"),
        ("Child Stunting: ", "8.1% (Z: -0.70)"),
        ("Child Wasting: ", "2.7% (Z: -0.54)"),
        ("Median GDP: ", "$14,264 (Upper-Mid/High)"),
        ("Geography: ", "Europe & Central Asia (32), Latin America (25), North America (USA, Canada)."),
        ("Policy Action: ", "Sugar taxes, front-of-pack labeling, urban walkability, cardiometabolic screening.")
    ]
    for ci_t, ci_v in c1_items:
        p = tf9_2.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = ci_t
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = ci_v
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_SLATE

    # Card 3: Cluster 2
    c_c2 = add_card(s9, Inches(0.8) + (col_w + gap)*2, Inches(1.85), col_w, Inches(4.9))
    b9_3 = s9.shapes.add_textbox(Inches(0.95) + (col_w + gap)*2, Inches(2.0), col_w - Inches(0.3), Inches(4.5))
    tf9_3 = b9_3.text_frame
    tf9_3.word_wrap = True

    p = tf9_3.paragraphs[0]
    p.text = "🟢 Cluster 2: Moderate / Transitional"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf9_3.add_paragraph()
    p.text = "37 Sovereign States (22.3% of cohort)"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED

    c2_items = [
        ("Child Stunting: ", "22.9% (Z: +0.46)"),
        ("Child Wasting: ", "5.4% (Z: +0.18)"),
        ("Child Anaemia: ", "42.8% (Z: +0.37)"),
        ("Adult Obesity: ", "18.0% (Z: -0.40)"),
        ("Median GDP: ", "$3,648 (Lower-Middle)"),
        ("Geography: ", "Sub-Saharan Africa (Ghana, Kenya, Zimbabwe), East Asia & Pacific (Philippines, Cambodia)."),
        ("Policy Action: ", "'Double-duty actions': protect breastfeeding while halting ultra-processed foods.")
    ]
    for ci_t, ci_v in c2_items:
        p = tf9_3.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = ci_t
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = ci_v
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 10: BORDERLINE CASES & NUTRITIONAL CONTINUUM
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "Uncertainty & Sensitivity Audit", "Borderline Nations: The Nutritional Transition Continuum", "Identifying 15 nations with low silhouette values (s < 0.05) on the boundary between clusters")
    add_footer(s10, 10)

    # Left Card: Theoretical Significance
    add_card(s10, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.9))
    b10_l = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf10_l = b10_l.text_frame
    tf10_l.word_wrap = True

    p = tf10_l.paragraphs[0]
    p.text = "Why Borderline Cases Matter"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    b_cases_notes = [
        ("The Silhouette Boundary: ", "15 out of 166 countries (9.0%) have silhouette scores < 0.05, placing them on geometric cluster boundaries."),
        ("Limitations of Hard Partitioning: ", "K-Means forces binary assignments, but epidemiological shifts occur continuously over decades."),
        ("The 'Double Burden' Embryo: ", "When K is increased to 4 or 5, it is precisely these borderline nations that fracture out to create the Double Burden cluster."),
        ("Policy Prudence: ", "Borderline countries must NOT be subjected to rigid single-track interventions. They require dual-track programming addressing both stunting and metabolic risks.")
    ]
    for bcn_t, bcn_d in b_cases_notes:
        p = tf10_l.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + bcn_t
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_AMBER
        r2 = p.add_run()
        r2.text = bcn_d
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_SLATE

    # Right Card: Exemplar Borderline Audit
    add_card(s10, Inches(6.7), Inches(1.85), Inches(5.833), Inches(4.9))
    b10_r = s10.shapes.add_textbox(Inches(6.9), Inches(2.0), Inches(5.433), Inches(4.5))
    tf10_r = b10_r.text_frame
    tf10_r.word_wrap = True

    p = tf10_r.paragraphs[0]
    p.text = "Key Borderline Nations Audited"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    b_countries = [
        ("Kiribati (KIR)", "s = -0.061", "Stunting: 29.8% | Adult Obesity: 46.0%", "Severe Pacific island double burden anomaly."),
        ("Cambodia (KHM)", "s = +0.007", "Stunting: 22.0% | Wasting: 9.6% | Obesity: 5.8%", "Fast-transitioning East Asian economy on cusp of C0/C2."),
        ("Guatemala (GTM)", "s = +0.015", "Stunting: 43.5% | Adult Obesity: 23.4%", "Extreme chronic stunting coexisting with urban obesity."),
        ("Solomon Islands (SLB)", "s = +0.021", "Stunting: 31.7% | Obesity: 28.9%", "Melanesian nutrition transition archetype."),
        ("Botswana (BWA)", "s = +0.029", "Stunting: 28.9% | Obesity: 18.9%", "Upper-middle income Sub-Saharan transition nation.")
    ]
    for c_name, sil_val, stats, notes_str in b_countries:
        p = tf10_r.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = f"{c_name}  [{sil_val}]\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = f"  {stats}\n  Note: {notes_str}"
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 11: INTERACTIVE DECISION SUPPORT DASHBOARD
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_background(s11)
    add_header(s11, "Decision Support Architecture", "Interactive Dashboard & 'What-If' Simulation Engine", "Client-side machine learning inference with real-time centroid distance calculations and factor projections")
    add_footer(s11, 11)

    add_card(s11, Inches(0.8), Inches(1.85), Inches(5.8), Inches(4.9))
    b11_l = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.4), Inches(4.5))
    tf11_l = b11_l.text_frame
    tf11_l.word_wrap = True

    p = tf11_l.paragraphs[0]
    p.text = "⚡ Live Country Nutrition Profile Simulator"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO

    dash_features = [
        ("9 Dynamic Indicator Sliders: ", "Users adjust stunting, wasting, obesity, and anaemia in real time."),
        ("Client-Side Standardization: ", "Uses exact pipeline StandardScaler parameters (μ, σ) stored in results.js to compute z-scores in <1ms without server roundtrips."),
        ("Centroid Distance Bars: ", "Computes Euclidean and Manhattan distance bars to all active cluster centers instantly."),
        ("Live PCA Projection: ", "Projects the simulated country as a pulsing glowing marker (★ SIMULATED NATION) on the PCA biplot."),
        ("Nearest Sovereign State Query: ", "Dynamically queries 9D Euclidean distance across all 166 nations to display the Top 3 closest real countries.")
    ]
    for df_t, df_d in dash_features:
        p = tf11_l.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = "• " + df_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = df_d
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE

    add_card(s11, Inches(6.9), Inches(1.85), Inches(5.633), Inches(4.9))
    b11_r = s11.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.233), Inches(4.5))
    tf11_r = b11_r.text_frame
    tf11_r.word_wrap = True

    p = tf11_r.paragraphs[0]
    p.text = "🔍 Additional Interactive Tools"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    tools = [
        ("Country Detail Inspector Drawer: ", "Clicking any scatter dot, country pill, or table row slides open an inspector drawer with radar comparisons against global/cluster averages, and a button to load that real country directly into the simulator."),
        ("▶ 'Play Progression' Engine: ", "Auto-cycles K=3 through K=8 on a smooth 1.6-second timer so users can observe cluster splitting dynamics on the 2D factor space."),
        ("Interactive Model Matrix: ", "Click any row in the 12-model configuration table to activate that configuration across the entire dashboard."),
        ("Zero-Build Static Architecture: ", "Vanilla HTML5 + CSS3 + pure JavaScript with responsive hand-drawn SVG charts. Zero external build tools; works by double-clicking index.html.")
    ]
    for t_t, t_d in tools:
        p = tf11_r.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = "✔ " + t_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_EMERALD
        r2 = p.add_run()
        r2.text = t_d
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 12: LIMITATIONS & ETHICAL FRAMEWORK
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_background(s12)
    add_header(s12, "Responsible AI & Public Health Ethics", "Limitations, Bias Audit & Responsible Use Principles", "Translating mathematical partitions into ethical public health policy")
    add_footer(s12, 12)

    add_card(s12, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.9))
    b12_l = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf12_l = b12_l.text_frame
    tf12_l.word_wrap = True

    p = tf12_l.paragraphs[0]
    p.text = "Methodological Limitations"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    limits = [
        ("Survey Asynchrony: ", "Household health surveys (DHS, MICS) operate on 3-5 year cycles; data reflects 2018-2023. Recent conflict or climate shocks are not captured instantaneously."),
        ("Ecological Fallacy: ", "National averages conceal severe subnational, wealth-quintile, and rural-urban inequalities within nations."),
        ("Missing Surveillance Bias: ", "Excluded nations were non-reporting microstates and developed nations without UNICEF anthropometric surveys."),
        ("Algorithm Sensitivity: ", "Clustering boundaries depend on scaling (StandardScaler) and chosen distance metric, reinforcing the necessity of sensitivity audits.")
    ]
    for l_t, l_d in limits:
        p = tf12_l.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "⚠️ " + l_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_AMBER
        r2 = p.add_run()
        r2.text = l_d
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE

    add_card(s12, Inches(6.8), Inches(1.85), Inches(5.733), Inches(4.9))
    b12_r = s12.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.333), Inches(4.5))
    tf12_r = b12_r.text_frame
    tf12_r.word_wrap = True

    p = tf12_r.paragraphs[0]
    p.text = "Ethical Principles for Decision Makers"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    ethics = [
        ("No Stigmatizing Nomenclature: ", "Clusters represent epidemiological typologies, NOT moral hierarchies. High obesity carries massive non-communicable disease burden, just as stunting carries mortality risk."),
        ("Decision Support, Not Automated Decisions: ", "Clusters must guide program co-design, never automate punitive aid reductions or resource reallocation."),
        ("Non-Circular Feature Selection: ", "GDP and Income Group were strictly isolated to prevent economic determinism from dictating health typologies."),
        ("Human Accountability: ", "Policy makers and epidemiologists remain accountable for all resource distribution decisions.")
    ]
    for e_t, e_d in ethics:
        p = tf12_r.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = "🛡️ " + e_t
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_INDIGO
        r2 = p.add_run()
        r2.text = e_d
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 13: MANDATORY FINAL SLIDE - PROJECT LINKS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_background(s13)
    add_header(s13, "Mandatory Final Slide", "Project Links & Deliverables", "Accessible hyperlinks to complete source code, real datasets, interactive deployment, and academic research paper")
    add_footer(s13, 13)

    # 4 Structured Resource Cards
    c_w = Inches(5.6)
    c_h = Inches(2.3)

    # Card 1: GitHub Repository
    add_card(s13, Inches(0.8), Inches(1.85), c_w, c_h, bg_color=C_LIGHT_INDIGO, border_color=C_INDIGO)
    b13_1 = s13.shapes.add_textbox(Inches(1.0), Inches(1.95), c_w - Inches(0.4), c_h - Inches(0.2))
    tf13_1 = b13_1.text_frame
    tf13_1.word_wrap = True
    p = tf13_1.paragraphs[0]
    p.text = "📦 1. GitHub Source Code Repository"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO

    p = tf13_1.add_paragraph()
    p.space_before = Pt(4)
    p.text = "Complete Python backend, 7-step pipeline, custom K-Medians metrics, interactive frontend, and documentation."
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_SLATE

    p = tf13_1.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    r.text = "🔗 GitHub Link: https://github.com/Abhiudhay-Singh/malnutrition-clustering-segmentation"
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = C_INDIGO

    # Card 2: Real Empirical Dataset
    add_card(s13, Inches(6.8), Inches(1.85), c_w, c_h, bg_color=C_LIGHT_EMERALD, border_color=C_EMERALD)
    b13_2 = s13.shapes.add_textbox(Inches(7.0), Inches(1.95), c_w - Inches(0.4), c_h - Inches(0.2))
    tf13_2 = b13_2.text_frame
    tf13_2.word_wrap = True
    p = tf13_2.paragraphs[0]
    p.text = "📊 2. Real World Bank & JME Dataset"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf13_2.add_paragraph()
    p.space_before = Pt(4)
    p.text = "Merged 166-country × 9-indicator health dataset with regional codes and income classifications."
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_SLATE

    p = tf13_2.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    r.text = "🔗 World Bank Open Data: https://data.worldbank.org/indicator\n📁 Local Raw CSV: backend/data/raw/nutrition_indicators.csv"
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = C_EMERALD

    # Card 3: Live Interactive Deployment
    add_card(s13, Inches(0.8), Inches(4.35), c_w, c_h, bg_color=C_LIGHT_AMBER, border_color=C_AMBER)
    b13_3 = s13.shapes.add_textbox(Inches(1.0), Inches(4.45), c_w - Inches(0.4), c_h - Inches(0.2))
    tf13_3 = b13_3.text_frame
    tf13_3.word_wrap = True
    p = tf13_3.paragraphs[0]
    p.text = "🌐 3. Live Dashboard Deployment"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    p = tf13_3.add_paragraph()
    p.space_before = Pt(4)
    p.text = "Interactive What-If Simulator, PCA Explorer, Dendrogram, Country Inspector Drawer, and Theme Toggle."
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_SLATE

    p = tf13_3.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    r.text = "🔗 Live Deployment: https://abhiudhay-singh.github.io/malnutrition-clustering-segmentation/\n🖥️ Local Live Server: http://localhost:8080/index.html"
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = C_AMBER

    # Card 4: IEEE Research Paper & Academic Artifacts
    add_card(s13, Inches(6.8), Inches(4.35), c_w, c_h, bg_color=C_CARD_BG, border_color=C_NAVY)
    b13_4 = s13.shapes.add_textbox(Inches(7.0), Inches(4.45), c_w - Inches(0.4), c_h - Inches(0.2))
    tf13_4 = b13_4.text_frame
    tf13_4.word_wrap = True
    p = tf13_4.paragraphs[0]
    p.text = "📄 4. IEEE Research Paper & Academic Docs"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    p = tf13_4.add_paragraph()
    p.space_before = Pt(4)
    p.text = "Mandatory IEEE-compliant Research Paper (Nov 24 submission), LaTeX sources, and comprehensive technical report."
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_SLATE

    p = tf13_4.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    r.text = "📑 IEEE Paper: docs/IEEE_RESEARCH_PAPER.md & .tex\n📑 Full Technical Report: docs/REPORT.md\n🎤 Speaker Script: presentation/SLIDES_TRANSCRIPT.md"
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = C_NAVY

    # Save presentation
    out_path = os.path.join("presentation", "Malnutrition_Clustering_Presentation.pptx")
    prs.save(out_path)
    print(f"[SUCCESS] Presentation generated successfully: {out_path}")

if __name__ == "__main__":
    create_deck()
