import pandas as pd
import matplotlib.pyplot as plt


def plot_ideology_trends(data):
    countries = data['Countryname'].unique()

    for country in countries:
        country_data = data[data['Countryname'] == country]

        plt.figure(figsize=(12, 5))

        # Plot Ideal Point (Neutral Ideology Trend)
        plt.subplot(1, 3, 1)
        plt.plot(country_data['session'], country_data['IdealPointAll'], marker='o', linestyle='-', label='Ideal Point')
        plt.axhline(0, color='red', linestyle='--', label='Neutral Ideology')
        plt.title(f'{country} - Ideological Position')
        plt.xlabel('UNGA Session')
        plt.ylabel('Ideal Point')
        plt.legend()
        plt.grid(alpha=0.5)

        # Plot US Alignment
        plt.subplot(1, 3, 2)
        plt.plot(country_data['session'], country_data['USAgree'], marker='o', linestyle='-', label='US Agreement',
                 color='blue')
        plt.axhline(0.5, color='gray', linestyle='--', alpha=0.7)
        plt.title(f'{country} - Alignment with US')
        plt.xlabel('UNGA Session')
        plt.ylabel('Voting Similarity')
        plt.legend()
        plt.grid(alpha=0.5)

        # Plot China Alignment
        plt.subplot(1, 3, 3)
        plt.plot(country_data['session'], country_data['ChinaAgree'], marker='o', linestyle='-',
                 label='China Agreement', color='green')
        plt.axhline(0.5, color='gray', linestyle='--', alpha=0.7)
        plt.title(f'{country} - Alignment with China')
        plt.xlabel('UNGA Session')
        plt.ylabel('Voting Similarity')
        plt.legend()
        plt.grid(alpha=0.5)

        plt.tight_layout()
        plt.show()


# Load dataset
file_path = 'IdealpointestimatesAll_Jun2024.csv'
df = pd.read_csv(file_path)

# Keep relevant columns and drop missing values
unga_data = df[['Countryname', 'session', 'IdealPointAll', 'USAgree', 'ChinaAgree']].dropna()

# Run the function to generate graphs
plot_ideology_trends(unga_data)
