import pandas as pd
import glob
import os

# 1. Match all Sold CSV files in the 'raw' folder
file_pattern = os.path.join('raw', 'CRMLSSold*.csv')
file_list = glob.glob(file_pattern)

if not file_list:
    print("No Sold CSV files found in the 'raw' folder. Please check the path or filenames!")
else:
    print(f"Found {len(file_list)} Sold files. Starting merge process...")

    # 2. Read all CSV files and append to a list
    df_list = []
    for file in file_list:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
            print(f"Successfully read: {file}")
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    # 3. Concatenate all dataframes vertically
    combined_df = pd.concat(df_list, ignore_index=True)

    # 4. Export to a final CSV file in the main folder
    output_filename = 'Final_Clean_Sold_Transactions.csv'
    combined_df.to_csv(output_filename, index=False)
    
    print(f"\nMerge complete! Total records: {len(combined_df)}")
    print(f"File saved as: {output_filename}")