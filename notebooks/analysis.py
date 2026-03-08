# ============================================================
# E-Commerce Sales & Customer Analytics Project
# Author: Vivek Thapa
# Description:
# This script analyzes an e-commerce transaction dataset to
# understand sales trends, product performance, geographic
# revenue distribution, and customer behavior using RFM analysis.
# ============================================================


# ==============================
# 1. Import Required Libraries
# ==============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ==============================
# 2. Load Dataset
# ==============================

# Reading the online retail dataset
df = pd.read_excel("data/online_retail.xlsx")

print("Initial Dataset Preview:\n")
print(df.head())

print("\nDataset Information:\n")
print(df.info())


# ==============================
# 3. Data Cleaning
# ==============================

# Remove rows where CustomerID is missing
df = df.dropna(subset=['CustomerID'])

# Remove cancelled transactions (Invoice numbers starting with 'C')
df = df[~df['InvoiceNo'].astype(str).str.contains('C')]

print("\nDataset shape after cleaning:", df.shape)


# ==============================
# 4. Feature Engineering
# ==============================

# Create Revenue column (Quantity * UnitPrice)
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# Extract Month from InvoiceDate for time-based analysis
df['Month'] = df['InvoiceDate'].dt.to_period('M')


# ==============================
# 5. Monthly Revenue Analysis
# ==============================

# Calculate monthly revenue
monthly_sales = df.groupby('Month')['Revenue'].sum()

print("\nMonthly Revenue:\n")
print(monthly_sales.head())

# Plot monthly revenue trend
monthly_sales.plot()

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.show()


# ==============================
# 6. Top Products Analysis
# ==============================

# Identify top 10 products by revenue
top_products = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Products by Revenue:\n")
print(top_products)

# Visualize top products
top_products.plot(kind='bar')

plt.title("Top 10 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")

plt.show()


# ==============================
# 7. Country-wise Revenue Analysis
# ==============================

# Identify top countries contributing to revenue
country_sales = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10)

print("\nTop Countries by Revenue:\n")
print(country_sales)

# Visualize country sales
country_sales.plot(kind='bar')

plt.title("Top Countries by Revenue")
plt.xlabel("Country")
plt.ylabel("Revenue")

plt.show()


# ==============================
# 8. Customer Segmentation (RFM Analysis)
# ==============================

# Snapshot date (latest transaction date in dataset)
snapshot_date = df['InvoiceDate'].max()

# Calculate Recency, Frequency, Monetary metrics
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'Revenue': 'sum'
})

# Rename columns for clarity
rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("\nRFM Table Preview:\n")
print(rfm.head())


# ==============================
# 9. Identify Top Customers
# ==============================

# Top 10 customers by total spending
top_customers = rfm.sort_values(by='Monetary', ascending=False).head(10)

print("\nTop Customers by Spending:\n")
print(top_customers)

# Visualize top customers
top_customers['Monetary'].plot(kind='bar')

plt.title("Top 10 Customers by Spending")
plt.xlabel("Customer ID")
plt.ylabel("Total Spending")

plt.show()


# ==============================
# 10. Basic Customer Segmentation
# ==============================

# Initialize customer segment column
rfm['CustomerSegment'] = 'Regular'

# Segment customers based on RFM values
rfm.loc[rfm['Monetary'] > 5000, 'CustomerSegment'] = 'VIP'
rfm.loc[rfm['Frequency'] > 50, 'CustomerSegment'] = 'Loyal'
rfm.loc[rfm['Recency'] > 200, 'CustomerSegment'] = 'At Risk'

print("\nCustomer Segment Distribution:\n")
print(rfm['CustomerSegment'].value_counts())


# ==============================
# 11. Save Processed Data
# ==============================

# Save cleaned transactional dataset
df.to_csv("data/cleaned_retail_data.csv", index=False)

# Save RFM customer segmentation data
rfm.to_csv("data/customer_rfm.csv")

print("\nProcessed datasets saved successfully.")