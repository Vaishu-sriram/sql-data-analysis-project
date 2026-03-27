/*
================================================================================
COMPREHENSIVE SQL QUERIES GUIDE - BEGINNER TO INTERMEDIATE
================================================================================
This file contains SQL examples that match the DataFrame operations from project-1.py
Each query demonstrates a different SQL concept with real-world examples.

Database Tables:
1. CUSTOMERS (customer_id, customer_name, city, join_date)
2. SALES (sale_id, customer_id, product_name, amount, sale_date)

================================================================================
*/

-- ============================================================================
-- SECTION 1: BASIC SELECT QUERIES
-- ============================================================================

/* Query 1.1: SELECT ALL DATA FROM CUSTOMERS TABLE
   Shows: How to retrieve all records from a table
*/
SELECT * 
FROM CUSTOMERS;

/* Query 1.2: SELECT SPECIFIC COLUMNS ONLY
   Shows: How to select only the columns you need
*/
SELECT customer_id, customer_name, city 
FROM CUSTOMERS;

/* Query 1.3: SELECT WITH ALIASES (rename columns in output)
   Shows: How to give columns custom names for better readability
*/
SELECT 
    customer_id AS ID,
    customer_name AS Name,
    city AS Location,
    join_date AS 'Joined On'
FROM CUSTOMERS;

/* Query 1.4: SELECT ALL SALES DATA
   Shows: Basic retrieval from sales table
*/
SELECT * 
FROM SALES;

/* Query 1.5: LIMIT RESULTS (Get top N records)
   Shows: How to restrict the number of rows returned
*/
SELECT TOP 5 * 
FROM SALES;  -- SQL Server syntax
-- OR use LIMIT in MySQL/PostgreSQL: LIMIT 5


-- ============================================================================
-- SECTION 2: FILTERING DATA (WHERE CLAUSE)
-- ============================================================================

/* Query 2.1: FILTER BY AMOUNT (WHERE clause)
   EQUIVALENT TO: sales_df[sales_df['amount'] > 100]
   Shows: How to filter rows based on numeric conditions
*/
SELECT * 
FROM SALES
WHERE amount > 100
ORDER BY amount DESC;

/* Query 2.2: FILTER BY PRODUCT NAME
   EQUIVALENT TO: sales_df[sales_df['product_name'] == 'Laptop']
   Shows: How to filter using text (string) values
*/
SELECT * 
FROM SALES
WHERE product_name = 'Laptop';

/* Query 2.3: MULTIPLE CONDITIONS (AND/OR)
   Shows: How to combine multiple filtering conditions
*/
SELECT * 
FROM SALES
WHERE amount > 100 AND product_name = 'Laptop';

/* Query 2.4: CONDITION WITH OR
   Shows: Rows that match EITHER condition
*/
SELECT * 
FROM SALES
WHERE product_name = 'Laptop' 
   OR product_name = 'Monitor';

/* Query 2.5: FILTER BY DATE RANGE
   Shows: How to filter using dates
*/
SELECT * 
FROM SALES
WHERE sale_date >= '2024-02-01' 
  AND sale_date <= '2024-03-31';

/* Query 2.6: USING IN to match multiple values
   Shows: Shorter way to write multiple OR conditions
*/
SELECT * 
FROM SALES
WHERE product_name IN ('Laptop', 'Monitor', 'Keyboard');

/* Query 2.7: FILTER CUSTOMERS BY CITY
   Shows: Filter from different table
*/
SELECT * 
FROM CUSTOMERS
WHERE city = 'New York';

/* Query 2.8: FILTER WITH NOT EQUAL
   Shows: Get records that DON'T match a condition
*/
SELECT * 
FROM SALES
WHERE product_name != 'Mouse' 
  AND product_name != 'USB Cable';


-- ============================================================================
-- SECTION 3: JOINING TABLES (JOIN clause)
-- ============================================================================

/* Query 3.1: INNER JOIN - Match records from both tables
   EQUIVALENT TO: pd.merge(sales_df, customers_df, on='customer_id', how='inner')
   Shows: Combine sales with customer information
*/
SELECT 
    s.sale_id,
    s.customer_id,
    c.customer_name,
    s.product_name,
    s.amount,
    c.city,
    c.join_date
FROM SALES s
INNER JOIN CUSTOMERS c 
    ON s.customer_id = c.customer_id
ORDER BY s.sale_id;

