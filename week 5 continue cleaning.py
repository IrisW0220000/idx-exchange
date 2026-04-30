import pandas as pd

# LOAD DATA
sold = pd.read_csv("Filtered_Sold_Transactions.csv", low_memory=False)
listed = pd.read_csv("Filtered_Listed_Transactions.csv", low_memory=False)

print(f"Loaded sold:   {len(sold):,} rows, {sold.shape[1]} cols")
print(f"Loaded listed: {len(listed):,} rows, {listed.shape[1]} cols")

# Re-convert date fields since CSV loses datetime format when saved
date_fields_sold = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]
date_fields_listed = ["ListingContractDate", "ContractStatusChangeDate"]

for col in date_fields_sold:
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors="coerce")

for col in date_fields_listed:
    if col in listed.columns:
        listed[col] = pd.to_datetime(listed[col], errors="coerce")

# 2. DATE CONSISTENCY CHECKS (sold only)
print("\n--- Date Consistency Checks ---")

# listing_after_close: ListingContractDate should come BEFORE CloseDate
sold["listing_after_close_flag"] = (
    sold["ListingContractDate"] > sold["CloseDate"]
)
print(f"  listing_after_close_flag  : {sold['listing_after_close_flag'].sum():,} records")

# purchase_after_close: PurchaseContractDate should come BEFORE CloseDate
sold["purchase_after_close_flag"] = (
    sold["PurchaseContractDate"] > sold["CloseDate"]
)
print(f"  purchase_after_close_flag : {sold['purchase_after_close_flag'].sum():,} records")

# negative_timeline: ListingContractDate should come BEFORE PurchaseContractDate
sold["negative_timeline_flag"] = (
    sold["ListingContractDate"] > sold["PurchaseContractDate"]
)
print(f"  negative_timeline_flag    : {sold['negative_timeline_flag'].sum():,} records")

# 3. GEOGRAPHIC DATA CHECKS
print("\n--- Geographic Data Checks ---")

def flag_geo(df, label):
    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        print(f"  {label}: No Latitude/Longitude columns found — skipping")
        return

    # Null coordinates
    df["flag_null_lat"] = df["Latitude"].isnull()
    df["flag_null_lon"] = df["Longitude"].isnull()
    print(f"  {label}: null Latitude         → {df['flag_null_lat'].sum():,}")
    print(f"  {label}: null Longitude        → {df['flag_null_lon'].sum():,}")

    # Sentinel zero values
    df["flag_zero_lat"] = df["Latitude"] == 0
    df["flag_zero_lon"] = df["Longitude"] == 0
    print(f"  {label}: Latitude == 0         → {df['flag_zero_lat'].sum():,}")
    print(f"  {label}: Longitude == 0        → {df['flag_zero_lon'].sum():,}")

    
flag_geo(sold, "sold")
flag_geo(listed, "listed")

# 4. SUMMARY
print("\n--- Summary ---")

date_flags = ["listing_after_close_flag", "purchase_after_close_flag", "negative_timeline_flag"]
geo_flags = ["flag_null_lat", "flag_null_lon", "flag_zero_lat", "flag_zero_lon", "flag_positive_lon", "flag_implausible_coords"]

all_flags_sold = [c for c in date_flags + geo_flags if c in sold.columns]
all_flags_listed = [c for c in geo_flags if c in listed.columns]

print(f"  sold   rows with any flag : {sold[all_flags_sold].any(axis=1).sum():,} of {len(sold):,}")
print(f"  listed rows with any flag : {listed[all_flags_listed].any(axis=1).sum():,} of {len(listed):,}")

# 5. SAVE FINAL CLEAN DATASETS
print("\n--- Saving final datasets ---")

sold.to_csv("Final_Clean_Sold_Transactions.csv", index=False)
listed.to_csv("Final_Clean_Listed_Transactions.csv", index=False)

print(f"  ✓ Final_Clean_Sold_Transactions.csv   ({len(sold):,} rows, {sold.shape[1]} cols)")
print(f"  ✓ Final_Clean_Listed_Transactions.csv ({len(listed):,} rows, {listed.shape[1]} cols)")
print("\nWeek 5 complete!")