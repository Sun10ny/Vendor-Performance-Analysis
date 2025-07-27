import sqlite3
import pandas as pd

# Connect to uploaded DB file
conn = sqlite3.connect("inventory.db")

# Load the data from vendor_sales_summary table
df = pd.read_sql_query("SELECT * FROM vendor_sales_summary", conn)

# Export to CSV
df.to_csv("vendor_sales_summary.csv", index=False)

# Close the connection
conn.close()

print("Export successful! File saved as vendor_sales_summary.csv")