# funnel_analysis.py
# Visualizes conversion drop-off for Airbnb guests exposed to Experiences banners.

import pandas as pd
import plotly.graph_objects as go
import os

def generate_funnel_chart():
    # Cohort counts from SQL analysis
    stages = [
        "1. Stay Bookings Confirmed", 
        "2. Experiences Banner Clicks", 
        "3. Search Page Loaded", 
        "4. Checkout Initiated", 
        "5. Experience Booking Completed"
    ]
    cohort_users = [850000, 102000, 22440, 7180, 3264]

    df = pd.DataFrame({"Stage": stages, "Users": cohort_users})

    # Plotting the conversion funnel
    fig = go.Figure(go.Funnel(
        y = df['Stage'],
        x = df['Users'],
        textinfo = "value+percent initial+percent previous",
        marker = {"color": ["#FF5A5F", "#FFB6C1", "#484848", "#008489", "#767676"]} # Airbnb styling colors
    ))

    fig.update_layout(
        title="Airbnb Stays to Experiences Cross-Sell Funnel (Baseline Analytics)",
        funnelmode="stack",
        plot_bgcolor="white"
    )

    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), "funnel_chart.png")
    fig.write_image(output_path)
    print(f"Funnel chart saved successfully to {output_path}")

if __name__ == "__main__":
    # Note: Requires 'plotly' and 'pandas' installed, and 'kaleido' for image export
    try:
        generate_funnel_chart()
    except Exception as e:
        print(f"Error generating chart: {e}")
        print("Please ensure pandas, plotly, and kaleido are installed.")
