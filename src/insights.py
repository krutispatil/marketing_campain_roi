import pandas as pd
import sqlite3
import os

# --- Utility to run SQL on Pandas dataframe ---
def run_sql(df, query):
    with sqlite3.connect(":memory:") as conn:
        df.to_sql("df", conn, index=False, if_exists="replace")
        return pd.read_sql(query, conn)

# --- 1. Campaign Responsiveness by Age Group ---
def age_group_responsiveness(df):
    q = """
    SELECT 
        CASE 
            WHEN age < 30 THEN 'Under 30'
            WHEN age BETWEEN 30 AND 50 THEN '30-50'
            ELSE '50+' 
        END AS age_group,
        AVG(acceptedcmp1 + acceptedcmp2 + acceptedcmp3 + acceptedcmp4 + acceptedcmp5) AS avg_campaigns_accepted
    FROM df
    GROUP BY age_group;
    """
    result = run_sql(df, q)
    best_group = result.sort_values("avg_campaigns_accepted", ascending=False).iloc[0]
    return f"👥 Customers aged **{best_group['age_group']}** are the most responsive, accepting more campaigns on average than other groups."


# --- 2. Spending by Education Level ---
def spending_by_education(df):
    q = """
    SELECT education, AVG(mnttotal) AS avg_spending
    FROM df
    GROUP BY education;
    """
    result = run_sql(df, q)
    top = result.sort_values("avg_spending", ascending=False).iloc[0]
    return f"🎓 Customers with **{top['education']}** education spend the most, averaging {top['avg_spending']:.0f} units."


# --- 3. Responsiveness by Marital Status ---
def responsiveness_by_marital_status(df):
    q = """
    SELECT marital_status, 
           AVG(acceptedcmp1 + acceptedcmp2 + acceptedcmp3 + acceptedcmp4 + acceptedcmp5) AS avg_campaigns_accepted
    FROM df
    GROUP BY marital_status;
    """
    result = run_sql(df, q)
    top = result.sort_values("avg_campaigns_accepted", ascending=False).iloc[0]
    return f"💍 Customers who are **{top['marital_status']}** respond best to campaigns, with an average acceptance rate of {top['avg_campaigns_accepted']:.2f}."


# --- 4. Top Product Category ---
def top_product_category(df):
    q = """
    SELECT 
        AVG(mntwines) AS avg_wines,
        AVG(mntfruits) AS avg_fruits,
        AVG(mntmeatproducts) AS avg_meat,
        AVG(mntfishproducts) AS avg_fish,
        AVG(mntsweetproducts) AS avg_sweets,
        AVG(mntgoldprods) AS avg_gold
    FROM df;
    """
    result = run_sql(df, q)
    row = result.iloc[0].to_dict()
    top_cat = max(row, key=row.get)
    return f"🍷 The most purchased category is **{top_cat.replace('avg_', '').title()}**, averaging {row[top_cat]:.0f} units per customer."


# --- 5. Loyalty Segments ---
def loyalty_segment(df):
    q = """
    SELECT 
        CASE 
            WHEN acceptedcmpoverall >= 3 THEN 'Loyal'
            WHEN acceptedcmpoverall = 2 THEN 'Moderately Loyal'
            ELSE 'Low Loyalty'
        END AS loyalty_segment,
        COUNT(*) AS customers
    FROM df
    GROUP BY loyalty_segment;
    """
    result = run_sql(df, q)
    top = result.sort_values("customers", ascending=False).iloc[0]
    return f"📊 The largest customer segment is **{top['loyalty_segment']}**, with {top['customers']} customers."

def load_data(filename="ifood_df.csv"):
    base_path = os.path.dirname(__file__)
    
    # First: look in src/
    path1 = os.path.join(base_path, filename)
    
    # Second: look in project root
    path2 = os.path.join(base_path, "..", filename)

    if os.path.exists(path1):
        path = path1
    elif os.path.exists(path2):
        path = path2
    else:
        raise FileNotFoundError(f"❌ Could not find {filename} in {path1} or {path2}")
    
    print("✅ Loading CSV from:", os.path.abspath(path))
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def campaign_acceptance(df):
    total = (df[['acceptedcmp1','acceptedcmp2','acceptedcmp3','acceptedcmp4','acceptedcmp5']].sum().sum())
    customers = len(df)
    rate = total / customers
    return f"📈 Overall campaign acceptance rate is **{rate:.2f} per customer** across all campaigns."

def recency_vs_engagement(df):
    q = """
    SELECT 
        CASE 
            WHEN recency <= 30 THEN 'Last Month'
            WHEN recency BETWEEN 31 AND 90 THEN '1-3 Months'
            WHEN recency BETWEEN 91 AND 180 THEN '3-6 Months'
            ELSE '6+ Months'
        END AS recency_group,
        AVG(acceptedcmp1 + acceptedcmp2 + acceptedcmp3 + acceptedcmp4 + acceptedcmp5) AS avg_campaigns_accepted
    FROM df
    GROUP BY recency_group;
    """
    result = run_sql(df, q)
    best = result.sort_values("avg_campaigns_accepted", ascending=False).iloc[0]
    return f"⏳ Customers with **{best['recency_group']}** since last purchase engage most, accepting {best['avg_campaigns_accepted']:.2f} campaigns on average."

def channel_effectiveness(df):
    q = """
    SELECT 
        AVG(numwebvisitsmonth) AS avg_web_visits,
        AVG(numwebpurchases) AS avg_web_purchases,
        AVG(numcatalogpurchases) AS avg_catalog_purchases,
        AVG(numstorepurchases) AS avg_store_purchases
    FROM df;
    """
    result = run_sql(df, q)
    row = result.iloc[0].to_dict()
    top_channel = max(row, key=row.get)
    return f"📢 The most effective channel is **{top_channel.replace('avg_', '').replace('_', ' ').title()}**, with an average of {row[top_channel]:.1f} interactions per customer."




def generate_insights(df):
    return [
        campaign_acceptance(df),
        age_group_responsiveness(df),
        recency_vs_engagement(df),
        channel_effectiveness(df),
        loyalty_segment(df),
        top_product_category(df),
        responsiveness_by_marital_status(df)
    ]


# --- Main Execution ---
if __name__ == "__main__":
    df = load_data()
    for insight in generate_insights(df):
        print(insight)
