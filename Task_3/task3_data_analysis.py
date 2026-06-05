"""
TASK 3: DATA ANALYSIS WITH PANDAS

"""

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================================
# SECTION 1: CREATE SAMPLE DATASET
# ============================================================================

def create_sample_dataset():
    """
    Creates a realistic sample dataset for e-commerce sales analysis.
    Includes some data quality issues to demonstrate cleaning techniques.
    """
    print("[Creating Sample Dataset]")
    print("-" * 70)
    
    # Create sample data with intentional quality issues
    data = {
        'Order_ID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                     111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
        'Date': pd.date_range('2026-01-01', periods=20, freq='D'),
        'Product_Category': ['Electronics', 'Clothing', 'Electronics', 'Books', 'Clothing',
                            'Electronics', None, 'Books', 'Clothing', 'Electronics',
                            'Books', 'Clothing', 'Electronics', 'Books', 'Clothing',
                            'Electronics', 'Books', 'Clothing', 'Electronics', 'Books'],
        'Quantity': [2, 1, 3, 1, 2, 4, 2, 1, 3, 2,
                    1, 2, 3, 1, 2, 4, 2, 1, 3, 2],
        'Unit_Price': [299.99, 45.50, 199.99, 12.99, 55.00,
                      149.99, 99.99, 15.99, 65.00, 249.99,
                      18.99, 42.00, 179.99, 9.99, 38.50,
                      299.99, 22.99, 48.00, 159.99, 14.99],
        'Discount': [0.1, 0.0, 0.15, 0.0, 0.05, 0.2, 0.0, 0.05, 0.0, 0.1,
                    0.0, 0.1, 0.15, 0.0, 0.05, 0.2, 0.0, 0.05, 0.1, 0.0],
        'Customer_ID': [1001, 1002, 1001, 1003, 1002,
                       1004, 1003, 1005, 1004, 1001,
                       1002, 1005, 1003, 1004, 1005,
                       1001, 1002, 1003, 1004, 1005],
        'Region': ['North', 'South', 'North', 'East', 'West',
                  'North', 'South', 'East', 'West', 'North',
                  'South', 'East', 'West', 'North', 'South',
                  'East', 'West', 'North', 'South', 'East']
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    csv_file = 'sales_data.csv'
    df.to_csv(csv_file, index=False)
    print(f"✓ Created sample dataset: {csv_file}")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    return csv_file


# ============================================================================
# SECTION 2: LOAD AND INSPECT DATA
# ============================================================================

def load_and_inspect(csv_file):
    """
    Loads CSV file and provides initial data inspection.
    
    This step is important for understanding:
    - Data shape and size
    - Column names and data types
    - First few rows
    - Data quality issues
    """
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(csv_file)
        print(f"\n✓ Successfully loaded: {csv_file}")
        
        # Display basic information
        print("\n[1. DATASET OVERVIEW]")
        print("-" * 70)
        print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"Total records: {len(df)}")
        
        # Display column info
        print("\n[2. COLUMN INFORMATION]")
        print("-" * 70)
        print(df.dtypes)
        
        # Display first rows
        print("\n[3. FIRST 5 ROWS]")
        print("-" * 70)
        print(df.head())
        
        # Display last rows
        print("\n[4. LAST 5 ROWS]")
        print("-" * 70)
        print(df.tail())
        
        # Display data quality metrics
        print("\n[5. DATA QUALITY CHECK]")
        print("-" * 70)
        print(df.info())
        print("\nMissing values per column:")
        missing = df.isnull().sum()
        print(missing)
        
        return df
    
    except FileNotFoundError:
        print(f"✗ Error: File not found - {csv_file}")
        return None
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return None


# ============================================================================
# SECTION 3: DATA CLEANING
# ============================================================================

def clean_data(df):
    """
    Cleans the dataset by handling missing values and data inconsistencies.
    
    Demonstrates:
    - Identifying missing values
    - Handling missing data (fill, drop, etc.)
    - Data type conversions
    - Removing duplicates
    """
    print("\n" + "=" * 70)
    print("DATA CLEANING PHASE")
    print("=" * 70)
    
    df_clean = df.copy()  # Work on a copy to preserve original
    
    # Step 1: Check for missing values
    print("\n[1. MISSING VALUES ANALYSIS]")
    print("-" * 70)
    missing = df_clean.isnull().sum()
    if missing.sum() > 0:
        print("Missing values found:")
        print(missing[missing > 0])
        
        # Fill missing Product_Category with 'Unknown'
        # (could also drop or use mode)
        df_clean['Product_Category'].fillna('Unknown', inplace=True)
        print("\n✓ Filled missing Product_Category with 'Unknown'")
    else:
        print("✓ No missing values found")
    
    # Step 2: Check for duplicates
    print("\n[2. DUPLICATE RECORDS ANALYSIS]")
    print("-" * 70)
    duplicates = df_clean.duplicated().sum()
    if duplicates > 0:
        print(f"Found {duplicates} duplicate records")
        df_clean = df_clean.drop_duplicates()
        print(f"✓ Removed {duplicates} duplicate records")
    else:
        print("✓ No duplicate records found")
    
    # Step 3: Data type conversion
    print("\n[3. DATA TYPE CONVERSION]")
    print("-" * 70)
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    print("✓ Converted 'Date' column to datetime format")
    
    # Step 4: Verify cleaned data
    print("\n[4. CLEANED DATA SUMMARY]")
    print("-" * 70)
    print(f"Records after cleaning: {len(df_clean)}")
    print(f"Columns: {list(df_clean.columns)}")
    
    return df_clean


