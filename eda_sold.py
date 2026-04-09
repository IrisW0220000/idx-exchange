import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("--- PART 1: WEEKS 2-3 DELIVERABLE (SOLD DATA) ---")

df = pd.read_csv('Final_Clean_Sold_Transactions.csv') 

# document unique type
print("\n1. Unique Property Types Found:")
print(df['PropertyType'].value_counts(dropna=False))

# q1
print("\n[Intern Question 1] Residential vs. other property type share:")
print((df['PropertyType'].value_counts(normalize=True) * 100).round(2).astype(str) + '%')

# filter
print("\n2. Filtering Logic Applied: Keeping ONLY 'Residential'...")
df = df[df['PropertyType'] == 'Residential'].reset_index(drop=True)

# >90% flag
print("\n3. Null-Count Summary Table (Top 15 highest nulls):")
null_summary = pd.DataFrame({
    'Null_Count': df.isnull().sum(),
    'Null_Percent': (df.isnull().sum() / len(df)) * 100
}).sort_values(by='Null_Percent', ascending=False)
print(null_summary.head(15))

cols_to_drop = null_summary[null_summary['Null_Percent'] > 90.0].index.tolist()
print(f"\nFLAGGED: Dropping {len(cols_to_drop)} columns with >90% missing values.")
df = df.drop(columns=cols_to_drop)

# numeric distribution summary
print("\n4. Numeric Distribution Summary (ClosePrice, LivingArea, DaysOnMarket):")
target_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
existing_targets = [col for col in target_cols if col in df.columns]
print(df[existing_targets].describe()) 

# save new csv
output_filename = 'Filtered_Sold_Transactions.csv'
df.to_csv(output_filename, index=False)
print(f"\n5. SUCCESS: Filtered dataset saved as {output_filename}")


print("\n\n--- PART 2: INTERN QUESTIONS ---")

# q2
print("\n[Intern Question 2] Median and average close prices:")
print(f"Average: ${df['ClosePrice'].mean():,.2f}")
print(f"Median:  ${df['ClosePrice'].median():,.2f}")

# q3
print("\n[Intern Question 3] Days on Market (DOM) Distribution:")
print(df['DaysOnMarket'].describe())

# q4
print("\n[Intern Question 4] Percentage of homes sold above vs. below list price:")
price_df = df.dropna(subset=['ClosePrice', 'ListPrice'])
if not price_df.empty:
    above = (price_df['ClosePrice'] > price_df['ListPrice']).sum()
    below = (price_df['ClosePrice'] < price_df['ListPrice']).sum()
    at = (price_df['ClosePrice'] == price_df['ListPrice']).sum()
    total = len(price_df)
    print(f"Above List: {(above/total)*100:.1f}% | Below List: {(below/total)*100:.1f}% | Exactly At List: {(at/total)*100:.1f}%")

# q5
print("\n[Intern Question 5] Date consistency issues (Close Date before List Date):")
try:
    list_dates = pd.to_datetime(df['ListDate'])
    close_dates = pd.to_datetime(df['CloseDate'])
    bad_dates = df[close_dates < list_dates]
    print(f"Found {len(bad_dates)} records where Close Date is BEFORE List Date.")
except KeyError:
    print("Columns 'ListDate' or 'CloseDate' not found. You may need to check your CSV for the exact column names.")

# q6
print("\n[Intern Question 6] Counties with highest median prices:")
try:
    if 'CountyOrParish' in df.columns:
        top_counties = df.groupby('CountyOrParish')['ClosePrice'].median().sort_values(ascending=False)
    else:
        top_counties = df.groupby('County')['ClosePrice'].median().sort_values(ascending=False)
    print(top_counties.head())
except KeyError:
    print("County column not found.")


print("\nGenerating charts... (Close the chart window to finish the script)")
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(df['DaysOnMarket'].dropna(), bins=50, ax=ax[0])
ax[0].set_title('Histogram of Days on Market')
sns.boxplot(x=df['DaysOnMarket'].dropna(), ax=ax[1])
ax[1].set_title('Boxplot of Days on Market')
plt.show()