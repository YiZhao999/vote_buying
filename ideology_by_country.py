import pandas as pd
import matplotlib.pyplot as plt


def plot_ideology_trend(country_name):
    file_path = 'IdealpointestimatesAll_Jun2024.csv'
    unga_data = pd.read_csv(file_path)
    unga_data = unga_data[['Countryname', 'session', 'IdealPointAll', 'USAgree', 'ChinaAgree']]
    neutral_ideology = 0  # Reference point for neutrality
    us_ideal_points = unga_data[unga_data['Countryname'] == 'United States'][['session', 'IdealPointAll']]
    china_ideal_points = unga_data[unga_data['Countryname'] == 'China'][['session', 'IdealPointAll']]

    unga_data = unga_data.merge(us_ideal_points, on='session', suffixes=('', '_US'))
    unga_data = unga_data.merge(china_ideal_points, on='session', suffixes=('', '_China'))

    unga_data['Distance_Neutral'] = abs(unga_data['IdealPointAll'] - neutral_ideology)
    unga_data['Distance_US'] = abs(unga_data['IdealPointAll'] - unga_data['IdealPointAll_US'])
    unga_data['Distance_China'] = abs(unga_data['IdealPointAll'] - unga_data['IdealPointAll_China'])

    if country_name not in unga_data['Countryname'].unique():
        print(f"Country '{country_name}' not found in the dataset.")
        return

    country_data = unga_data[unga_data['Countryname'] == country_name]

    plt.figure(figsize=(10, 5))
    plt.plot(country_data['session'], country_data['IdealPointAll'], marker='o', linestyle='-',
             label=f'{country_name} Ideal Point')
    plt.plot(us_ideal_points['session'], us_ideal_points['IdealPointAll'], linestyle='--', color='blue',
             label='U.S. Ideology')
    plt.plot(china_ideal_points['session'], china_ideal_points['IdealPointAll'], linestyle='--', color='red',
             label='China Ideology')

    plt.title(f'Ideological Trend of {country_name} in UNGA')
    plt.xlabel('UNGA Session')
    plt.ylabel('Ideal Point Estimate')
    plt.legend()
    plt.grid(alpha=0.5)
    plt.show()

# Example usage
plot_ideology_trend('Singapore')
