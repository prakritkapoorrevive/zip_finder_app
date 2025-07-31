
import pandas as pd
import streamlit as st
from math import radians, cos, sin, asin, sqrt

@st.cache_data
def load_data():
    return pd.read_csv("zip_data_trimmed.csv")

def haversine(lat1, lon1, lat2, lon2):
    R = 3956  # miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

st.title("📍 ZIP Code Radius Finder")
st.write("Enter a latitude, longitude, and radius (in miles) to find ZIP codes within that area.")

lat = st.number_input("Latitude", value=40.7128)
lon = st.number_input("Longitude", value=-74.0060)
radius = st.number_input("Radius (miles)", value=50)

if st.button("Find ZIP Codes"):
    df = load_data()
    df["distance"] = df.apply(lambda row: haversine(lat, lon, row["lat"], row["lng"]), axis=1)
    nearby = df[df["distance"] <= radius].sort_values("distance")
    st.success(f"Found {len(nearby)} ZIP codes within {radius} miles.")
    st.dataframe(nearby[["zip", "city", "state_id", "county_name", "distance"]])
    csv = nearby.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "zip_radius_results.csv", "text/csv")
