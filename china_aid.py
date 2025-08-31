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
china_variables = [col for col in wb_data.columns if col.startswith("CHN_")]
india_variables = [col for col in wb_data.columns if col.startswith("IND_")]
regression_data = merged_data[["ChinaAgree", "IndiaAgree", "gid_0", "year"] + china_variables + india_variables]
# Preprocess data
regression_data = regression_data.drop_duplicates(subset=['gid_0', 'year'])
regression_data.to_csv("china_india_regression_data.csv", index=False)
# regression_data['year'] = pd.to_numeric(regression_data['year'], errors='coerce')
# regression_data['gid_0'] = regression_data['gid_0'].astype(str)
# regression_data = regression_data.dropna(subset=['CHN_comm', 'ChinaAgree', 'gid_0', 'year'])
# Run regression models with fixed effects
# model1 = smf.ols('CHN_comm ~ ChinaAgree + C(gid_0) + C(year)', data=regression_data).fit()
#
# # Display results
# summary = summary_col(
#     [model1],
#     stars=True,
#     model_names=["WB_comm", "WB_disb"],
#     info_dict={"N": lambda x: f"{int(x.nobs)}", "R2": lambda x: f"{x.rsquared:.2f}"}
# )
#
# print(summary)