import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col

# Load datasets
wb_data = pd.read_csv("adm1pan_china_india_wb.csv")
idealpoint_data = pd.read_csv("IdealpointestimatesAll_Jun2024.csv")

# Convert session to year
idealpoint_data["year"] = idealpoint_data["session"] + 1945

# Merge datasets on country and year
merged_data = wb_data.merge(
    idealpoint_data,
    left_on=["gid_0", "year"],
    right_on=["iso3c", "year"],
    how="inner"
)

# Select relevant variables
wb_variables = [col for col in wb_data.columns if col.startswith("WB_")]
regression_data = merged_data[["USAgree", "gid_0", "year"] + wb_variables]

# Preprocess data
regression_data = regression_data.dropna().drop_duplicates(subset=['gid_0', 'year'])
regression_data['year'] = pd.to_numeric(regression_data['year'], errors='coerce')
regression_data['gid_0'] = regression_data['gid_0'].astype(str)
regression_data = regression_data.dropna(subset=['WB_comm', 'WB_disb', 'USAgree', 'gid_0', 'year'])

# Run regression models with fixed effects
model1 = smf.ols('WB_comm ~ USAgree + C(gid_0) + C(year)', data=regression_data).fit()
model2 = smf.ols('WB_disb ~ USAgree + C(gid_0) + C(year)', data=regression_data).fit()

# Display results
summary = summary_col(
    [model1, model2],
    stars=True,
    model_names=["WB_comm", "WB_disb"],
    info_dict={"N": lambda x: f"{int(x.nobs)}", "R2": lambda x: f"{x.rsquared:.2f}"}
)

print(summary)