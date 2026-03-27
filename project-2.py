"""
================================================================================
STEP 2: ADVANCED ANALYSIS, VISUALIZATIONS & REPORT GENERATION
================================================================================
This script performs:
✓ Complex data analysis on sales data
✓ Creates multiple visualizations (charts, graphs)
✓ Generates comprehensive reports
✓ Exports to Excel and HTML
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# ============================================================================
# SETUP: Configure visualization style
# ============================================================================

sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 80)
print("STEP 2: ADVANCED ANALYSIS, VISUALIZATIONS & REPORT GENERATION")
print("=" * 80)

# ============================================================================
# SECTION 1: LOAD AND PREPARE DATA
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 1: LOADING DATA")
print("=" * 80)

# Load the CSV files created in Step 1
try:
    sales_df = pd.read_csv('sales_data.csv')
    customers_df = pd.read_csv('customers_data.csv')
    print("\n✓ Data loaded successfully!")
    print(f"  - Sales records: {len(sales_df)}")
    print(f"  - Customers: {len(customers_df)}")
except FileNotFoundError:
    print("❌ Error: CSV files not found. Run project-1.py first!")
    exit()

# Convert date columns to datetime
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
customers_df['join_date'] = pd.to_datetime(customers_df['join_date'])

# Merge data for analysis
merged_df = pd.merge(sales_df, customers_df, on='customer_id', how='inner')

print("\n✓ Data prepared and merged successfully!")


# ============================================================================
# SECTION 2: COMPLEX DATA ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 2: ANALYZING DATA")
print("=" * 80)

# 2.1: Customer Analysis
print("\n📊 CUSTOMER ANALYSIS:")
customer_analysis = merged_df.groupby('customer_name').agg({
    'sale_id': 'count',
    'amount': ['sum', 'mean', 'min', 'max']
}).round(2)
customer_analysis.columns = ['Total Orders', 'Total Spent', 'Avg Order Value', 'Min Purchase', 'Max Purchase']
customer_analysis = customer_analysis.sort_values('Total Spent', ascending=False)
print(customer_analysis)

# 2.2: Product Analysis
print("\n📊 PRODUCT ANALYSIS:")
product_analysis = merged_df.groupby('product_name').agg({
    'sale_id': 'count',
    'amount': ['sum', 'mean']
}).round(2)
product_analysis.columns = ['Units Sold', 'Total Revenue', 'Avg Price']
product_analysis = product_analysis.sort_values('Total Revenue', ascending=False)
print(product_analysis)

# 2.3: City Analysis
print("\n📊 CITY ANALYSIS:")
city_analysis = merged_df.groupby('city').agg({
    'customer_id': 'nunique',
    'sale_id': 'count',
    'amount': ['sum', 'mean']
}).round(2)
city_analysis.columns = ['Unique Customers', 'Total Orders', 'Total Revenue', 'Avg Order']
city_analysis = city_analysis.sort_values('Total Revenue', ascending=False)
print(city_analysis)

# 2.4: Time-based Analysis
print("\n📊 TIME-BASED ANALYSIS:")
merged_df['year_month'] = merged_df['sale_date'].dt.to_period('M')
time_analysis = merged_df.groupby('year_month').agg({
    'sale_id': 'count',
    'amount': 'sum'
}).round(2)
time_analysis.columns = ['Number of Orders', 'Revenue']
print(time_analysis)

# 2.5: Statistical Summary
print("\n📊 STATISTICAL SUMMARY:")
print(f"\nTotal Revenue: ${merged_df['amount'].sum():,.2f}")
print(f"Average Transaction Value: ${merged_df['amount'].mean():.2f}")
print(f"Median Transaction Value: ${merged_df['amount'].median():.2f}")
print(f"Standard Deviation: ${merged_df['amount'].std():.2f}")
print(f"Revenue Range: ${merged_df['amount'].min():.2f} - ${merged_df['amount'].max():.2f}")

# 2.6: Customer Segmentation by Spend
print("\n📊 CUSTOMER SEGMENTATION (By Spending):")
customer_spending = merged_df.groupby('customer_id')['amount'].sum()
high_value = len(customer_spending[customer_spending > 1000])
medium_value = len(customer_spending[(customer_spending >= 500) & (customer_spending <= 1000)])
low_value = len(customer_spending[customer_spending < 500])

print(f"High Value (>$1000): {high_value} customers")
print(f"Medium Value ($500-$1000): {medium_value} customers")
print(f"Low Value (<$500): {low_value} customers")


# ============================================================================
# SECTION 3: CREATE VISUALIZATIONS
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 3: CREATING VISUALIZATIONS")
print("=" * 80)

# Create directory for charts
os.makedirs('visualizations', exist_ok=True)
print("\n✓ Visualizations directory created")

# 3.1: Revenue by Product (Bar Chart)
print("\n📈 Chart 1: Product Performance (Bar Chart)")
fig, ax = plt.subplots(figsize=(10, 6))
product_revenue = merged_df.groupby('product_name')['amount'].sum().sort_values(ascending=False)
colors = sns.color_palette("husl", len(product_revenue))
bars = ax.bar(product_revenue.index, product_revenue.values, color=colors)
ax.set_title('Total Revenue by Product', fontsize=16, fontweight='bold')
ax.set_xlabel('Product Name', fontsize=12)
ax.set_ylabel('Revenue ($)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:,.0f}',
            ha='center', va='bottom', fontsize=10)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visualizations/01_product_revenue.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/01_product_revenue.png")
plt.close()

# 3.2: Customer Performance (Top 10)
print("\n📈 Chart 2: Top Customers (Horizontal Bar Chart)")
fig, ax = plt.subplots(figsize=(10, 6))
top_customers = merged_df.groupby('customer_name')['amount'].sum().sort_values(ascending=True).tail(10)
colors = sns.color_palette("RdYlGn", len(top_customers))
bars = ax.barh(top_customers.index, top_customers.values, color=colors)
ax.set_title('Top 10 Customers by Spending', fontsize=16, fontweight='bold')
ax.set_xlabel('Total Spending ($)', fontsize=12)
ax.grid(axis='x', alpha=0.3)
# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'${width:,.0f}',
            ha='left', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('visualizations/02_top_customers.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/02_top_customers.png")
plt.close()

# 3.3: Sales Distribution (Histogram)
print("\n📈 Chart 3: Sales Distribution (Histogram)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(merged_df['amount'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
ax.axvline(merged_df['amount'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${merged_df["amount"].mean():.2f}')
ax.axvline(merged_df['amount'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: ${merged_df["amount"].median():.2f}')
ax.set_title('Distribution of Transaction Amounts', fontsize=16, fontweight='bold')
ax.set_xlabel('Amount ($)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/03_sales_distribution.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/03_sales_distribution.png")
plt.close()

# 3.4: Revenue by City (Pie Chart)
print("\n📈 Chart 4: Revenue Distribution by City (Pie Chart)")
fig, ax = plt.subplots(figsize=(10, 8))
city_revenue = merged_df.groupby('city')['amount'].sum()
colors = sns.color_palette("Set2", len(city_revenue))
wedges, texts, autotexts = ax.pie(city_revenue.values, 
                                    labels=city_revenue.index,
                                    autopct='%1.1f%%',
                                    colors=colors,
                                    startangle=90)
ax.set_title('Revenue Distribution by City', fontsize=16, fontweight='bold')
# Make percentage text bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
plt.tight_layout()
plt.savefig('visualizations/04_revenue_by_city_pie.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/04_revenue_by_city_pie.png")
plt.close()

# 3.5: Orders by City (Bar Chart)
print("\n📈 Chart 5: Number of Orders by City (Bar Chart)")
fig, ax = plt.subplots(figsize=(10, 6))
city_orders = merged_df.groupby('city')['sale_id'].count().sort_values(ascending=False)
colors = sns.color_palette("coolwarm", len(city_orders))
bars = ax.bar(city_orders.index, city_orders.values, color=colors)
ax.set_title('Number of Orders by City', fontsize=16, fontweight='bold')
ax.set_xlabel('City', fontsize=12)
ax.set_ylabel('Number of Orders', fontsize=12)
ax.grid(axis='y', alpha=0.3)
# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=10)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visualizations/05_orders_by_city.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/05_orders_by_city.png")
plt.close()

# 3.6: Product Mix (Units Sold)
print("\n📈 Chart 6: Product Mix by Units Sold (Donut Chart)")
fig, ax = plt.subplots(figsize=(10, 8))
product_units = merged_df.groupby('product_name')['sale_id'].count().sort_values(ascending=False)
colors = sns.color_palette("husl", len(product_units))
wedges, texts, autotexts = ax.pie(product_units.values,
                                    labels=product_units.index,
                                    autopct='%1.1f%%',
                                    colors=colors,
                                    pctdistance=0.85)
# Create donut hole
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
ax.add_artist(centre_circle)
ax.set_title('Product Mix (Units Sold)', fontsize=16, fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
plt.tight_layout()
plt.savefig('visualizations/06_product_mix_donut.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/06_product_mix_donut.png")
plt.close()

# 3.7: Customer Purchase Frequency
print("\n📈 Chart 7: Customer Purchase Frequency (Scatter Plot)")
fig, ax = plt.subplots(figsize=(10, 6))
customer_freq = merged_df.groupby('customer_name').agg({
    'sale_id': 'count',
    'amount': 'sum'
})
scatter = ax.scatter(customer_freq['sale_id'], customer_freq['amount'], 
                     s=200, alpha=0.6, c=range(len(customer_freq)), cmap='viridis')
ax.set_title('Customer Purchase Frequency vs Total Spending', fontsize=16, fontweight='bold')
ax.set_xlabel('Number of Purchases', fontsize=12)
ax.set_ylabel('Total Spending ($)', fontsize=12)
ax.grid(True, alpha=0.3)
# Add customer labels
for idx, row in customer_freq.iterrows():
    ax.annotate(idx, (row['sale_id'], row['amount']), 
                fontsize=9, alpha=0.7)
plt.tight_layout()
plt.savefig('visualizations/07_purchase_frequency.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/07_purchase_frequency.png")
plt.close()

# 3.8: Timeline (Sales over time)
print("\n📈 Chart 8: Sales Timeline (Line Chart)")
fig, ax = plt.subplots(figsize=(12, 6))
daily_sales = merged_df.groupby('sale_date')['amount'].agg(['sum', 'count'])
ax.plot(daily_sales.index, daily_sales['sum'], marker='o', linewidth=2, 
        markersize=8, color='#2E86AB', label='Daily Revenue')
ax.fill_between(daily_sales.index, daily_sales['sum'], alpha=0.3, color='#2E86AB')
ax.set_title('Daily Sales Revenue Timeline', fontsize=16, fontweight='bold')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Revenue ($)', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/08_sales_timeline.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/08_sales_timeline.png")
plt.close()

# 3.9: Heatmap - Product vs City
print("\n📈 Chart 9: Product-City Heatmap")
fig, ax = plt.subplots(figsize=(10, 6))
heatmap_data = pd.crosstab(merged_df['product_name'], merged_df['city'], values=merged_df['amount'], aggfunc='sum')
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Revenue ($)'})
ax.set_title('Revenue Heatmap: Product vs City', fontsize=16, fontweight='bold')
ax.set_xlabel('City', fontsize=12)
ax.set_ylabel('Product', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/09_product_city_heatmap.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: visualizations/09_product_city_heatmap.png")
plt.close()

print("\n✓ All 9 visualizations created successfully!")


# ============================================================================
# SECTION 4: GENERATE REPORTS
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 4: GENERATING REPORTS")
print("=" * 80)

# 4.1: Create Summary Report (Text)
print("\n📄 Creating Text Summary Report...")

report_text = f"""
{'='*80}
COMPREHENSIVE SALES ANALYSIS REPORT
{'='*80}
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

