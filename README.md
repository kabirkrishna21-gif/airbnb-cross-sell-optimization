# Airbnb Stays to Experiences: Cross-Sell Conversion Optimization

This repository contains the analysis, SQL query, visualization code, A/B testing framework, and business impact dashboard for a product optimization project at Airbnb. The project focuses on improving the conversion funnel for cross-selling **Experiences** to guests with confirmed **Stays** bookings.

---

## 1. The Core Problem: The Stay-to-Experience Gap

### Business Context
Airbnb has millions of monthly active users booking accommodations (Stays). To drive incremental revenue per guest, the business focuses on cross-selling **Experiences** (tours, classes, and activities) to guests with confirmed lodging reservations. 

Despite placing high-visibility promotion cards on the post-booking trip itinerary page, the conversion rate remained low.

### The Ambiguity
A cohort analysis of guests booking travel revealed a significant leak:
1. **High Click-Through, Low Action**: The promo banner on the active trip itinerary page had a solid CTR of **12%**, indicating guests were interested in activities.
2. **The Friction Point (Context Loss)**: Upon clicking the banner, users were redirected to the generic Experiences homepage. They had to manually re-enter their trip destination, checkout/check-in dates, and guest count. This friction caused a **78% drop-off** on the search landing page.
3. **The Hypothesis**: By implementing **Context-Preserved Dynamic Routing**—automatically pre-filtering the Experiences catalog by the guest's booked stay dates, neighborhood (within a 5km radius), and guest count—we will increase transaction conversion rates by **at least 1.5% absolute**.

---

## 2. Repository Structure

* `funnel_analysis.sql`: Production-ready SQL cohort analysis query to map the user conversion funnel.
* `funnel_analysis.py`: Python script using `plotly` and `pandas` to visualize funnel drop-off stages.
* `README.md`: Detailed project summary, experimentation framework, results, and learnings.

---

## 3. Data Investigation (SQL & Python)

### SQL Funnel Extraction
The cohort analysis was extracted using standard clickstream schemas:
* `lodging_bookings.reservations`: Holds checkout and reservation status data.
* `clickstream.events`: Captures trip itinerary view and banner click events.
* `experiences.search_events` & `experiences.checkout_funnel`: Tracks downstream user actions on the Experiences vertical.
* `experiences.transactions`: Holds success payment events.

*(See full query in `funnel_analysis.sql`)*

### Funnel Visualization
The Python script in `funnel_analysis.py` models the 5-step conversion funnel:
1. Stay Bookings Confirmed
2. Experiences Banner Clicks
3. Search Page Loaded
4. Checkout Initiated
5. Experience Booking Completed

---

## 4. The Experiment: Context-Preserved Deep-Linking

### Design
* **Target Audience**: Confirmed Stays guests viewing their itinerary in major tourist hubs (e.g., Paris, Tokyo, London, New York).
* **Control (Variant A - 50% traffic)**: Standard itinerary banner linking to the generic Experiences homepage.
* **Variant B (50% traffic)**: Context-preserved banner dynamically linking to the Experiences listing page, pre-filtered for the booking's exact dates and guest count, centered around the lodging geo-coordinates.

### Key Metrics
* **Primary Metric**: Banner Click-to-Booking Completion Rate (%)
* **Secondary Metrics**: Search Page Bounce Rate, Average Search-to-Checkout Time, Average Order Value (AOV), and 7-day post-experience retention (reviews submitted).

---

## 5. The Impact: A/B Test Results

After running the experiment for 14 days, the results demonstrated statistical significance ($p < 0.01$):

| Funnel Metric | Control (A) | Variant (B) | Relative Delta |
| :--- | :--- | :--- | :--- |
| **Itinerary Banner CTR** | 12.0% | 14.1% | +17.5% |
| **Landing Page Bounce Rate** | 78.0% | 43.0% | -44.9% |
| **Checkout Initiation Rate (per click)**| 7.0% | 15.5% | +121.4% |
| **Conversion Rate (Click to Booking)**| **3.20%** | **5.02%** | **+56.9% (Absolute +1.82%)** |
| **Avg. Search-to-Checkout Time** | 22 mins | 9 mins | -59.1% |

### Key Takeaway
Dynamic routing eliminated top-of-funnel friction. By automating search details, users reached checkout **59% faster** (9 mins vs 22 mins), reducing time-to-decision and increasing bookings.