/* Query 3.2: INNER JOIN with WHERE clause
   Shows: Filter joined data further
*/
SELECT 
    s.sale_id,
    c.customer_name,
    s.product_name,
    s.amount
FROM SALES s
INNER JOIN CUSTOMERS c 
    ON s.customer_id = c.customer_id
WHERE s.amount > 100;

/* Query 3.3: LEFT JOIN - Keep all sales, add customer info if available
   Shows: What if a sale has no matching customer?
*/
SELECT 
    s.sale_id,
    s.customer_id,
    c.customer_name,
    s.product_name,
    s.amount
FROM SALES s
LEFT JOIN CUSTOMERS c 
    ON s.customer_id = c.customer_id;

/* Query 3.4: JOIN - Get all customers with their sales total
   Shows: Combining data from both tables with filtering
*/
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(s.sale_id) AS total_purchases,
    SUM(s.amount) AS total_amount_spent
FROM CUSTOMERS c
LEFT JOIN SALES s 
    ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_name, c.city;

/* Query 3.5: FINDING UNMATCHED RECORDS (Customers with no sales)
   Shows: Using LEFT JOIN to find records without matches
*/
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(s.sale_id) AS number_of_sales
FROM CUSTOMERS c
LEFT JOIN SALES s 
    ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(s.sale_id) = 0;


-- ============================================================================
-- SECTION 4: GROUPING DATA (GROUP BY clause)
-- ============================================================================

/* Query 4.1: GROUP BY - Total sales per customer
   EQUIVALENT TO: sales_df.groupby('customer_id').agg({'amount': 'sum'})
   Shows: Aggregate data by a specific column
*/
SELECT 
    customer_id,
    COUNT(*) AS purchase_count,
    SUM(amount) AS total_spent,
    AVG(amount) AS average_purchase,
    MIN(amount) AS cheapest_purchase,
    MAX(amount) AS most_expensive_purchase
FROM SALES
GROUP BY customer_id
ORDER BY total_spent DESC;

/* Query 4.2: GROUP BY with customer name (using JOIN)
   Shows: More readable GROUP BY by joining with customer names
*/
SELECT 
    s.customer_id,
    c.customer_name,
    COUNT(s.sale_id) AS total_purchases,
    SUM(s.amount) AS total_spent,
    AVG(s.amount) AS avg_purchase_value
FROM SALES s
INNER JOIN CUSTOMERS c 
    ON s.customer_id = c.customer_id
GROUP BY s.customer_id, c.customer_name
ORDER BY total_spent DESC;

/* Query 4.3: GROUP BY - Sales statistics by product
   EQUIVALENT TO: sales_df.groupby('product_name').agg(...)
   Shows: Aggregate sales information by product
*/
SELECT 
    product_name,
    COUNT(*) AS quantity_sold,
    SUM(amount) AS total_sales,
    AVG(amount) AS avg_price,
    MIN(amount) AS min_price,
    MAX(amount) AS max_price
FROM SALES
GROUP BY product_name
ORDER BY total_sales DESC;

/* Query 4.4: GROUP BY with date (Monthly sales)
   Shows: Aggregate data by time periods
*/
SELECT 
    YEAR(sale_date) AS year,
    MONTH(sale_date) AS month,
    COUNT(*) AS transactions,
    SUM(amount) AS monthly_revenue
FROM SALES
GROUP BY YEAR(sale_date), MONTH(sale_date)
ORDER BY year, month;

/* Query 4.5: GROUP BY - Sales by City
   Shows: Aggregate sales combined with customer location
*/
SELECT 
    c.city,
    COUNT(s.sale_id) AS total_transactions,
    SUM(s.amount) AS total_city_sales,
    AVG(s.amount) AS avg_transaction
FROM SALES s
INNER JOIN CUSTOMERS c 
    ON s.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_city_sales DESC;


-- ============================================================================
-- SECTION 5: HAVING CLAUSE (Filter after GROUP BY)
-- ============================================================================

/* Query 5.1: HAVING - Find customers who spent more than $500
   Shows: Filter grouped results (WHERE works on rows, HAVING works on groups)
*/
SELECT 
    customer_id,
    COUNT(*) AS purchase_count,
    SUM(amount) AS total_spent
FROM SALES
GROUP BY customer_id
HAVING SUM(amount) > 500
ORDER BY total_spent DESC;

/* Query 5.2: HAVING - Find products sold more than once
   Shows: Filter groups by count
*/
SELECT 
    product_name,
    COUNT(*) AS quantity_sold,
    SUM(amount) AS total_sales
