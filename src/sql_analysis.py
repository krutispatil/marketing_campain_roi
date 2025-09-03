import pandas as pd
from sqlalchemy import create_engine

# Connect to MySQL
engine = create_engine("mysql+pymysql://root:password@localhost/marketing_db")

# Example: Campaign acceptance rate
query = """
SELECT 
    (SUM(acceptedcmp1 + acceptedcmp2 + acceptedcmp3 + acceptedcmp4 + acceptedcmp5)) 
    / COUNT(*) AS avg_acceptance_rate
FROM customers;
"""
result = pd.read_sql(query, engine)
print("📊 Campaign Acceptance Rate:")
print(result)

# Example: Revenue by product category
query2 = """
SELECT 
    AVG(mntwines) AS avg_wine_spent,
    AVG(mntmeatproducts) AS avg_meat_spent,
    AVG(mntgoldprods) AS avg_gold_spent
FROM customers;
"""
result2 = pd.read_sql(query2, engine)
print("\n📊 Avg Spending by Category:")
print(result2)
