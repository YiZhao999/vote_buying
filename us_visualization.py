import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv("us_regression_data_dropped.csv")  # Replace with your actual file path

# Group by country (ISO code) and aggregate
agg_data = df.groupby("gid_0").agg({
    "WB_comm": "sum",
    "WB_disb": "sum",
    "USAgree": "mean"
}).reset_index()

# Load world shapefile from geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge aggregated data with world map
world = world.merge(agg_data, how="left", left_on="iso_a3", right_on="gid_0")


# Function to plot a single map
def plot_world_map(data, column, title, cmap, filename=None, use_variance=True):
    # Set color scale range based on mean ± std if use_variance is True
    if use_variance:
        mean_val = data[column].mean()
        std_val = data[column].std()
        vmin = mean_val - std_val
        vmax = mean_val + std_val
    else:
        vmin = data[column].min()
        vmax = data[column].max()

    fig, ax = plt.subplots(figsize=(12, 8))
    data.plot(column=column, cmap=cmap, linewidth=0.8, edgecolor='0.8',
              legend=True, ax=ax, vmin=vmin, vmax=vmax)
    ax.set_title(title, fontsize=15)
    ax.axis('off')
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300)
    plt.show()


# Plot World Bank Commitments Map
plot_world_map(world, 'WB_comm', 'Total WB Commitments by Country', 'Blues', 'WB_commitments_map.png')


# Plot US Agreement Map
plot_world_map(world, 'USAgree', 'Average US Voting Agreement by Country', 'OrRd', 'US_agreement_map.png')