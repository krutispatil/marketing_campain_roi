import streamlit as st
from insights import load_data, generate_insights

st.title("📊 Marketing Campaign ROI Insights")

df = load_data()

# Generate Insights
st.subheader("🔎 Business Insights (from SQL)")
for insight in generate_insights(df):
    st.markdown(insight)

# Embed Tableau
st.subheader("📈 Interactive Tableau Dashboard")

tableau_url = "https://public.tableau.com/views/Superstore_17265530774290/Dashboard1?:showVizHome=no&:embed=true"

st.components.v1.iframe(tableau_url, height=927, width=1300)

