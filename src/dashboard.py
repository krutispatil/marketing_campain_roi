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
tableau_url = "https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Su&#47;Superstore_17265530774290&#47;Dashboard1&#47;1_rss.png' style='border: none'"

st.components.v1.iframe(tableau_url, width=1200, height=800)
