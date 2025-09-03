import pandas as pd
from sqlalchemy import create_engine

# 1. Load CSV
df = pd.read_csv("../data/ifood_df.csv")

# 2. Basic Cleaning
df = df.drop_duplicates()
df.columns = [c.lower().replace(" ", "_") for c in df.columns]

# 3. Connect to MySQL
engine = create_engine("mysql+pymysql://root:password@localhost/marketing_db")

# 4. Write to MySQL
df.to_sql("customers", con=engine, if_exists="replace", index=False)

print("✅ Data loaded into MySQL successfully!")
