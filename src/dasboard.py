import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Connect to MySQL
engine = create_engine("mysql+pymysql://root:password@localhost/marketing_db")

# Load data
df = pd.read_sql("SELECT * FROM customers", engine)

st.title("📊 Marketing Campaign ROI Dashboard")

# Filters
income_filter = st.slider("Filter by Income", int(df["income"].min()), int(df["income"].max()), (20000, 80000))
df_filtered = df[(df["income"] >= income_filter[0]) & (df["income"] <= income_filter[1])]

# Show metrics
st.metric("Total Customers", len(df_filtered))
st.metric("Avg Income", int(df_filtered["income"].mean()))

# Spending chart
st.subheader("Average Spending by Product Category")
categories = ["mntwines", "mntmeatproducts", "mntgoldprods", "mntfruits", "mntsweetproducts"]
avg_spending = df_filtered[categories].mean()

fig, ax = plt.subplots()
avg_spending.plot(kind="bar", ax=ax)
st.pyplot(fig)