{'='*80}
EXECUTIVE SUMMARY
{'='*80}

Total Revenue:                ${merged_df['amount'].sum():,.2f}
Total Transactions:           {len(merged_df)}
Average Transaction Value:    ${merged_df['amount'].mean():.2f}
Median Transaction Value:     ${merged_df['amount'].median():.2f}
Standard Deviation:           ${merged_df['amount'].std():.2f}
Revenue Range:                ${merged_df['amount'].min():.2f} - ${merged_df['amount'].max():.2f}

Total Customers:              {customers_df['customer_id'].nunique()}
Total Products:               {merged_df['product_name'].nunique()}
Number of Cities:             {merged_df['city'].nunique()}

Date Range:                   {merged_df['sale_date'].min().date()} to {merged_df['sale_date'].max().date()}


{'='*80}
TOP PERFORMERS
{'='*80}

TOP 3 PRODUCTS BY REVENUE:
"""

top_products = merged_df.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(3)
for idx, (product, revenue) in enumerate(top_products.items(), 1):
    units = len(merged_df[merged_df['product_name'] == product])
    avg_price = revenue / units
    report_text += f"\n{idx}. {product:20s} | Revenue: ${revenue:>10,.2f} | Units: {units:>2d} | Avg Price: ${avg_price:>8,.2f}"

report_text += f"\n\nTOP 3 CUSTOMERS BY SPENDING:\n"
top_customers = merged_df.groupby('customer_name')['amount'].sum().sort_values(ascending=False).head(3)
for idx, (customer, spending) in enumerate(top_customers.items(), 1):
    orders = len(merged_df[merged_df['customer_name'] == customer])
    avg_order = spending / orders
    report_text += f"\n{idx}. {customer:20s} | Spent: ${spending:>10,.2f} | Orders: {orders:>2d} | Avg Order: ${avg_order:>8,.2f}"

report_text += f"\n\nTOP 3 CITIES BY REVENUE:\n"
top_cities = merged_df.groupby('city')['amount'].sum().sort_values(ascending=False).head(3)
for idx, (city, revenue) in enumerate(top_cities.items(), 1):
    customers = merged_df[merged_df['city'] == city]['customer_id'].nunique()
    transactions = len(merged_df[merged_df['city'] == city])
    report_text += f"\n{idx}. {city:20s} | Revenue: ${revenue:>10,.2f} | Customers: {customers:>2d} | Orders: {transactions:>2d}"

report_text += f"""

