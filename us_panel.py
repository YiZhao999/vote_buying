import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col

# Load data
df = pd.read_csv("us_regression_data_dropped.csv")

# Run regression with country/year fixed effects
model1 = smf.ols('WB_comm ~ USAgree + C(gid_0) + C(year)', data=df).fit()

# Format results for APSA-style table
summary = summary_col(
    [model1],
    stars=True,
    model_names=["WB_comm"],  # Single column for this model
    info_dict={
        "N": lambda x: f"{int(x.nobs)}",
        "R2": lambda x: f"{x.rsquared:.2f}"
    },
    float_format="%0.3f",  # 3 decimal places for coefficients/SEs
    regressor_order=["USAgree", "Intercept"]  # Highlight key variables
)

# Add significance and fixed effects notes
summary.add_text(
    "Standard errors in parentheses. "
    "* p<0.10, ** p<0.05, *** p<0.01.\n"
    "Country and year fixed effects included."
)

# Print formatted table
print(summary)