
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Global Readiness Map (Scaled Radius)", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("USAF_Global_125_Bases.csv")
    df["adjusted_radius"] = 60000 / (1 + (df["Latitude"].abs() - 40) * 0.05)
    return df

df = load_data()

st.title("🌍 Global Mission Readiness Map (Scaled Radius)")
st.markdown("Circle size is adjusted based on latitude to reduce visual distortion near poles.")

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

# Map layer with scaled radius
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[Longitude, Latitude]",
    get_color="color",
    get_radius="adjusted_radius",
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=1.3,
    pitch=0,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Base: {Base}\nCountry: {Country}\nReadiness: {Readiness}"}
))

# Insights
st.subheader("📊 Readiness Quartile Summary")
st.markdown(f"- 🟥 Q1 (≤ {q1:.1f}) – Critically low readiness")
st.markdown(f"- 🟧 Q2 (≤ {q2:.1f}) – Below average")
st.markdown(f"- 🟨 Q3 (≤ {q3:.1f}) – Above average")
st.markdown("- 🟩 Q4 (> Q3) – Highest readiness")

st.subheader("🧠 Smart Pattern Detection")
high_df = df[df["Readiness"] >= q3]
low_df = df[df["Readiness"] <= q1]
top_countries = high_df["Country"].value_counts().head(3)
bottom_countries = low_df["Country"].value_counts().head(3)

st.markdown("**Top Countries with High Readiness Bases:**")
for country, count in top_countries.items():
    st.markdown(f"- 🟩 {country}: {count} base(s) in Q4")

st.markdown("**Countries with Most Critically Low Readiness Bases:**")
for country, count in bottom_countries.items():
    st.markdown(f"- 🟥 {country}: {count} base(s) in Q1")

st.markdown("**Observation:** These patterns may indicate strengths or systemic vulnerabilities in specific regions. Use these trends to inform strategic interventions.")
