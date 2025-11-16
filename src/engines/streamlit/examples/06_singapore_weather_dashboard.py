from datetime import datetime

import pandas as pd
import requests
import streamlit as st

st.title("🌦️ Singapore 2-Hour Weather Forecast")


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_weather_data():
    url = "https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch weather data: {str(e)}")
        return None


weather_data = get_weather_data()

if weather_data and weather_data.get("code") == 0:
    # Extract metadata
    area_metadata = weather_data["data"]["area_metadata"]
    forecast_item = weather_data["data"]["items"][0]
    forecasts = forecast_item["forecasts"]

    # Extract timestamp information
    update_time = datetime.fromisoformat(forecast_item["update_timestamp"])
    valid_period = forecast_item["valid_period"]["text"]

    # Display header info
    st.caption(f"**Last Updated:** {update_time.strftime('%d %b %Y, %I:%M %p')}")
    st.caption(f"**Valid Period:** {valid_period}")

    # Create DataFrame for map visualization
    map_data = []
    for area in area_metadata:
        # Find matching forecast
        forecast_info = next((f for f in forecasts if f["area"] == area["name"]), None)
        if forecast_info:
            map_data.append(
                {
                    "area": area["name"],
                    "latitude": area["label_location"]["latitude"],
                    "longitude": area["label_location"]["longitude"],
                    "forecast": forecast_info["forecast"],
                }
            )

    weather_data_df = pd.DataFrame(map_data)

    # Get unique forecast types for color mapping
    unique_forecasts = weather_data_df["forecast"].unique()

    # Create color mapping for different weather conditions
    weather_colors = {
        "Fair": [0, 255, 0, 160],  # Green
        "Fair (Day)": [0, 255, 0, 160],  # Green
        "Fair (Night)": [0, 200, 0, 160],  # Dark Green
        "Partly Cloudy": [100, 200, 255, 160],  # Light Blue
        "Partly Cloudy (Day)": [100, 200, 255, 160],
        "Partly Cloudy (Night)": [50, 150, 200, 160],
        "Cloudy": [150, 150, 150, 160],  # Gray
        "Light Rain": [255, 200, 0, 160],  # Yellow
        "Moderate Rain": [255, 150, 0, 160],  # Orange
        "Heavy Rain": [255, 100, 0, 160],  # Dark Orange
        "Passing Showers": [255, 200, 100, 160],  # Light Orange
        "Light Showers": [255, 220, 100, 160],
        "Showers": [255, 180, 0, 160],
        "Heavy Showers": [255, 100, 50, 160],
        "Thundery Showers": [255, 0, 0, 160],  # Red
        "Heavy Thundery Showers": [200, 0, 0, 160],  # Dark Red
        "Hazy": [200, 180, 150, 160],  # Tan
        "Mist": [180, 180, 200, 160],  # Light Gray
        "Windy": [150, 200, 255, 160],  # Sky Blue
    }

    # Assign colors
    weather_data_df["color"] = weather_data_df["forecast"].map(
        lambda x: weather_colors.get(str(x), [128, 128, 128, 160])
    )

    # Statistics
    col1, col2, col3 = st.columns(3)

    # Display map
    st.subheader("📍 Weather Map")
    st.map(
        weather_data_df,
        latitude="latitude",
        longitude="longitude",
        color="color",
        height=600,
        size=600,
        zoom=10,
    )

    # Legend
    st.subheader("🎨 Color Legend")
    legend_cols = st.columns(3)

    weather_legend = {
        "Fair/Clear": "🟢 Green",
        "Partly Cloudy": "🔵 Light Blue",
        "Cloudy": "⚪ Gray",
        "Light Rain/Showers": "🟡 Yellow/Light Orange",
        "Moderate Rain/Showers": "🟠 Orange",
        "Heavy Rain/Showers": "🟠 Dark Orange",
        "Thundery Showers": "🔴 Red",
        "Hazy/Mist": "🟤 Tan/Light Gray",
    }
    st.divider()

    with col1:
        st.metric("Total Areas", len(weather_data_df))

    with col2:
        most_common = weather_data_df["forecast"].value_counts().iloc[0]
        most_common_forecast = weather_data_df["forecast"].value_counts().index[0]
        st.metric("Most Common", most_common_forecast, f"{most_common} areas")

    with col3:
        unique_conditions = len(weather_data_df["forecast"].unique())
        st.metric("Unique Conditions", unique_conditions)

    # Detailed table with filters
    st.subheader("🔍 Detailed Area Forecast")

    # Filter by forecast type
    selected_forecast = st.multiselect(
        "Filter by weather condition:",
        options=["All"] + sorted(weather_data_df["forecast"].unique().tolist()),
        default=["All"],
    )

    # Apply filter
    if "All" not in selected_forecast and selected_forecast:
        filtered_df = weather_data_df[
            weather_data_df["forecast"].isin(selected_forecast)
        ]
    else:
        filtered_df = weather_data_df

    # Sort options
    sort_map = {
        "Area Name": "area",
        "Forecast": "forecast",
        "Latitude": "latitude",
        "Longitude": "longitude",
    }

    display_df = filtered_df[["area", "forecast", "latitude", "longitude"]].sort_values(
        by=sort_map["Area Name"]
    )
    display_df.columns = ["Area", "Forecast", "Latitude", "Longitude"]

    st.dataframe(display_df, width="stretch", hide_index=True)

    for idx, (condition, color) in enumerate(weather_legend.items()):
        with legend_cols[idx % 3]:
            st.caption(f"**{condition}:** {color}")

else:
    st.error("Unable to load weather data. Please try again later.")
