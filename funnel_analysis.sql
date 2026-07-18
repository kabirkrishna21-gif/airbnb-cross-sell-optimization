-- funnel_analysis.sql
-- Analyzes conversion drop-off for Airbnb guests exposed to Experiences banners on Stays bookings.

WITH confirmed_stays AS (
  SELECT 
    booking_id,
    guest_user_id,
    destination_city,
    check_in_date,
    check_out_date,
    guest_count,
    created_at AS stay_booking_time
  FROM lodging_bookings.reservations
  WHERE check_in_date BETWEEN '2026-04-01' AND '2026-04-30'
    AND status = 'CONFIRMED'
),

banner_clicks AS (
  SELECT 
    cs.guest_user_id,
    cs.destination_city,
    cs.check_in_date,
    cs.check_out_date,
    cs.guest_count,
    e.event_timestamp AS click_time
  FROM confirmed_stays cs
  JOIN clickstream.events e 
    ON cs.guest_user_id = e.user_id 
    AND e.event_timestamp BETWEEN cs.stay_booking_time AND cs.stay_booking_time + INTERVAL '7' DAY
  WHERE e.element_id = 'itinerary_experiences_cross_sell'
),

experience_searches AS (
  SELECT 
    bc.guest_user_id,
    s.event_timestamp AS search_time
  FROM banner_clicks bc
  JOIN experiences.search_events s 
    ON bc.guest_user_id = s.user_id 
    AND s.event_timestamp BETWEEN bc.click_time AND bc.click_time + INTERVAL '30' MINUTE
),

checkout_initiations AS (
  SELECT 
    es.guest_user_id,
    c.event_timestamp AS checkout_time
  FROM experience_searches es
  JOIN experiences.checkout_funnel c 
    ON es.guest_user_id = c.user_id 
    AND c.event_timestamp BETWEEN es.search_time AND es.search_time + INTERVAL '60' MINUTE
  WHERE c.step_name = 'initiated_checkout'
),

completed_bookings AS (
  SELECT 
    ci.guest_user_id,
    t.event_timestamp AS transaction_time
  FROM checkout_initiations ci
  JOIN experiences.transactions t 
    ON ci.guest_user_id = t.user_id 
    AND t.event_timestamp BETWEEN ci.checkout_time AND ci.checkout_time + INTERVAL '30' MINUTE
  WHERE t.payment_status = 'SUCCESS'
)

SELECT 
  COUNT(DISTINCT cs.guest_user_id) AS step_1_confirmed_stays,
  COUNT(DISTINCT bc.guest_user_id) AS step_2_banner_clicks,
  COUNT(DISTINCT es.guest_user_id) AS step_3_search_page_opens,
  COUNT(DISTINCT ci.guest_user_id) AS step_4_checkout_initiated,
  COUNT(DISTINCT cb.guest_user_id) AS step_5_booking_completed,
  ROUND(COUNT(DISTINCT cb.guest_user_id) * 100.0 / COUNT(DISTINCT bc.guest_user_id), 2) AS click_to_booking_conversion_pct
FROM confirmed_stays cs
LEFT JOIN banner_clicks bc ON cs.guest_user_id = bc.guest_user_id
LEFT JOIN experience_searches es ON bc.guest_user_id = es.guest_user_id
LEFT JOIN checkout_initiations ci ON es.guest_user_id = ci.guest_user_id
LEFT JOIN completed_bookings cb ON ci.guest_user_id = cb.guest_user_id;