FROM SALES
GROUP BY product_name
HAVING COUNT(*) > 1
ORDER BY quantity_sold DESC;

/* Query 5.3: HAVING with multiple conditions
   Shows: Complex filtering on grouped data
*/
SELECT 
    product_name,
    COUNT(*) AS quantity_sold,
    AVG(amount) AS avg_price
FROM SALES
GROUP BY product_name
HAVING COUNT(*) >= 2 
   AND AVG(amount) > 100;


-- ============================================================================
-- SECTION 6: SUBQUERIES (Queries within Queries)
-- ============================================================================

/* Query 6.1: Simple subquery - Get sales above average
   Shows: Use result of one query as filter for another
*/
SELECT * 
FROM SALES
WHERE amount > (
    SELECT AVG(amount) 
    FROM SALES
);

/* Query 6.2: Subquery in FROM clause - Create derived table
   Shows: Use subquery result as a temporary table
*/
SELECT 
    customer_id,
    total_spent,
    CASE 
        WHEN total_spent > 1000 THEN 'High Value Customer'
        WHEN total_spent > 500 THEN 'Medium Value Customer'
        ELSE 'Low Value Customer'
    END AS customer_tier
FROM (
    SELECT 
        customer_id,
        SUM(amount) AS total_spent
    FROM SALES
    GROUP BY customer_id
) AS customer_totals;

/* Query 6.3: Subquery with IN operator
   Shows: Find customers who bought laptops
*/
SELECT DISTINCT customer_id
FROM SALES
WHERE customer_id IN (
    SELECT customer_id 
    FROM SALES 
    WHERE product_name = 'Laptop'
);

/* Query 6.4: Find products that sold above average
   Shows: Compare individual records to aggregate value
*/
SELECT 
    s.product_name,
    COUNT(s.sale_id) AS times_sold,
    (SELECT AVG(quantity) FROM (
        SELECT COUNT(*) AS quantity 
        FROM SALES 
        GROUP BY product_name
    ) AS product_counts) AS avg_product_sales
FROM SALES s
GROUP BY s.product_name;

/* Query 6.5: Correlated subquery - Get customer info with sale count
   Shows: Advanced subquery that references outer table
*/
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    (SELECT COUNT(*) FROM SALES WHERE customer_id = c.customer_id) AS total_purchases,
    (SELECT SUM(amount) FROM SALES WHERE customer_id = c.customer_id) AS total_spent
FROM CUSTOMERS c;


-- ============================================================================
-- SECTION 7: SORTING (ORDER BY)
-- ============================================================================

/* Query 7.1: Sort by single column ascending
   Shows: Default sort order (A-Z or smallest to largest)
*/
SELECT * 
FROM SALES
ORDER BY amount ASC;

/* Query 7.2: Sort by single column descending
   Shows: Reverse sort order (Z-A or largest to smallest)
*/
SELECT * 
FROM SALES
ORDER BY amount DESC;

/* Query 7.3: Sort by multiple columns
   Shows: Primary sort then secondary sort
*/
SELECT 
    customer_id,
    product_name,
    amount,
    sale_date
FROM SALES
ORDER BY customer_id ASC, amount DESC;

/* Query 7.4: Sort with NULL values last
   Shows: Control where NULL values appear
*/
SELECT * 
FROM SALES
ORDER BY product_name IS NULL, product_name ASC;


-- ============================================================================
-- SECTION 8: ADVANCED QUERIES
-- ============================================================================

/* Query 8.1: UNION - Combine results from two queries
   Shows: Stack results from different queries
*/
SELECT customer_name AS name, city, 'Customer' AS type
FROM CUSTOMERS
UNION
SELECT DISTINCT product_name, NULL, 'Product'
FROM SALES;

/* Query 8.2: TOP sellers - Find best performing products
   Shows: Ranking and limiting results
*/
SELECT TOP 3 
    product_name,
    COUNT(*) AS times_sold,
    SUM(amount) AS total_revenue
FROM SALES
GROUP BY product_name
ORDER BY total_revenue DESC;

/* Query 8.3: Window function - Rank customers by total spend
   Shows: Advanced ranking (SQL Server specific)
*/
SELECT 
    customer_id,
    SUM(amount) AS total_spent,
    RANK() OVER (ORDER BY SUM(amount) DESC) AS customer_rank
FROM SALES
GROUP BY customer_id;