{'='*80}
CUSTOMER SEGMENTATION
{'='*80}

High Value Customers (>$1000):    {high_value} customers ({high_value/len(customers_df)*100:.1f}%)
Medium Value Customers ($500-1000): {medium_value} customers ({medium_value/len(customers_df)*100:.1f}%)
Low Value Customers (<$500):      {low_value} customers ({low_value/len(customers_df)*100:.1f}%)

{'='*80}
PRODUCT ANALYSIS
{'='*80}

"""

for product in merged_df['product_name'].unique():
    product_data = merged_df[merged_df['product_name'] == product]
    report_text += f"\n{product}:\n"
    report_text += f"  - Units Sold: {len(product_data)}\n"
    report_text += f"  - Total Revenue: ${product_data['amount'].sum():,.2f}\n"
    report_text += f"  - Average Price: ${product_data['amount'].mean():.2f}\n"
    report_text += f"  - Price Range: ${product_data['amount'].min():.2f} - ${product_data['amount'].max():.2f}\n"

report_text += f"""

{'='*80}
GEOGRAPHIC ANALYSIS
{'='*80}

"""

for city in merged_df['city'].unique():
    city_data = merged_df[merged_df['city'] == city]
    report_text += f"\n{city}:\n"
    report_text += f"  - Customers: {city_data['customer_id'].nunique()}\n"
    report_text += f"  - Orders: {len(city_data)}\n"
    report_text += f"  - Total Revenue: ${city_data['amount'].sum():,.2f}\n"
    report_text += f"  - Average Order Value: ${city_data['amount'].mean():.2f}\n"

report_text += f"""

