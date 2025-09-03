import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pymysql

st.set_page_config(page_title="Marketing Campaign ROI", layout="wide")

st.title("📊 Marketing Campaign ROI Dashboard")

# --- DATA LOADING FUNCTION ---
@st.cache_data
def load_data():
    try:
        # Try MySQL connection
        engine = create_engine("mysql+pymysql://root:password@localhost/marketing_db")
        df = pd.read_sql("SELECT * FROM customers", engine)
        st.success("✅ Loaded data from MySQL database")
    except Exception as e:
        # Fallback to CSV
        st.warning(f"⚠️ MySQL not available. Using CSV instead.\nError: {e}")
        df = pd.read_csv("data/ifood_df.csv")
    return df

df = load_data()

# --- FILTERS ---
with st.sidebar:
    st.header("🔍 Filters")
    income_filter = st.slider(
        "Income Range",
        int(df["income"].min()), 
        int(df["income"].max()), 
        (20000, 80000)
    )
    df = df[(df["income"] >= income_filter[0]) & (df["income"] <= income_filter[1])]

# --- METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Avg Income", f"${int(df['income'].mean()):,}")
col3.metric("Acceptance Rate", 
            f"{((df[['acceptedcmp1','acceptedcmp2','acceptedcmp3','acceptedcmp4','acceptedcmp5']].sum(axis=1) > 0).mean()*100:.1f}%")

# --- VISUALS ---
st.subheader("Average Spending by Product Category")
categories = ["mntwines", "mntmeatproducts", "mntgoldprods", "mntfruits", "mntsweetproducts"]
avg_spending = df[categories].mean()

fig, ax = plt.subplots()
avg_spending.plot(kind="bar", ax=ax, color="skyblue")
ax.set_ylabel("Average Spending ($)")
st.pyplot(fig)

st.subheader("Campaign Acceptance Distribution")
acceptance_cols = ["acceptedcmp1", "acceptedcmp2", "acceptedcmp3", "acceptedcmp4", "acceptedcmp5"]
campaign_acceptance = df[acceptance_cols].sum()

fig2, ax2 = plt.subplots()
campaign_acceptance.plot(kind="bar", ax=ax2, color="green")
ax2.set_ylabel("Number of Customers Accepted")
st.pyplot(fig2)

st.caption("💡 Data Source: iFood Marketing Campaign Dataset")
