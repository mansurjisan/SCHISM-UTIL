import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.dates import DateFormatter

# Create wind data
wind_data = pd.DataFrame({
    'dateTime': pd.date_range(start='2012-10-27', end='2012-10-29 08:30:00', freq='30min'),
    'speed': [7.435, 7.867, 7.881, 7.500, 6.932, 7.278, 6.264, 7.179, 7.617, 7.835, 8.565, 9.256,
              9.793, 10.035, 10.356, 11.219, 11.297, 11.822, 11.872, 11.680, 11.865, 12.675, 12.040, 13.055,
              12.987, 12.603, 12.478, 12.535, 12.639, 12.522, 12.608, 12.004, 12.186, 11.858, 12.465, 12.873,
              12.411, 12.042, 12.734, 13.210, 13.390, 13.921, 13.820, 15.133, 15.497, 15.357, 15.563, 15.947,
              16.063, 15.598, 16.754, 16.375, 16.246, 16.708, 16.339, 16.667, 16.734, 17.334, 17.522, 17.281,
              18.253, 18.938, 18.528, 18.914, 18.363, 18.043, 20.115, 19.516, 19.500, 18.946, 19.916, 19.778,
              20.737, 21.654, 21.509, 21.167, 20.761, 20.336, 19.828, 20.321, 21.468, 20.963, 19.400, 20.505,
              21.002, 21.494, 22.033, 22.547, 22.369, 21.541, 21.838, 21.473, 22.517, 21.344, 20.096, 21.376,
              21.580, 19.860, 19.147, 19.200, 18.670, 17.536, 18.191, 17.616, 17.371, 20.569, 20.157, 17.039,
              18.014, 18.326, 17.106, 18.376, 16.802, 19.425],
    'direction': [52.684, 50.328, 51.388, 49.623, 46.142, 44.897, 45.672, 48.873, 41.814, 43.537, 44.955, 43.750,
                 42.355, 43.548, 43.907, 43.125, 45.109, 38.934, 44.363, 39.335, 42.201, 47.360, 47.326, 43.120,
                 45.451, 45.420, 48.061, 48.836, 45.791, 43.182, 44.511, 44.485, 47.284, 45.678, 40.425, 36.488,
                 38.103, 34.658, 34.380, 32.303, 30.680, 27.824, 29.178, 28.648, 28.627, 26.666, 27.069, 25.735,
                 21.864, 20.976, 19.892, 17.549, 19.986, 24.324, 23.454, 22.903, 22.044, 22.285, 18.202, 17.999,
                 17.343, 18.969, 17.374, 15.652, 15.142, 15.404, 15.269, 14.274, 13.791, 13.270, 12.537, 11.233,
                 10.915, 9.788, 7.362, 4.169, 4.359, 2.788, 1.600, 2.616, 4.127, 359.323, 0.767, 1.947,
                 357.784, 357.214, 354.653, 354.065, 353.572, 353.580, 353.640, 350.784, 348.906, 345.500, 350.426, 350.858,
                 348.539, 348.731, 343.537, 350.634, 349.832, 346.447, 348.072, 348.998, 354.848, 9.243, 11.261, 4.050,
                 358.792, 0.148, 350.151, 358.435, 352.459, 358.425]
})

# Create figure with two subplots
fig, (ax1) = plt.subplots(1, 1, figsize=(15, 6))
#fig, ax1 = plt.figure(figsize=(15, 6))
date_format = DateFormatter('%b %d %HZ')

# Plot wind speed

ax1.plot(wind_data['dateTime'], wind_data['speed'], 'b-', linewidth=2)
ax1.xaxis.set_major_formatter(date_format)

ax1.set_title('Hurricane Sandy Observed Wind Speed (Duck, NC - October 27-29, 2012)', fontsize=12, pad=10)
ax1.set_xlabel('Date/Time')
#ax1.set_ylabel('Wind Speed (m/s)')
ax1.set_ylabel('Wind Speed (m s$^{-1}$)')  # using matplotlib's LaTeX

ax1.grid(True, linestyle='--', alpha=0.7)
ax1.tick_params(axis='x', rotation=45)

y_ticks = np.arange(5, 30, 5)  # Creates array [0, 5, 10, 15, 20]
ax1.set_yticks(y_ticks)



# Add annotations for max and min speed
max_speed = wind_data['speed'].max()
min_speed = wind_data['speed'].min()
max_time = wind_data.loc[wind_data['speed'].idxmax(), 'dateTime']
min_time = wind_data.loc[wind_data['speed'].idxmin(), 'dateTime']

ax1.annotate(f'Max: {max_speed:.1f} m s$^{{-1}}$', 
             xy=(max_time, max_speed),
             xytext=(10, 10), textcoords='offset points')

#ax1.annotate(f'Max: {max_speed:.1f} m s$^{{-1}}$',
#             xy=(max_time, max_speed),
#             xytext=(10, 10), textcoords='offset points')

ax1.annotate(f'Min: {min_speed:.1f} m s$^{{-1}}$',
             xy=(min_time, min_speed),
             xytext=(10, -15), textcoords='offset points')

# Plot wind direction
#ax2.plot(wind_data['dateTime'], wind_data['direction'], 'g-', linewidth=2)
#ax2.set_title('Wind Direction Time Series', fontsize=12, pad=10)
#ax2.set_xlabel('Date/Time')
#ax2.set_ylabel('Wind Direction (degrees)')
#ax2.grid(True, linestyle='--', alpha=0.7)
#ax2.tick_params(axis='x', rotation=45)
#
## Adjust y-axis to show complete 0-360 range
#ax2.set_ylim(0, 360)
#
# Add horizontal lines for cardinal directions
#cardinal_directions = {0: 'N', 90: 'E', 180: 'S', 270: 'W', 360: 'N'}
#for degree, direction in cardinal_directions.items():
#    ax2.axhline(y=degree, color='r', linestyle='--', alpha=0.3)
#    ax2.text(wind_data['dateTime'].iloc[0], degree, direction, ha='right', va='center')
#
# Adjust layout
plt.tight_layout()

# Save plot
plt.savefig('wind_analysis.png', dpi=300, bbox_inches='tight')

# Show plot
plt.show()

# Print statistics
print("\nWind Statistics:")
print("-" * 50)
print(f"Start time: {wind_data['dateTime'].min()}")
print(f"End time: {wind_data['dateTime'].max()}")
print("\nWind Speed:")
print(f"Maximum: {wind_data['speed'].max():.1f} m/s")
print(f"Minimum: {wind_data['speed'].min():.1f} m/s")
print(f"Mean: {wind_data['speed'].mean():.1f} m/s")
print(f"Standard deviation: {wind_data['speed'].std():.1f} m/s")
print("\nWind Direction:")
print(f"Range: {wind_data['direction'].min():.1f}° to {wind_data['direction'].max():.1f}°")
print(f"Mean direction: {wind_data['direction'].mean():.1f}°")