{'='*80}
KEY INSIGHTS & RECOMMENDATIONS
{'='*80}

1. REVENUE CONCENTRATION:
   The top 3 products account for {(top_products.sum()/merged_df['amount'].sum()*100):.1f}% of total revenue.
   Focus on maintaining stock and quality of high-performing products.

2. CUSTOMER VALUE:
   {high_value} customer(s) ({high_value/len(customers_df)*100:.1f}%) are high-value spending more than $1,000.
   Implement loyalty programs to retain these key customers.

3. GEOGRAPHIC PERFORMANCE:
   {top_cities.index[0]} is the strongest market with {top_cities.values[0]:,.2f} in revenue.
   Consider expansion strategies for lower-performing cities.

4. SALES PATTERN:
   Average transaction value is ${merged_df['amount'].mean():.2f}.
   Standard deviation of ${merged_df['amount'].std():.2f} indicates variable purchase amounts.

5. PRODUCT DIVERSITY:
   With {merged_df['product_name'].nunique()} products, the portfolio is well-diversified.
   Monitor underperforming products for potential discontinuation.

{'='*80}
DETAILED CUSTOMER ANALYSIS
{'='*80}

"""

for customer in sorted(merged_df['customer_name'].unique()):
    customer_data = merged_df[merged_df['customer_name'] == customer]
    report_text += f"\n{customer}:\n"
    report_text += f"  - Total Purchases: {len(customer_data)}\n"
    report_text += f"  - Total Spent: ${customer_data['amount'].sum():,.2f}\n"
    report_text += f"  - Average Purchase: ${customer_data['amount'].mean():.2f}\n"
    report_text += f"  - Highest Purchase: ${customer_data['amount'].max():.2f}\n"
    report_text += f"  - Last Purchase: {customer_data['sale_date'].max().date()}\n"

report_text += f"""