/* Query 8.4: Calculate running total
   Shows: Cumulative sum (SQL Server specific)
*/
SELECT 
    sale_id,
    customer_id,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY sale_id
    ) AS running_total
FROM SALES;

/* Query 8.5: Customer lifetime value with metrics
   Shows: Complex aggregation with multiple metrics
*/
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    c.join_date,
    COUNT(DISTINCT s.sale_id) AS total_orders,
    COUNT(DISTINCT s.product_name) AS unique_products_bought,
    SUM(s.amount) AS total_value,
    AVG(s.amount) AS avg_order_value,
    MIN(s.sale_date) AS first_purchase,
    MAX(s.sale_date) AS last_purchase
FROM CUSTOMERS c
LEFT JOIN SALES s 
    ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_name, c.city, c.join_date
ORDER BY total_value DESC;

/* Query 8.6: Compare each sale to customer average
   Shows: Individual vs. aggregate comparison
*/
SELECT 
    s.sale_id,
    s.customer_id,
    s.product_name,
    s.amount,
    (SELECT AVG(amount) FROM SALES WHERE customer_id = s.customer_id) AS customer_avg,
    s.amount - (SELECT AVG(amount) FROM SALES WHERE customer_id = s.customer_id) AS diff_from_avg
FROM SALES s
ORDER BY s.customer_id, diff_from_avg DESC;

/* Query 8.7: Year-over-year analysis (if multi-year data)
   Shows: Compare periods over time
*/
SELECT 
    YEAR(sale_date) AS year,
    MONTH(sale_date) AS month,
    COUNT(*) AS transactions,
    SUM(amount) AS monthly_revenue,
    SUM(amount) OVER (
        PARTITION BY YEAR(sale_date) 
        ORDER BY MONTH(sale_date)
    ) AS ytd_total
FROM SALES
ORDER BY year, month;


-- ============================================================================
-- SECTION 9: DATA CLEANING & VALIDATION QUERIES
-- ============================================================================

/* Query 9.1: Find missing or NULL values
   Shows: Data quality check
*/
SELECT 
    'customer_id' AS column_name,
    COUNT(*) - COUNT(customer_id) AS null_count
FROM SALES
UNION ALL
SELECT 
    'product_name',
    COUNT(*) - COUNT(product_name)
FROM SALES
UNION ALL
SELECT 
    'amount',
    COUNT(*) - COUNT(amount)
FROM SALES;

/* Query 9.2: Find duplicate records
   Shows: Identify redundant data
*/
SELECT 
    customer_id,
    product_name,
    amount,
    sale_date,
    COUNT(*) AS occurrence_count
FROM SALES
GROUP BY customer_id, product_name, amount, sale_date
HAVING COUNT(*) > 1;

/* Query 9.3: Find inconsistent data types
   Shows: Validate data integrity
*/
SELECT * 
FROM SALES
WHERE 
    TRY_CAST(amount AS INT) IS NULL
    OR LEN(product_name) = 0
    OR sale_date IS NULL;

/* Query 9.4: Standardize data
   Shows: Clean and normalize values
*/
SELECT 
    customer_id,
    UPPER(TRIM(product_name)) AS product_name_clean,
    amount,
    CONVERT(DATE, sale_date) AS sale_date_clean
FROM SALES;


-- ============================================================================
-- SUMMARY & KEY CONCEPTS
-- ============================================================================

/*
KEY SQL CONCEPTS COVERED:

1. SELECT - Retrieve specific columns
2. WHERE - Filter rows based on conditions
3. JOIN - Combine data from multiple tables
4. GROUP BY - Aggregate data by categories
5. HAVING - Filter grouped results
6. ORDER BY - Sort results
7. LIMIT/TOP - Restrict number of rows
8. SUBQUERIES - Nested queries for complex logic
9. AGGREGATE FUNCTIONS:
   - COUNT(*) - Count rows
   - SUM() - Total values
   - AVG() - Average value
   - MIN() - Minimum value
   - MAX() - Maximum value

PRACTICE TIPS:
- Start with simple SELECT queries
- Add WHERE to filter specific data
- Use JOIN when combining tables
- Use GROUP BY to summarize data
- Test each query individually
- Comment your queries for clarity

DATABASE COMPARISON:
SQL Server: Uses TOP, CONVERT for dates
MySQL: Uses LIMIT, DATE_FORMAT for dates
PostgreSQL: Uses LIMIT, CAST for type conversion
*/

-- ============================================================================
-- END OF SQL QUERIES FILE
-- ============================================================================
