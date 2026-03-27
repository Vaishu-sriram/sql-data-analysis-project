"""
================================================================================
BEGINNER'S GUIDE TO: SQL + DATA CLEANING + ANALYSIS
================================================================================
This is STEP 1: Learning Data Basics & Creating Sample Sales Data

WHAT YOU NEED TO KNOW:
- Pandas = A Python library for working with data (like Excel but more powerful)
- DataFrame = A table with rows and columns (like Excel spreadsheet)
- This script will teach you by doing!
================================================================================
"""

# First, we need to import libraries (tools we'll use)
# Think of it like: "Hey Python, please load these power tools for me"
import pandas as pd  # This is for data manipulation (cleaning, analyzing)
import numpy as np   # This is for numbers and calculations
from datetime import datetime, timedelta  # For working with dates

print("=" * 80)
print("STEP 1: CREATING SAMPLE SALES DATA")
print("=" * 80)

# ============================================================================
# SECTION 1: CREATE SAMPLE DATA
# ============================================================================

# Let's pretend we have a store with customers and sales
# We'll create fake but realistic data to practice with

# Create sample customers
customers = {
    'customer_id': [101, 102, 103, 104, 105, 106, 107, 108],
    'customer_name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'city': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Los Angeles', 'New York', 'Chicago', 'Boston'],
    'join_date': ['2023-01-15', '2023-02-20', '2023-01-10', '2023-03-05', '2023-02-14', '2023-01-20', '2023-03-01', '2023-02-28']
}

# Create sample sales transactions
sales = {
    'sale_id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    'customer_id': [101, 102, 101, 103, 104, 102, 105, 101, 103, 106],
    'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'USB Cable', 'Headphones', 'Monitor', 'Keyboard', 'Laptop'],
    'amount': [1200, 25, 75, 300, 1200, 10, 80, 300, 75, 1200],
    'sale_date': ['2024-01-10', '2024-01-12', '2024-01-15', '2024-01-18', '2024-01-20', 
                   '2024-02-05', '2024-02-10', '2024-02-15', '2024-02-20', '2024-03-01']
}

# Convert these dictionaries into DataFrames (tables)
# A DataFrame is like an Excel spreadsheet - it has rows and columns
customers_df = pd.DataFrame(customers)
sales_df = pd.DataFrame(sales)

print("\n📊 CUSTOMERS TABLE:")
print(customers_df)
print(f"\nShape: {customers_df.shape[0]} rows, {customers_df.shape[1]} columns")

print("\n" + "=" * 80)
print("\n📊 SALES TABLE:")
print(sales_df)
print(f"\nShape: {sales_df.shape[0]} rows, {sales_df.shape[1]} columns")


# ============================================================================
# SECTION 2: BASIC DATA EXPLORATION (Like a Detective!)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 2: EXPLORING THE DATA")
print("=" * 80)

# What columns do we have?
print("\n✓ Column names (headers):")
print(sales_df.columns.tolist())

# What data types do we have?
print("\n✓ Data types:")
print(sales_df.dtypes)

# Basic statistics
print("\n✓ Summary statistics for numbers:")
print(sales_df.describe())


# ============================================================================
# SECTION 3: SIMPLE FILTERING (SELECT WHERE = SQL concept)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 3: FILTERING DATA (This is like SQL's WHERE clause)")
print("=" * 80)

# SQL equivalent: SELECT * FROM sales WHERE amount > 100
high_value_sales = sales_df[sales_df['amount'] > 100]
print("\n✓ Sales with amount > $100:")
print(high_value_sales)

# SQL equivalent: SELECT * FROM sales WHERE product_name = 'Laptop'
laptop_sales = sales_df[sales_df['product_name'] == 'Laptop']
print("\n✓ All laptop sales:")
print(laptop_sales)


# ============================================================================
# SECTION 4: JOINING TABLES (SQL JOIN Concept)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 4: JOINING TABLES (SQL INNER JOIN)")
print("=" * 80)

