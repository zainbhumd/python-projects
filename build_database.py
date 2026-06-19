import pandas as pd
import sqlite3

# 1. Connect to SQLite
conn = sqlite3.connect("karachi_housing.db")

# 2. Load your clean CSV files into Pandas
main_properties_df = pd.read_csv(r"C:\Users\Pc\OneDrive\Work\Karachi property.csv")
portions_df = pd.read_csv(r"C:\Users\Pc\OneDrive\Work\Upper and Lower portions.csv")

# 3. Convert them into SQL database tables
main_properties_df.to_sql("main_properties", conn, if_exists="replace", index=False)
portions_df.to_sql("portions", conn, if_exists="replace", index=False)

# 4. Close the connection
conn.close()
