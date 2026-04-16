import pandas as pd
import ssl

# Fix for Mac SSL Certificate Error
ssl._create_default_https_context = ssl._create_unverified_context

print("Starting mortgage enrichment pipeline...")


sold = pd.read_csv('Final_Clean_Sold_Transactions.csv', low_memory=False)
listings = pd.read_csv('Final_Clean_Listed_Transactions.csv', low_memory=False)

# Fetch live mortgage rates from FRED API
print("Fetching live data from FRED...")
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"


mortgage = pd.read_csv(url)


mortgage = mortgage.iloc[:, :2]
mortgage.columns = ['date', 'rate_30yr_fixed']

mortgage['date'] = pd.to_datetime(mortgage['date'], errors='coerce')

mortgage = mortgage.dropna(subset=['date'])

mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index()

sold['CloseDate'] = pd.to_datetime(sold['CloseDate'], errors='coerce')
sold['year_month'] = sold['CloseDate'].dt.to_period('M')

listings['ListingContractDate'] = pd.to_datetime(listings['ListingContractDate'], errors='coerce')
listings['year_month'] = listings['ListingContractDate'].dt.to_period('M')

print("Merging datasets...")
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

sold_nulls = sold_with_rates['rate_30yr_fixed'].isnull().sum()
listed_nulls = listings_with_rates['rate_30yr_fixed'].isnull().sum()
print(f"Unmatched Sold Rows: {sold_nulls}")
print(f"Unmatched Listed Rows: {listed_nulls}")

sold_with_rates.to_csv('Enriched_Sold_Transactions.csv', index=False)
listings_with_rates.to_csv('Enriched_Listed_Transactions.csv', index=False)

print("SUCCESS: Live data fetch and merge complete!")