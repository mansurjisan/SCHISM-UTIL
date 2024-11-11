import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import seaborn as sns
from datetime import datetime

# Set style for better visualization

#plt.style.use('seaborn-v0_8-darkgrid')  # or
#sns.set_palette("husl")

# Create the water level data
water_level_data = [
    {"dateTime":"20121027 000000", "level":0.437},
    {"dateTime":"20121027 003000", "level":0.329},
    {"dateTime":"20121027 010000", "level":0.160},
    {"dateTime":"20121027 013000", "level":0.034},
    {"dateTime":"20121027 020000", "level":-0.108},
    {"dateTime":"20121027 023000", "level":-0.200},
    {"dateTime":"20121027 030000", "level":-0.247},
    {"dateTime":"20121027 033000", "level":-0.283},
    {"dateTime":"20121027 040000", "level":-0.301},
    {"dateTime":"20121027 043000", "level":-0.308},
    {"dateTime":"20121027 050000", "level":-0.249},
    {"dateTime":"20121027 053000", "level":-0.171},
    {"dateTime":"20121027 060000", "level":-0.035},
    {"dateTime":"20121027 063000", "level":0.047},
    {"dateTime":"20121027 070000", "level":0.246},
    {"dateTime":"20121027 073000", "level":0.349},
    {"dateTime":"20121027 080000", "level":0.515},
    {"dateTime":"20121027 083000", "level":0.656},
    {"dateTime":"20121027 090000", "level":0.728},
    {"dateTime":"20121027 093000", "level":0.839},
    {"dateTime":"20121027 100000", "level":0.860},
    {"dateTime":"20121027 103000", "level":0.886},
    {"dateTime":"20121027 110000", "level":0.871},
    {"dateTime":"20121027 113000", "level":0.840},
    {"dateTime":"20121027 120000", "level":0.736},
    {"dateTime":"20121027 123000", "level":0.656},
    {"dateTime":"20121027 130000", "level":0.570},
    {"dateTime":"20121027 133000", "level":0.459},
    {"dateTime":"20121027 140000", "level":0.348},
    {"dateTime":"20121027 143000", "level":0.179},
    {"dateTime":"20121027 150000", "level":0.100},
    {"dateTime":"20121027 153000", "level":-0.029},
    {"dateTime":"20121027 160000", "level":-0.017},
    {"dateTime":"20121027 163000", "level":-0.071},
    {"dateTime":"20121027 170000", "level":-0.086},
    {"dateTime":"20121027 173000", "level":-0.047},
    {"dateTime":"20121027 180000", "level":-0.021},
    {"dateTime":"20121027 183000", "level":0.051},
    {"dateTime":"20121027 190000", "level":0.175},
    {"dateTime":"20121027 193000", "level":0.289},
    {"dateTime":"20121027 200000", "level":0.411},
    {"dateTime":"20121027 203000", "level":0.550},
    {"dateTime":"20121027 210000", "level":0.687},
    {"dateTime":"20121027 213000", "level":0.731},
    {"dateTime":"20121027 220000", "level":0.823},
    {"dateTime":"20121027 223000", "level":0.916},
    {"dateTime":"20121027 230000", "level":0.936},
    {"dateTime":"20121027 233000", "level":0.849},
    {"dateTime":"20121028 000000", "level":0.882},
    {"dateTime":"20121028 003000", "level":0.822},
    {"dateTime":"20121028 010000", "level":0.723},
    {"dateTime":"20121028 013000", "level":0.526},
    {"dateTime":"20121028 020000", "level":0.509},
    {"dateTime":"20121028 023000", "level":0.453},
    {"dateTime":"20121028 030000", "level":0.378},
    {"dateTime":"20121028 033000", "level":0.228},
    {"dateTime":"20121028 040000", "level":0.184},
    {"dateTime":"20121028 043000", "level":0.202},
    {"dateTime":"20121028 050000", "level":0.264},
    {"dateTime":"20121028 053000", "level":0.249},
    {"dateTime":"20121028 060000", "level":0.414},
    {"dateTime":"20121028 063000", "level":0.454},
    {"dateTime":"20121028 070000", "level":0.534},
    {"dateTime":"20121028 073000", "level":0.620},
    {"dateTime":"20121028 080000", "level":0.836},
    {"dateTime":"20121028 083000", "level":0.994},
    {"dateTime":"20121028 090000", "level":1.065},
    {"dateTime":"20121028 093000", "level":1.212},
    {"dateTime":"20121028 100000", "level":1.257},
    {"dateTime":"20121028 103000", "level":1.349},
    {"dateTime":"20121028 110000", "level":1.327},
    {"dateTime":"20121028 113000", "level":1.377},
    {"dateTime":"20121028 120000", "level":1.369},
    {"dateTime":"20121028 123000", "level":1.307},
    {"dateTime":"20121028 130000", "level":1.165},
    {"dateTime":"20121028 133000", "level":1.109},
    {"dateTime":"20121028 140000", "level":0.990},
    {"dateTime":"20121028 143000", "level":0.922},
    {"dateTime":"20121028 150000", "level":0.745},
    {"dateTime":"20121028 153000", "level":0.764},
    {"dateTime":"20121028 160000", "level":0.600},
    {"dateTime":"20121028 163000", "level":0.536},
    {"dateTime":"20121028 170000", "level":0.427},
    {"dateTime":"20121028 173000", "level":0.530},
    {"dateTime":"20121028 180000", "level":0.473},
    {"dateTime":"20121028 183000", "level":0.575},
    {"dateTime":"20121028 190000", "level":0.632},
    {"dateTime":"20121028 193000", "level":0.667},
    {"dateTime":"20121028 200000", "level":0.745},
    {"dateTime":"20121028 203000", "level":0.880},
    {"dateTime":"20121028 210000", "level":1.000},
    {"dateTime":"20121028 213000", "level":1.097},
    {"dateTime":"20121028 220000", "level":1.215},
    {"dateTime":"20121028 223000", "level":1.222},
    {"dateTime":"20121028 230000", "level":1.229},
    {"dateTime":"20121028 233000", "level":1.279},
    {"dateTime":"20121029 000000", "level":1.229},
    {"dateTime":"20121029 003000", "level":1.162},
    {"dateTime":"20121029 010000", "level":1.161},
    {"dateTime":"20121029 013000", "level":1.060},
    {"dateTime":"20121029 020000", "level":0.936},
    {"dateTime":"20121029 023000", "level":0.863},
    {"dateTime":"20121029 030000", "level":0.745},
    {"dateTime":"20121029 033000", "level":0.693},
    {"dateTime":"20121029 040000", "level":0.579},
    {"dateTime":"20121029 043000", "level":0.574},
    {"dateTime":"20121029 050000", "level":0.636},
    {"dateTime":"20121029 053000", "level":0.611},
    {"dateTime":"20121029 060000", "level":0.537},
    {"dateTime":"20121029 063000", "level":0.670},
    {"dateTime":"20121029 070000", "level":0.801},
    {"dateTime":"20121029 073000", "level":0.793},
    {"dateTime":"20121029 080000", "level":1.004},
    {"dateTime":"20121029 083000", "level":1.142}
]


