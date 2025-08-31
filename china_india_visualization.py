import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv("china_india_regression_data.csv")  # Replace with your actual file path

# Group by country (ISO code) and aggregate
agg_data = df.groupby("gid_0").agg({
    "CHN_comm": "sum",
    "IND_comm": "sum",
    "ChinaAgree": "mean",
    "IndiaAgree": "mean"
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


# Plot China Commitments Map
plot_world_map(world, 'CHN_comm', 'Total CHN Commitments by Country', 'Blues', 'CHN_commitments_map.png')
# Plot China Commitments Map
plot_world_map(world, 'IND_comm', 'Total IND Commitments by Country', 'Blues', 'IND_commitments_map.png')

# Plot China Agreement Map
plot_world_map(world, 'ChinaAgree', 'Average China Voting Agreement by Country', 'OrRd', 'China_agreement_map.png')
# Plot India Agreement Map
plot_world_map(world, 'IndiaAgree', 'Average India Voting Agreement by Country', 'OrRd', 'India_agreement_map.png')