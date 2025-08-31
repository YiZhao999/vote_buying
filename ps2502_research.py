import pandas as pd

# Load datasets
wb = pd.read_csv("adm1pan_china_india_wb.csv")
idealpoint_data = pd.read_csv("IdealpointestimatesAll_Jun2024.csv")

# Step 1: Drop all columns except the specified ones
df_filtered = wb[['gid_0', 'gid_1', 'name_0', 'year', 'CHN_comm', 'WB_comm', 'IND_comm']]

# Step 2: Aggregate province-level (gid_1) data to country-level (gid_0), by year
df_aggregated = df_filtered.groupby(['gid_0', 'name_0', 'year'], as_index=False).agg({
    'CHN_comm': 'sum',
    'WB_comm': 'sum',
    'IND_comm': 'sum'
})

# Rename the columns to indicate they are aggregated
df_aggregated.rename(columns={
    'CHN_comm': 'CHN_comm_added',
    'WB_comm': 'WB_comm_added',
    'IND_comm': 'IND_comm_added'
}, inplace=True)

# Convert session to year
idealpoint_data["year"] = idealpoint_data["session"] + 1945

ip_filtered = idealpoint_data[['iso3c', 'year', 'ChinaAgree', 'IndiaAgree', 'USAgree']]

merged_data_new = df_aggregated.merge(
    ip_filtered,
    left_on=["gid_0", "year"],
    right_on=["iso3c", "year"],
    how="inner"
)

merged_data_new.to_csv("ps2502_regression_data.csv", index=False)