{'='*80}
END OF REPORT
{'='*80}
This report was automatically generated and contains insights from {len(merged_df)} transactions.
For questions or clarifications, please refer to the detailed analysis files.
"""

# Save text report
with open('SALES_ANALYSIS_REPORT.txt', 'w') as f:
    f.write(report_text)
print("   ✓ Saved: SALES_ANALYSIS_REPORT.txt")

# Print to console
print("\n" + report_text)

# 4.2: Export to Excel
print("\n📊 Creating Excel Report with multiple sheets...")

try:
    with pd.ExcelWriter('SALES_ANALYSIS_REPORT.xlsx', engine='openpyxl') as writer:
        # Sheet 1: Raw Sales Data
        sales_df.to_excel(writer, sheet_name='Sales Data', index=False)
        
        # Sheet 2: Customer Data
        customers_df.to_excel(writer, sheet_name='Customers', index=False)
        
        # Sheet 3: Customer Analysis
        customer_analysis.to_excel(writer, sheet_name='Customer Analysis')
        
        # Sheet 4: Product Analysis
        product_analysis.to_excel(writer, sheet_name='Product Analysis')
        
        # Sheet 5: City Analysis
        city_analysis.to_excel(writer, sheet_name='City Analysis')
        
        # Sheet 6: Summary Statistics
        summary_stats = pd.DataFrame({
            'Metric': [
                'Total Revenue', 'Total Transactions', 'Average Transaction',
                'Median Transaction', 'Standard Deviation', 'Min Transaction',
                'Max Transaction', 'Total Customers', 'Total Products',
                'Total Cities'
            ],
            'Value': [
                f"${merged_df['amount'].sum():,.2f}",
                len(merged_df),
                f"${merged_df['amount'].mean():.2f}",
                f"${merged_df['amount'].median():.2f}",
                f"${merged_df['amount'].std():.2f}",
                f"${merged_df['amount'].min():.2f}",
                f"${merged_df['amount'].max():.2f}",
                customers_df['customer_id'].nunique(),
                merged_df['product_name'].nunique(),
                merged_df['city'].nunique()
            ]
        })
        summary_stats.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sheet 7: Crosstab - Product vs City
        crosstab_data = pd.crosstab(merged_df['product_name'], merged_df['city'], 
                                     values=merged_df['amount'], aggfunc='sum')
        crosstab_data.to_excel(writer, sheet_name='Product-City Crosstab')
    
    print("   ✓ Saved: SALES_ANALYSIS_REPORT.xlsx")
except Exception as e:
    print(f"   ⚠ Could not save Excel file: {e}")
    print("   Install openpyxl with: pip install openpyxl")


# 4.3: Create HTML Report
print("\n📄 Creating HTML Report...")

html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Sales Analysis Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        .metric {{
            display: inline-block;
            width: 22%;
            margin: 10px 1%;
            padding: 15px;
            background-color: #ecf0f1;
            border-radius: 5px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2980b9;
        }}
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 10px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .visualization {{
            margin: 20px 0;
            text-align: center;
        }}
        .visualization img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Sales Analysis Report</h1>
        <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        
        <h2>Key Metrics</h2>
        <div class="metric">
            <div class="metric-value">${merged_df['amount'].sum():,.0f}</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        <div class="metric">
            <div class="metric-value">{len(merged_df)}</div>
            <div class="metric-label">Transactions</div>
        </div>
        <div class="metric">
            <div class="metric-value">${merged_df['amount'].mean():.0f}</div>
            <div class="metric-label">Avg Transaction</div>
        </div>
        <div class="metric">
            <div class="metric-value">{len(customers_df)}</div>
            <div class="metric-label">Customers</div>
        </div>
        
        <h2>Product Performance</h2>
        <table>
            <tr>
                <th>Product</th>
                <th>Units Sold</th>
                <th>Total Revenue</th>
                <th>Average Price</th>
            </tr>
"""