# ============================================================================
# SECTION 4: FILTERING & SELECTION
# ============================================================================

def filtering_operations(df):
    """
    Demonstrates various filtering techniques to subset data.
    
    Important for:
    - Extracting specific records based on criteria
    - Analyzing subsets of data
    - Finding outliers or special cases
    """
    print("\n" + "=" * 70)
    print("FILTERING & SELECTION PHASE")
    print("=" * 70)
    
    # Filter 1: High-value orders
    print("\n[1. FILTER: HIGH-VALUE ORDERS]")
    print("-" * 70)
    df['Total_Amount'] = df['Quantity'] * df['Unit_Price'] * (1 - df['Discount'])
    
    high_value = df[df['Total_Amount'] > 500]
    print(f"Orders with total > $500: {len(high_value)}")
    if len(high_value) > 0:
        print(high_value[['Order_ID', 'Product_Category', 'Quantity', 'Unit_Price', 'Total_Amount']])
    
    # Filter 2: Specific category
    print("\n[2. FILTER: ELECTRONICS CATEGORY]")
    print("-" * 70)
    electronics = df[df['Product_Category'] == 'Electronics']
    print(f"Electronics orders: {len(electronics)}")
    print(f"Total value: ${electronics['Total_Amount'].sum():.2f}")
    
    # Filter 3: Region selection
    print("\n[3. FILTER: NORTH REGION]")
    print("-" * 70)
    north = df[df['Region'] == 'North']
    print(f"Orders in North region: {len(north)}")
    print(f"Average order value: ${north['Total_Amount'].mean():.2f}")
    
    # Filter 4: Multiple conditions
    print("\n[4. FILTER: ELECTRONICS IN NORTH REGION]")
    print("-" * 70)
    result = df[(df['Product_Category'] == 'Electronics') & (df['Region'] == 'North')]
    print(f"Matching orders: {len(result)}")
    if len(result) > 0:
        print(result[['Order_ID', 'Region', 'Quantity', 'Total_Amount']])
    
    return df


# ============================================================================
# SECTION 5: GROUPING & AGGREGATION
# ============================================================================

def grouping_operations(df):
    """
    Demonstrates grouping and aggregation to summarize data.
    
    Important for:
    - Creating pivot tables
    - Calculating summaries by category/region/etc
    - Finding top performers
    """
    print("\n" + "=" * 70)
    print("GROUPING & AGGREGATION PHASE")
    print("=" * 70)
    
    # Aggregation 1: By Category
    print("\n[1. SUMMARY BY PRODUCT CATEGORY]")
    print("-" * 70)
    category_summary = df.groupby('Product_Category').agg({
        'Order_ID': 'count',           # Number of orders
        'Quantity': 'sum',              # Total quantity
        'Total_Amount': ['sum', 'mean', 'min', 'max']  # Revenue stats
    })
    category_summary.columns = ['Orders', 'Total_Qty', 'Total_Revenue', 
                                'Avg_Order_Value', 'Min_Order', 'Max_Order']
    category_summary['Total_Revenue'] = category_summary['Total_Revenue'].round(2)
    category_summary['Avg_Order_Value'] = category_summary['Avg_Order_Value'].round(2)
    
    print(category_summary)
    print(f"\n✓ Highest revenue category: {category_summary['Total_Revenue'].idxmax()} "
          f"(${category_summary['Total_Revenue'].max():.2f})")
    
    # Aggregation 2: By Region
    print("\n[2. SUMMARY BY REGION]")
    print("-" * 70)
    region_summary = df.groupby('Region').agg({
        'Order_ID': 'count',
        'Quantity': 'sum',
        'Total_Amount': ['sum', 'mean']
    })
    region_summary.columns = ['Orders', 'Total_Qty', 'Total_Revenue', 'Avg_Order_Value']
    region_summary['Total_Revenue'] = region_summary['Total_Revenue'].round(2)
    region_summary['Avg_Order_Value'] = region_summary['Avg_Order_Value'].round(2)
    
    print(region_summary)
    
    # Aggregation 3: By Customer
    print("\n[3. TOP 5 CUSTOMERS BY REVENUE]")
    print("-" * 70)
    customer_summary = df.groupby('Customer_ID').agg({
        'Order_ID': 'count',
        'Total_Amount': ['sum', 'mean']
    }).round(2)
    customer_summary.columns = ['Orders', 'Total_Spent', 'Avg_Order']
    customer_summary = customer_summary.sort_values('Total_Spent', ascending=False)
    
    print(customer_summary.head())
    
    return category_summary, region_summary, customer_summary


