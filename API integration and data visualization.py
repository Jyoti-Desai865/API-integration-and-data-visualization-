import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(page_title="Weather Forecast Dashboard", layout="wide")

st.title("🌦️ Weather Forecast Visualization Dashboard")
st.markdown("Using **OpenWeatherMap API** + **Seaborn**")

# User input
city = st.text_input("Enter City Name", "kolhapur")

# API config
API_KEY = "c0f8081c10a1c7716413010706b2c088"  # Replace with your OpenWeatherMap API key

# Fetch weather data
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    forecast_data = []

    for entry in data['list']:
        forecast_data.append({
            'datetime': entry['dt_txt'],
            'temperature': entry['main']['temp'],
            'humidity': entry['main']['humidity'],
            'weather': entry['weather'][0]['main']
        })

    df = pd.DataFrame(forecast_data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

# Main
df = get_weather_data(city)

if df is None:
    st.error("Failed to fetch data. Check city name or API key.")
else:
    st.success(f"Data fetched successfully for {city}!")

    col1, col2 = st.columns(2)

    # Temperature Line Chart
    with col1:
        st.subheader("🌡️ Temperature Forecast")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=df, x='datetime', y='temperature', ax=ax1, marker='o')
        ax1.set_title(f"Temperature Trend in {city}")
        ax1.set_xticklabels(df['datetime'].dt.strftime('%m-%d %H:%M'), rotation=45)
        st.pyplot(fig1)

    # Humidity Line Chart
    with col2:
        st.subheader("💧 Humidity Forecast")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=df, x='datetime', y='humidity', ax=ax2, color='blue', marker='s')
        ax2.set_title(f"Humidity Trend in {city}")
        ax2.set_xticklabels(df['datetime'].dt.strftime('%m-%d %H:%M'), rotation=45)
        st.pyplot(fig2)

    # Weather Count Plot
    st.subheader("🌥️ Weather Conditions Over 5 Days")
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.countplot(data=df, x='weather', palette='Set2', ax=ax3)
    ax3.set_title("Weather Conditions")
    st.pyplot(fig3)