# Convert to DataFrame
df = pd.DataFrame(water_level_data)
df['dateTime'] = pd.to_datetime(df['dateTime'], format='%Y%m%d %H%M%S')
start_time = df['dateTime'].min()

df['hours'] = (df['dateTime'] - start_time).dt.total_seconds() / 3600

# Create figure with multiple subplots

fig, (ax1) = plt.subplots(1, 1, figsize=(15, 6))
date_format = DateFormatter('%b %d %HZ')


# Plot 1: Time series

ax1.plot(df['dateTime'], df['level'], 'b-', linewidth=2)
ax1.xaxis.set_major_formatter(date_format)

ax1.set_title('Hurricane Sandy Observed Water Level (Duck, NC - October 27-29, 2012)', fontsize=12, pad=10)
ax1.set_xlabel('Date/Time')
ax1.set_ylabel('Water Level (m)')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.tick_params(axis='x', rotation=45)

y_ticks = np.arange(-1, 3, 1) 
ax1.set_yticks(y_ticks)


max_speed = df['level'].max()
min_speed = df['level'].min()
max_time  = df.loc[df['level'].idxmax(), 'dateTime']
min_time  = df.loc[df['level'].idxmin(), 'dateTime']

ax1.annotate(f'Max: {max_speed:.1f} m',
             xy=(max_time, max_speed),
             xytext=(10, 10), textcoords='offset points')
ax1.annotate(f'Min: {min_speed:.1f} m',
             xy=(min_time, min_speed),
             xytext=(10, -15), textcoords='offset points')




# Add horizontal line at zero

#plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)

# Set tick parameters to make them visible and clearer
#plt.tick_params(axis='both', direction='in', length=6, width=1.5, colors='black', grid_alpha=0.7)

# Add min and max annotations

#max_idx = df['level'].idxmax()
#min_idx = df['level'].idxmin()

#plt.annotate(f'Max: {df["level"].max():.2f}m',
#             xy=(df['dateTime'][max_idx], df['level'].max()),
#             xytext=(10, 10), textcoords='offset points')
#plt.annotate(f'Min: {df["level"].min():.2f}m',
#             xy=(df['dateTime'][min_idx], df['level'].min()),
#             xytext=(10, -10), textcoords='offset points')



plt.tight_layout()
plt.savefig('water_level_analysis2.png', dpi=300, bbox_inches='tight')
plt.show()

# Print statistical summary

print("-" * 50)
print(f"Start time: {start_time}")
print(f"End time: {df['dateTime'].max()}")
print(f"Duration: {df['hours'].max():.1f} hours")

print(f"\nWater Level Summary:")

print(f"Minimum: {df['level'].min():.3f} m")

print(f"Maximum: {df['level'].max():.3f} m")