# ============================================================================
# SECTION 6: STATISTICAL INSIGHTS
# ============================================================================

def generate_insights(df):
    """
    Generates statistical insights and key findings from the data.
    
    Demonstrates:
    - Descriptive statistics
    - Trend analysis
    - Performance metrics
    """
    print("\n" + "=" * 70)
    print("STATISTICAL INSIGHTS")
    print("=" * 70)
    
    # Calculate key metrics
    total_revenue = df['Total_Amount'].sum()
    average_order = df['Total_Amount'].mean()
    median_order = df['Total_Amount'].median()
    std_order = df['Total_Amount'].std()
    min_order = df['Total_Amount'].min()
    max_order = df['Total_Amount'].max()
    
    print("\n[1. REVENUE STATISTICS]")
    print("-" * 70)
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Average Order Value: ${average_order:.2f}")
    print(f"Median Order Value: ${median_order:.2f}")
    print(f"Standard Deviation: ${std_order:.2f}")
    print(f"Min Order: ${min_order:.2f}")
    print(f"Max Order: ${max_order:.2f}")
    print(f"Order Range: ${max_order - min_order:.2f}")
    
    # Quantity analysis
    print("\n[2. QUANTITY ANALYSIS]")
    print("-" * 70)
    print(f"Total Units Sold: {df['Quantity'].sum()}")
    print(f"Average Units per Order: {df['Quantity'].mean():.2f}")
    print(f"Most Common Order Size: {df['Quantity'].mode().values[0]} units")
    
    # Discount analysis
    print("\n[3. DISCOUNT ANALYSIS]")
    print("-" * 70)
    discounted_orders = df[df['Discount'] > 0]
    print(f"Orders with Discount: {len(discounted_orders)} ({len(discounted_orders)/len(df)*100:.1f}%)")
    print(f"Average Discount: {df['Discount'].mean()*100:.1f}%")
    print(f"Total Discount Amount: ${(df['Unit_Price'] * df['Quantity'] * df['Discount']).sum():.2f}")
    
    # Category performance
    print("\n[4. CATEGORY PERFORMANCE]")
    print("-" * 70)
    top_category = df.groupby('Product_Category')['Total_Amount'].sum().idxmax()
    top_revenue = df.groupby('Product_Category')['Total_Amount'].sum().max()
    print(f"Top Performing Category: {top_category} (${top_revenue:.2f})")
    
    # Regional insights
    print("\n[5. REGIONAL INSIGHTS]")
    print("-" * 70)
    best_region = df.groupby('Region')['Total_Amount'].sum().idxmax()
    best_revenue = df.groupby('Region')['Total_Amount'].sum().max()
    print(f"Best Performing Region: {best_region} (${best_revenue:.2f})")
    
    # Time-based insights
    print("\n[6. TIME-BASED ANALYSIS]")
    print("-" * 70)
    daily_sales = df.groupby(df['Date'].dt.date)['Total_Amount'].sum()
    print(f"Average Daily Revenue: ${daily_sales.mean():.2f}")
    print(f"Peak Day Revenue: ${daily_sales.max():.2f}")
    print(f"Lowest Day Revenue: ${daily_sales.min():.2f}")
    
    return {
        'total_revenue': total_revenue,
        'average_order': average_order,
        'total_orders': len(df),
        'total_units': df['Quantity'].sum()
    }


# ============================================================================
# SECTION 7: MAIN DEMONSTRATION
# ============================================================================

def main():
    """
    Main function orchestrating the complete data analysis workflow.
    """
    print("\n" + "=" * 70)
    print("TASK 3: DATA ANALYSIS WITH PANDAS")
    print("=" * 70)
    
    # Step 1: Create sample data
    csv_file = create_sample_dataset()
    
    # Step 2: Load and inspect
    df = load_and_inspect(csv_file)
    if df is None:
        return
    
    # Step 3: Clean data
    df = clean_data(df)
    
    # Step 4: Filtering operations
    df = filtering_operations(df)
    
    # Step 5: Grouping and aggregation
    category_summary, region_summary, customer_summary = grouping_operations(df)
    
    # Step 6: Generate insights
    insights = generate_insights(df)
    
    # Step 7: Save analysis results
    print("\n" + "=" * 70)
    print("SAVING ANALYSIS RESULTS")
    print("=" * 70)
    
    # Save summaries
    category_summary.to_csv('analysis_by_category.csv')
    region_summary.to_csv('analysis_by_region.csv')
    customer_summary.to_csv('analysis_by_customer.csv')
    
    # Save processed data
    df.to_csv('cleaned_sales_data.csv', index=False)
    
    print("\n✓ Saved analysis results:")
    print("  • analysis_by_category.csv")
    print("  • analysis_by_region.csv")
    print("  • analysis_by_customer.csv")
    print("  • cleaned_sales_data.csv")
    
    # Summary
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"\nTotal Orders Analyzed: {insights['total_orders']}")
    print(f"Total Revenue: ${insights['total_revenue']:.2f}")
    print(f"Average Order Value: ${insights['average_order']:.2f}")
    print(f"Total Units Sold: {insights['total_units']}")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()