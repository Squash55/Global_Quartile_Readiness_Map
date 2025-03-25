
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Global Readiness Map by Quartile (Artificial data)", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("USAF_Global_125_Bases.csv")

df = load_data()

st.title("🌍 Global Mission Readiness Map by Quartile (Artificial data)")
st.markdown("Explore 125 Air Force bases worldwide, color-coded by readiness quartile.")

# Compute quartiles
q1 = df["Readiness"].quantile(0.25)
q2 = df["Readiness"].quantile(0.50)
q3 = df["Readiness"].quantile(0.75)

def assign_color(readiness):
    if readiness <= q1:
        return [255, 0, 0]       # Red
    elif readiness <= q2:
        return [255, 165, 0]     # Orange
    elif readiness <= q3:
        return [255, 255, 0]     # Yellow
    else:
        return [0, 200, 0]       # Green

df["color"] = df["Readiness"].apply(assign_color)

# Map layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[Longitude, Latitude]",
    get_color="color",
    get_radius=60000,
    pickable=True,
)

# View settings
view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=1.3,
    pitch=30,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Base: {Base}\nCountry: {Country}\nReadiness: {Readiness}"}
))

# Smart insights
st.subheader("📊 Readiness Quartile Summary")
st.markdown(f"- 🟥 **Q1 (≤ {q1:.1f})** – Critically low readiness")
st.markdown(f"- 🟧 **Q2 (≤ {q2:.1f})** – Below average")
st.markdown(f"- 🟨 **Q3 (≤ {q3:.1f})** – Above average")
st.markdown("- 🟩 **Q4 (> Q3)** – Highest readiness")
st.markdown("Color trends can help prioritize global interventions and identify top-performing regions.")