for product in merged_df['product_name'].unique():
    product_data = merged_df[merged_df['product_name'] == product]
    units = len(product_data)
    revenue = product_data['amount'].sum()
    avg_price = product_data['amount'].mean()
    html_report += f"""
            <tr>
                <td>{product}</td>
                <td>{units}</td>
                <td>${revenue:,.2f}</td>
                <td>${avg_price:.2f}</td>
            </tr>
"""

html_report += """
        </table>
        
        <h2>Top Customers</h2>
        <table>
            <tr>
                <th>Customer</th>
                <th>Orders</th>
                <th>Total Spent</th>
                <th>Avg Order Value</th>
            </tr>
"""

for customer in top_customers.head(5).index:
    customer_data = merged_df[merged_df['customer_name'] == customer]
    html_report += f"""
            <tr>
                <td>{customer}</td>
                <td>{len(customer_data)}</td>
                <td>${customer_data['amount'].sum():,.2f}</td>
                <td>${customer_data['amount'].mean():.2f}</td>
            </tr>
"""

html_report += """
        </table>
        
        <h2>Visualizations</h2>
"""

# Add visualizations to HTML
viz_files = [
    ('01_product_revenue.png', 'Product Revenue'),
    ('02_top_customers.png', 'Top Customers'),
    ('03_sales_distribution.png', 'Sales Distribution'),
    ('04_revenue_by_city_pie.png', 'Revenue by City'),
    ('05_orders_by_city.png', 'Orders by City'),
    ('06_product_mix_donut.png', 'Product Mix'),
    ('07_purchase_frequency.png', 'Purchase Frequency'),
    ('08_sales_timeline.png', 'Sales Timeline'),
    ('09_product_city_heatmap.png', 'Product-City Heatmap'),
]

for viz_file, viz_title in viz_files:
    html_report += f"""
        <div class="visualization">
            <h3>{viz_title}</h3>
            <img src="visualizations/{viz_file}" alt="{viz_title}">
        </div>
"""

html_report += f"""
        <div class="footer">
            <p>This report was automatically generated from {len(merged_df)} sales transactions.</p>
            <p>For more details, see the accompanying Excel file and visualizations folder.</p>
        </div>
    </div>
</body>
</html>
"""

with open('SALES_ANALYSIS_REPORT.html', 'w') as f:
    f.write(html_report)
print("   ✓ Saved: SALES_ANALYSIS_REPORT.html")


# ============================================================================
# COMPLETION
# ============================================================================

print("\n" + "=" * 80)
print("✅ STEP 2 COMPLETE - ALL REPORTS GENERATED SUCCESSFULLY!")
print("=" * 80)

print("\n📁 FILES CREATED:")
print("   ✓ SALES_ANALYSIS_REPORT.txt - Text summary report")
print("   ✓ SALES_ANALYSIS_REPORT.xlsx - Excel workbook with multiple sheets")
print("   ✓ SALES_ANALYSIS_REPORT.html - Interactive HTML report")
print("   ✓ visualizations/ folder - 9 high-quality charts (PNG)")

print("\n🎯 DELIVERABLES SUMMARY:")
print("   ✓ Complex Data Analysis - Customer, Product, Geographic, Time-based")
print("   ✓ 9 Professional Visualizations - Bar, Pie, Histogram, Heatmap, Timeline")
print("   ✓ 3 Report Formats - Text, Excel, HTML")
print("   ✓ Key Insights & Recommendations")

print("\n📂 NEXT STEPS:")
print("   1. Open SALES_ANALYSIS_REPORT.html in your browser to view the interactive report")
print("   2. Open SALES_ANALYSIS_REPORT.xlsx in Excel for detailed data analysis")
print("   3. Check visualizations/ folder for individual charts")
print("   4. Read SALES_ANALYSIS_REPORT.txt for detailed insights")

print("\n" + "=" * 80)
