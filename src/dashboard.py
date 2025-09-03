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
tableau_url = "https://public.tableau.com/views/YourDashboardName/Dashboard1?:embed=y&:display_count=yes"
st.components.v1.iframe(tableau_url, width=1200, height=800)
