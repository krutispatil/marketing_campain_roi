import pandas as pd
import pandasql as psql

# Load & clean dataset
def load_data(path="data/ifood_df.csv"):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]  # normalize col names
    return df

# Run SQL queries
def run_sql(df, query):
    return psql.sqldf(query, locals())

# 1. Campaign Acceptance Rate
def campaign_acceptance(df):
    q = """
    SELECT 
        (CAST(SUM(acceptedcmp1 + acceptedcmp2 + acceptedcmp3 + acceptedcmp4 + acceptedcmp5) AS FLOAT) 
        / (COUNT(*) * 5)) * 100 AS acceptance_rate
    FROM df;
    """
    result = run_sql(df, q).iloc[0, 0]
    return f"✅ Overall campaign acceptance rate is **{result:.1f}%**. Most customers were hard to convert, suggesting sharper targeting is needed."

# 2. Income vs Spending
def income_vs_spending(df):
    q = """
    SELECT 
        CASE WHEN income >= 60000 THEN 'High Income' ELSE 'Low Income' END AS income_group,
        AVG(mntwines + mntmeatproducts + mntgoldprods + mntfishproducts + mntsweetproducts) AS avg_spent
    FROM df
    GROUP BY income_group;
    """
    result = run_sql(df, q)
    hi = result[result['income_group'] == 'High Income']['avg_spent'].values[0]
    lo = result[result['income_group'] == 'Low Income']['avg_spent'].values[0]
    return f"💰 High-income customers spend **${hi:.0f}** on average vs **${lo:.0f}** for low-income. Campaigns should target high-income for premium products."

# 3. Age Group Responsiveness
def age_group_responsiveness(df):
    q = """
    SELECT 
        CASE 
            WHEN (2025 - year_birth) < 30 THEN 'Under 30'
            WHEN (2025 - year_birth) BETWEEN 30 AND 50 THEN '30-50'
            ELSE '50+' 
        END AS age_group,
        AVG(acceptedcmp1 + acceptedcmp2 + acceptedcmp3 + acceptedcmp4 + acceptedcmp5) AS avg_campaigns_accepted
    FROM df
    GROUP BY age_group;
    """
    result = run_sql(df, q)
    best_group = result.sort_values("avg_campaigns_accepted", ascending=False).iloc[0]
    return f"👥 Customers aged **{best_group['age_group']}** are the most responsive, accepting more campaigns on average than other groups."

# 4. Recency vs Engagement
def recency_vs_engagement(df):
    q = """
    SELECT 
        CASE 
            WHEN recency <= 30 THEN 'Active Recently'
            WHEN recency BETWEEN 31 AND 90 THEN 'Moderately Active'
            ELSE 'Dormant'
        END AS activity_segment,
        AVG(acceptedcmp1 + acceptedcmp2 + acceptedcmp3 + acceptedcmp4 + acceptedcmp5) AS avg_accepted
    FROM df
    GROUP BY activity_segment;
    """
    result = run_sql(df, q)
    active = result[result['activity_segment'] == 'Active Recently']['avg_accepted'].values[0]
    dormant = result[result['activity_segment'] == 'Dormant']['avg_accepted'].values[0]
    return f"⏳ Recently active customers accept **{active:.2f} campaigns** on average vs only **{dormant:.2f}** for dormant customers. Retarget recent buyers!"

# 5. Channel Effectiveness
def channel_effectiveness(df):
    q = """
    SELECT 
        AVG(numwebpurchases) AS avg_web,
        AVG(numcatalogpurchases) AS avg_catalog,
        AVG(numstorepurchases) AS avg_store
    FROM df;
    """
    result = run_sql(df, q).iloc[0]
    return f"🌐 Customers buy mostly online (**{result['avg_web']:.1f} avg purchases**) while catalogs underperform (**{result['avg_catalog']:.1f}**). Shift campaigns toward digital channels."
    

# Collect all insights
def generate_insights(df):
    return [
        campaign_acceptance(df),
        income_vs_spending(df),
        age_group_responsiveness(df),
        recency_vs_engagement(df),
        channel_effectiveness(df)
    ]
