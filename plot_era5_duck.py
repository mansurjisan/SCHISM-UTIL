import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np
import os
import pandas as pd

# Create output directory if it doesn't exist
output_dir = 'wspd_maps_era5'
os.makedirs(output_dir, exist_ok=True)

# Set the fixed colorbar range
VMIN = 0
VMAX = 20

# Define the region of interest around Duck Island, NC
LON_MIN = -76.0  # Western boundary
LON_MAX = -75.6  # Eastern boundary
LAT_MIN = 36.0   # Southern boundary
LAT_MAX = 36.4   # Northern boundary

# Convert negative longitudes to 0-360 format
def convert_lon_360(lon):
    return lon % 360

def plot_velocity(ds, time_index, time_value):
    # Convert our region boundaries to 0-360 format
    lon_min_360 = convert_lon_360(LON_MIN)
    lon_max_360 = convert_lon_360(LON_MAX)
    
    print(f"Converting longitude range {LON_MIN}° to {LON_MAX}° → {lon_min_360}° to {lon_max_360}°")
    
    # Extract u and v components for the region of interest
    data_slice = ds.sel(
        longitude=slice(lon_min_360, lon_max_360),
        latitude=slice(LAT_MAX, LAT_MIN),  # Note: ERA5 latitudes are in descending order
        valid_time=time_value
    )
    
    if data_slice.sizes['longitude'] == 0 or data_slice.sizes['latitude'] == 0:
        print("No data found in the specified region!")
        print(f"Available longitude range: {ds.longitude.min().values:.2f}° to {ds.longitude.max().values:.2f}°")
        print(f"Available latitude range: {ds.latitude.min().values:.2f}° to {ds.latitude.max().values:.2f}°")
        return
    
    # Calculate wind speed magnitude
    wind_speed = np.sqrt(data_slice.u10**2 + data_slice.v10**2)
    
    # Calculate min/max for the region
    velmin_filtered = float(wind_speed.min())
    velmax_filtered = float(wind_speed.max())
    print(f"Min wind speed in Duck Island region: {velmin_filtered:.2f} m/s")
    print(f"Max wind speed in Duck Island region: {velmax_filtered:.2f} m/s")

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), 
                          subplot_kw={'projection': ccrs.PlateCarree()})

    # Convert longitudes back to -180 to 180 for plotting
    lons = data_slice.longitude.values
    lons_180 = np.where(lons > 180, lons - 360, lons)
    
    # Plot wind speed
    im = ax.pcolormesh(lons_180, data_slice.latitude, wind_speed, 
                       transform=ccrs.PlateCarree(),
                       cmap='jet', shading='auto', 
                       vmin=VMIN, vmax=VMAX)

    # Add coastlines and land features
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    ax.add_feature(cfeature.LAND.with_scale('10m'), facecolor='lightgray')

    # Customize tick parameters
    ax.tick_params(axis='both', which='major', labelsize=10, pad=5, 
                  direction='out')
    ax.tick_params(axis='both', which='minor', length=0)

    # Add labels to the axes
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, orientation='vertical', pad=0.05, 
                       extend='max')
    cbar.set_label('Wind Speed (m/s)')

    # Set map extent to focus on Duck Island
    ax.set_extent([LON_MIN, LON_MAX, LAT_MIN, LAT_MAX])

    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlocator = plt.FixedLocator(np.arange(LON_MIN, LON_MAX + 0.1, 0.1))
    gl.ylocator = plt.FixedLocator(np.arange(LAT_MIN, LAT_MAX + 0.1, 0.1))
    
    # Format latitude/longitude labels
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    # Add title with timestamp and min/max values
    plt.title(f"ERA5 Wind Speed near Duck Island, NC at {time_value}\n" +
             f"Min: {velmin_filtered:.2f} m/s, Max: {velmax_filtered:.2f} m/s")

    # Save the plot
    plt.switch_backend('Agg')
    output_file = os.path.join(output_dir, 
                              f"era5_wspd_plot_{time_value.strftime('%Y%m%d_%H%M%S')}.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

# Set the backend at the start
plt.switch_backend('Agg')

# Read ERA5 data
print("Reading ERA5 data...")
ds = xr.open_dataset('era5_data_20220913_20220915.nc')

# Convert times to datetime
times = pd.to_datetime(ds.valid_time.values, unit='s')

# Print some diagnostic information
print(f"\nDataset coordinates:")
print(f"Longitude range: {ds.longitude.min().values:.2f}° to {ds.longitude.max().values:.2f}°")
print(f"Latitude range: {ds.latitude.min().values:.2f}° to {ds.latitude.max().values:.2f}°")
print(f"Time range: {times[0]} to {times[-1]}")
print(f"\nRequested region:")
print(f"Longitude: {LON_MIN}° to {LON_MAX}° (will be converted to 0-360° format)")
print(f"Latitude: {LAT_MIN}° to {LAT_MAX}°")
print("\nStarting processing...")

# Loop through all time steps
for time_index, time_value in enumerate(times):
    print(f"\nProcessing time step {time_index + 1}: {time_value}")
    plot_velocity(ds, time_index, time_value)

ds.close()

print("\nAll plots have been generated and saved.")