# SQL equivalent: SELECT * FROM sales 
#                 INNER JOIN customers ON sales.customer_id = customers.customer_id

merged_data = pd.merge(sales_df, customers_df, on='customer_id', how='inner')
print("\n✓ Sales data WITH customer names and cities:")
print(merged_data)


# ============================================================================
# SECTION 5: GROUPING & AGGREGATION (SQL GROUP BY concept)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 5: GROUPING DATA (SQL GROUP BY)")
print("=" * 80)

# SQL equivalent: SELECT customer_id, COUNT(*), SUM(amount) 
#                 FROM sales GROUP BY customer_id

customer_stats = sales_df.groupby('customer_id').agg({
    'sale_id': 'count',  # How many purchases?
    'amount': 'sum'      # Total spent?
}).rename(columns={'sale_id': 'purchase_count', 'amount': 'total_spent'})

print("\n✓ How much did each customer spend?")
print(customer_stats)

# SQL equivalent: SELECT product_name, COUNT(*), AVG(amount) 
#                 FROM sales GROUP BY product_name

product_stats = sales_df.groupby('product_name')['amount'].agg([
    ('total_sales', 'sum'),
    ('avg_price', 'mean'),
    ('quantity_sold', 'count')
])

print("\n✓ Sales statistics by product:")
print(product_stats)


# ============================================================================
# SECTION 6: BASIC DATA CLEANING
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 6: DATA CLEANING (Fixing messy data)")
print("=" * 80)

# Let's create a "messy" dataset to practice cleaning
messy_data = {
    'product_id': [1, 2, 3, 4, 5, 6],
    'product_name': ['Laptop', 'mouse', 'KEYBOARD', 'Monitor', None, 'Headphones'],  # Mixed case, missing value
    'price': [1200, 25, 75, 300, 150, 80],
    'stock': [5, 100, None, 20, 15, 50]  # Missing value
}

messy_df = pd.DataFrame(messy_data)
print("\n✓ BEFORE CLEANING (messy data):")
print(messy_df)
print(f"Missing values:\n{messy_df.isnull().sum()}")

# CLEANING STEP 1: Fill missing values
cleaned_df = messy_df.copy()  # Make a copy so we don't change original
cleaned_df['product_name'] = cleaned_df['product_name'].fillna('Unknown')  # Replace None with 'Unknown'
cleaned_df['stock'] = cleaned_df['stock'].fillna(cleaned_df['stock'].mean())  # Replace with average

# CLEANING STEP 2: Standardize text (make everything lowercase then capitalize)
cleaned_df['product_name'] = cleaned_df['product_name'].str.lower().str.title()

print("\n✓ AFTER CLEANING:")
print(cleaned_df)
print(f"Missing values:\n{cleaned_df.isnull().sum()}")


# ============================================================================
# SECTION 7: SAVING DATA
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 7: SAVING DATA")
print("=" * 80)

# Save as CSV file (Excel-friendly format)
sales_df.to_csv('c:\\Users\\vaish\\OneDrive\\Desktop\\projects\\sales_data.csv', index=False)
print("\n✓ Saved: sales_data.csv")

customers_df.to_csv('c:\\Users\\vaish\\OneDrive\\Desktop\\projects\\customers_data.csv', index=False)
print("✓ Saved: customers_data.csv")

cleaned_df.to_csv('c:\\Users\\vaish\\OneDrive\\Desktop\\projects\\cleaned_products.csv', index=False)
print("✓ Saved: cleaned_products.csv")


print("\n" + "=" * 80)
print("✅ STEP 1 COMPLETE!")
print("=" * 80)
print("\nYou just learned:")
print("  ✓ How to create tables (DataFrames)")
print("  ✓ How to filter data (WHERE clause)")
print("  ✓ How to join tables (JOIN clause)")
print("  ✓ How to group and aggregate data (GROUP BY)")
print("  ✓ How to clean messy data")
print("  ✓ How to save data to files")
print("\nNext Step: We'll create SQL queries and advanced analysis!")
print("=" * 80)
