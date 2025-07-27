Vendor Performance Analysis
This project performs an in-depth analysis of vendor and brand performance using inventory and sales data from a SQLite database. It applies data visualization, statistical techniques, and business logic to identify key insights that can drive procurement strategies, vendor negotiations, and pricing decisions.

📁 Project Structure
Data Source: data folder,inventory.db (SQLite database)

Table Used: purchase_price,vendor_invoice,sales,vendor_sales_summary(analyzed)

Tools: pandas, numpy, matplotlib, seaborn, sqlite3, scipy,lookerstudio(instead of Power BI)

🔍 Objectives
Evaluate vendor and brand-level sales and profitability

Identify slow-moving products and excess inventory

Analyze bulk purchasing patterns and their impact on cost

Determine underperforming brands with high margin potential

Apply statistical testing to compare vendor performance

📊 Key Analyses Performed
1. Exploratory Data Analysis (EDA)
Descriptive statistics and distribution plots

Box plots and histograms to visualize skewness and outliers

Heatmap to uncover correlations between key metrics

2. Brand Optimization Strategy
Identify brands with:

Low Sales (bottom 15%)

High Profit Margins (top 15%)

Target these for promotional strategies or dynamic pricing

3. Top Vendors & Brands
Ranked vendors and brands by total sales

Visualized using annotated bar charts

Applied currency formatting for readability (K, M)

4. Vendor Purchase Contribution (Pareto Analysis)
Calculated % contribution of each vendor to total purchase dollars

Plotted Pareto chart with cumulative contribution

Revealed that Top 10 vendors account for most purchasing

5. Bulk Purchase Impact on Cost
Compared unit price across order sizes (Small, Medium, Large)

Result: Larger orders significantly reduce per-unit cost

6. Inventory & Capital Efficiency
Identified vendors with:

Low stock turnover (<1)

High unsold inventory value

Visualized locked capital per vendor

7. Profitability Confidence Intervals
Compared 95% confidence intervals for profit margins:

Top-performing vendors vs. Low-performing vendors

Revealed interesting trade-off: higher margin ≠ higher sales

8. Hypothesis Testing (T-Test)
Tested if mean profit margins between top and low performers are significantly different

Result: Statistically significant difference (p < 0.05)

📌 Key Insights
📉 Some vendors show low turnover, locking capital in unsold inventory.

💸 Bulk buying reduces unit costs by up to 72%, boosting profit margins.

📈 Low-selling brands with high margins are ripe for targeted promotion.

🧮 Top vendors dominate procurement — ideal candidates for renegotiation.

📊 Data-backed insights support smarter purchasing and pricing strategies.

🛠️ Technologies Used
Tool	Purpose
pandas	Data loading and transformation
numpy	Numerical calculations
matplotlib	Static plotting
seaborn	Advanced visualizations
sqlite3	Database connection
scipy.stats	Statistical testing

How to Run
Clone the Repository

bash
Copy code
git clone https://github.com/Sun10ny/Vendor-Performance-Analysis.git

cd Vendor-Performance-Analysis
Download Required Files

The data/ folder and inventory.db file are not included in the GitHub repo due to size limitations.

Download them from the following Google Drive link:

https://drive.google.com/drive/folders/1uQVu16lDHaP-iVPp5aKDiW6Rzr4i0Ye_?usp=sharing

After downloading, place both the data/ folder and inventory.db file in the project’s root directory (Vendor-Performance-Analysis/).

Install required Dependencies


