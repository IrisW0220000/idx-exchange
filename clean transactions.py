import pandas as pd

# 1.load data
sold = pd.read_csv("Enriched_Sold_Transactions.csv", low_memory=False)
listed = pd.read_csv("Enriched_Listed_Transactions.csv", low_memory=False)

print(f"Loaded sold:   {len(sold):,} rows, {sold.shape[1]} cols")
print(f"Loaded listed: {len(listed):,} rows, {listed.shape[1]} cols")

# 2. convert date fields to datetime (eg 2024-3-19 to datetime)
print("\n--- Converting date fields ---")

sold_date_cols = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]
listed_date_cols = ["ListingContractDate", "ContractStatusChangeDate"]

for col in sold_date_cols:
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors="coerce")
        print(f"  sold['{col}'] converted  (nulls: {sold[col].isnull().sum():,})")

for col in listed_date_cols:
    if col in listed.columns:
        listed[col] = pd.to_datetime(listed[col], errors="coerce")
        print(f"  listed['{col}'] converted  (nulls: {listed[col].isnull().sum():,})")

# 3. fix numeric variable types(to int)
print("\n--- Fixing numeric field types ---")

numeric_cols = [
    "ClosePrice", "ListPrice", "OriginalListPrice",
    "LivingArea", "LotSizeAcres",
    "BedroomsTotal", "BathroomsTotalInteger",
    "DaysOnMarket", "YearBuilt",
    "Latitude", "Longitude",
]

for col in numeric_cols:
    for df, name in [(sold, "sold"), (listed, "listed")]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

print("  Numeric fields converted for both datasets")

# 4. flag invalid numerical values(<0)
print("\n--- Flagging invalid numeric values ---")

# Sold flags
if "ClosePrice" in sold.columns:
    sold["flag_invalid_close_price"] = sold["ClosePrice"] <= 0
    print(f"  sold: ClosePrice <= 0      → {sold['flag_invalid_close_price'].sum():,} flagged")

if "LivingArea" in sold.columns:
    sold["flag_invalid_living_area"] = sold["LivingArea"] <= 0
    print(f"  sold: LivingArea <= 0      → {sold['flag_invalid_living_area'].sum():,} flagged")

if "DaysOnMarket" in sold.columns:
    sold["flag_negative_dom"] = sold["DaysOnMarket"] < 0
    print(f"  sold: DaysOnMarket < 0     → {sold['flag_negative_dom'].sum():,} flagged")

if "BedroomsTotal" in sold.columns:
    sold["flag_negative_beds"] = sold["BedroomsTotal"] < 0
    print(f"  sold: Bedrooms < 0         → {sold['flag_negative_beds'].sum():,} flagged")

if "BathroomsTotalInteger" in sold.columns:
    sold["flag_negative_baths"] = sold["BathroomsTotalInteger"] < 0
    print(f"  sold: Bathrooms < 0        → {sold['flag_negative_baths'].sum():,} flagged")

# Listed flags
if "ListPrice" in listed.columns:
    listed["flag_invalid_list_price"] = listed["ListPrice"] <= 0
    print(f"  listed: ListPrice <= 0     → {listed['flag_invalid_list_price'].sum():,} flagged")

if "LivingArea" in listed.columns:
    listed["flag_invalid_living_area"] = listed["LivingArea"] <= 0
    print(f"  listed: LivingArea <= 0    → {listed['flag_invalid_living_area'].sum():,} flagged")

# 5.drop columns that are 90% null
print("\n--- Dropping columns that are >90% null ---")

# Always keep these even if mostly null
core_fields = {
    "ClosePrice", "ListPrice", "OriginalListPrice", "LivingArea",
    "BedroomsTotal", "BathroomsTotalInteger", "DaysOnMarket",
    "CloseDate", "ListingContractDate", "PurchaseContractDate",
    "CountyOrParish", "PostalCode", "City", "MLSAreaMajor",
    "PropertyType", "PropertySubType", "YearBuilt",
    "ListOfficeName", "BuyerOfficeName",
    "Latitude", "Longitude", "rate_30yr_fixed",
}

for df, name in [(sold, "sold"), (listed, "listed")]:
    null_pct = df.isnull().mean()
    to_drop = [c for c in null_pct[null_pct > 0.90].index if c not in core_fields]
    df.drop(columns=to_drop, inplace=True)
    print(f"  {name}: dropped {len(to_drop)} columns → {df.shape[1]} columns remain")

# save cleaned data set
print("\n--- Saving cleaned datasets ---")

sold.to_csv("Filtered_Sold_Transactions.csv", index=False)
listed.to_csv("Filtered_Listed_Transactions.csv", index=False)

print(f"  ✓ Filtered_Sold_Transactions.csv   ({len(sold):,} rows, {sold.shape[1]} cols)")
print(f"  ✓ Filtered_Listed_Transactions.csv ({len(listed):,} rows, {listed.shape[1]} cols)")
print("\nWeek 4 cleaning complete!")