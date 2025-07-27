import pandas as pd
import sqlite3
import time

conn=sqlite3.connect('inventory.db')

tables=pd.read_sql_query("SELECT name from sqlite_master where type='table'",conn)


for table in tables['name']:
    print('-'*50,f'{table}','-'*50)
    print('Count of records:',pd.read_sql(f"select count(*) as count from {table}",conn)['count'].values[0])
    pd.read_sql(f"select * from {table} limit 5",conn)

purchases=pd.read_sql_query("select * from purchases where VendorNumber=4466",conn)
print(purchases)
purchase_prices=pd.read_sql_query("select * from purchase_prices where VendorNumber=4466",conn)
print(purchase_prices)
vendor_invoice=pd.read_sql_query("select * from vendor_invoice where VendorNumber=4466",conn)
print(vendor_invoice)
sales=pd.read_sql_query("select * from sales where VendorNo=4466",conn)
print(sales)

print(purchases.groupby(['Brand','PurchasePrice'])[['Quantity','Dollars']].sum())

print(vendor_invoice['PONumber'].nunique())

print(sales.groupby('Brand')[['SalesDollars','SalesPrice','SalesQuantity']].sum())

'''The purchases table contains actual purchase data, including the date of purchase, products (brands) purchased by vendors, the amount paid (in dollars), and the quantity purchased.

The purchase price column is derived from the purchase_prices table, which provides product-wise actual and purchase prices. The combination of vendor and brand is unique in this table.

The vendor_invoice table aggregates data from the purchases table, summarizing quantity and dollar amounts, along with an additional column for freight. This table maintains uniqueness based on vendor and PO number.

The sales table captures actual sales transactions, detailing the brands purchased by vendors, the quantity sold, the selling price, and the revenue earned.

As the data that we need for analysis is distributed in different tables, we need to create a summary table containing:

purchase transactions made by vendors

sales transaction data

freight costs for each vendor'''

freight_summary=pd.read_sql_query("select VendorNumber, SUM(Freight) as FreightCost From vendor_invoice Group by VendorNumber",conn)
print(freight_summary)

pd.read_sql("select p.VendorNumber,p.VendorName, p.Brand, p.PurchasePrice, pp.Volume ,pp.Price as ActualPrice, SUM(p.Quantity) as TotalPurchaseQuantity, SUM(p.Dollars) as TotalPurchaseDollars FROM purchases p JOIN purchase_prices pp ON p.Brand = pp.Brand where p.PurchasePrice>0 GROUP BY p.VendorNumber, p.VendorName, p.Brand ORDER BY TotalPurchaseDollars",conn)

pd.read_sql_query("select VendorNo,Brand,SUM(SalesDollars) as TotalSalesDollars, SUM(SalesPrice) as TotalSalesPrice, SUM(SalesQuantity) as TotalSalesQuantity, SUM(ExciseTax) as TotalExciseTax From sales Group BY VendorNo,Brand ORDER BY TotalSalesDollars",conn)

vendor_sales_summary=pd.read_sql_query("WITH FreightSummary AS ( SELECT VendorNumber, SUM(Freight) AS FreightCost FROM vendor_invoice GROUP BY VendorNumber),   PurchaseSummary AS (SELECT p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price AS ActualPrice, pp.Volume, SUM(p.Quantity) AS TotalPurchaseQuantity, SUM(p.Dollars) AS TotalPurchaseDollars FROM purchases p JOIN purchase_prices pp ON p.Brand = pp.Brand WHERE p.PurchasePrice > 0 GROUP BY  p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume),SalesSummary AS (SELECT VendorNo, Brand, SUM(SalesQuantity) AS TotalSalesQuantity, SUM(SalesDollars) AS TotalSalesDollars, SUM(SalesPrice) AS TotalSalesPrice, SUM(ExciseTax) AS TotalExciseTax FROM sales GROUP BY VendorNo, Brand) SELECT ps.VendorNumber, ps.VendorName, ps.Brand, ps.Description, ps.PurchasePrice, ps.ActualPrice, ps.Volume, ps.TotalPurchaseQuantity, ps.TotalPurchaseDollars, ss.TotalSalesQuantity, ss.TotalSalesDollars, ss.TotalSalesPrice, ss.TotalExciseTax, fs.FreightCost FROM PurchaseSummary ps LEFT JOIN SalesSummary ss ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand LEFT JOIN FreightSummary fs ON ps.VendorNumber = fs.VendorNumber ORDER BY ps.TotalPurchaseDollars DESC",conn)
print(vendor_sales_summary)

'''Notebook Section: Performance Optimization
This query generates a vendor-wise sales and purchase summary, which is valuable for:

Performance Optimization Points
The query involves heavy joins and aggregations on large datasets like sales and purchases.

Storing the pre-aggregated results avoids repeated expensive computations.

Helps in analyzing sales, purchases, and pricing for different vendors and brands.

There are future benefits of storing this data for faster dashboarding and reporting.

Instead of running expensive queries each time, dashboards can fetch data quickly from the vendor_sales_summary.

Key Points:

The main query creates a summary table for efficient vendor sales and purchases reporting.

Performance is improved by reducing repeated heavy computations.

Storing summaries allows for quicker, more scalable analysis and dashboard use.

Analyzing this summary data helps with strategic business decisions regarding vendors and brands.'''

vendor_sales_summary.dtypes
vendor_sales_summary.isnull().sum()

vendor_sales_summary['Volume']=vendor_sales_summary['Volume'].astype('float64')
vendor_sales_summary.fillna(0,inplace=True)
vendor_sales_summary['VendorName']=vendor_sales_summary['VendorName'].str.strip()
vendor_sales_summary['VendorName'].unique()

vendor_sales_summary['GrossProfit']=vendor_sales_summary['TotalSalesDollars']-vendor_sales_summary["TotalPurchaseDollars"]
print(vendor_sales_summary['GrossProfit'].min())

vendor_sales_summary['ProfitMargin'] = (vendor_sales_summary['GrossProfit'] / vendor_sales_summary['TotalSalesDollars'])*100

vendor_sales_summary['StockTurnover']=vendor_sales_summary['TotalSalesQuantity']/vendor_sales_summary["TotalPurchaseQuantity"]

vendor_sales_summary['SalestoPurchaseRatio']=vendor_sales_summary['TotalSalesDollars']/vendor_sales_summary["TotalPurchaseDollars"]

cursor=conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS vendor_sales_summary (
    VendorNumber INT,
    VendorName VARCHAR(100),
    Brand INT,
    Description VARCHAR(100),
    PurchasePrice DECIMAL(10,2),
    ActualPrice DECIMAL(10,2),
    Volume ,
    TotalPurchaseQuantity INT,
    TotalPurchaseDollars DECIMAL(15,2),
    TotalSalesQuantity INT,
    TotalSalesDollars DECIMAL(15,2),
    TotalSalesPrice DECIMAL(15,2),
    TotalExciseTax DECIMAL(15,2),
    FreightCost DECIMAL(15,2),
    GrossProfit DECIMAL(15,2),
    ProfitMargin DECIMAL(15,2),
    StockTurnover DECIMAL(15,2),
    SalesToPurchaseRatio DECIMAL(15,2),
    PRIMARY KEY (VendorNumber, Brand)
);
               """)

print(pd.read_sql_query("SELECT * FROM vendor_sales_summary", conn))
print(vendor_sales_summary.to_sql('vendor_sales_summary', conn, if_exists='replace', index=False))