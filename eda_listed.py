import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("--- PART 1: WEEKS 2-3 DELIVERABLE (LISTED DATA) ---")

df = pd.read_csv('Final_Clean_Listed_Transactions.csv') 

# document different property types
print("\n1. Unique Property Types Found:")
print(df['PropertyType'].value_counts(dropna=False))

# q1
print("\n[Intern Question 1] Residential vs. other property type share:")
print((df['PropertyType'].value_counts(normalize=True) * 100).round(2).astype(str) + '%')

# filtering
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

print("\n4. Numeric Distribution Summary (LivingArea, DaysOnMarket):")
target_cols = ['LivingArea', 'DaysOnMarket'] 
existing_targets = [col for col in target_cols if col in df.columns]
print(df[existing_targets].describe())

# filtered
output_filename = 'Filtered_Listed_Transactions.csv'
df.to_csv(output_filename, index=False)
print(f"\n5. SUCCESS: Filtered dataset saved as {output_filename}")


print("\n\n--- PART 2: INTERN QUESTIONS ---")

# q2
print("\n[Intern Question 2] Median and average LIST prices (Homes not sold yet):")
if 'ListPrice' in df.columns:
    print(f"Average: ${df['ListPrice'].mean():,.2f}")
    print(f"Median:  ${df['ListPrice'].median():,.2f}")
else:
    print("ListPrice column not found.")

# q3
print("\n[Intern Question 3] Days on Market (DOM) Distribution:")
if 'DaysOnMarket' in df.columns:
    print(df['DaysOnMarket'].describe())
else:
    print("DaysOnMarket column not found.")

# q4&5
print("\n[Intern Question 4] Percentage of homes sold above vs. below list price:")
print("-> SKIPPED: Not applicable for listed properties (no ClosePrice yet).")

print("\n[Intern Question 5] Date consistency issues (Close Date before List Date):")
print("-> SKIPPED: Not applicable for listed properties (no CloseDate yet).")

# q6
print("\n[Intern Question 6] Counties with highest median LIST prices:")
try:
    if 'CountyOrParish' in df.columns:
        top_counties = df.groupby('CountyOrParish')['ListPrice'].median().sort_values(ascending=False)
    else:
        top_counties = df.groupby('County')['ListPrice'].median().sort_values(ascending=False)
    print(top_counties.head())
except KeyError:
    print("County or ListPrice column not found.")


print("\nGenerating charts... (Close the chart window to finish the script)")
if 'DaysOnMarket' in df.columns:
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(df['DaysOnMarket'].dropna(), bins=50, ax=ax[0])
    ax[0].set_title('Histogram of Days on Market (Listed)')
    sns.boxplot(x=df['DaysOnMarket'].dropna(), ax=ax[1])
    ax[1].set_title('Boxplot of Days on Market (Listed)')
    plt.show()