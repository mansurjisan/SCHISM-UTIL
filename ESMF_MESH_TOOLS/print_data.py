import xarray as xr
import numpy as np
import pandas as pd

# Read the data
print("Reading ERA5 data...")
ds = xr.open_dataset('era5_data_19941012_19941014_rot_fix.nc')

# Define region (Duck Island)
LON_MIN = -76.0
LON_MAX = -75.6
LAT_MIN = 36.0
LAT_MAX = 36.4

# Convert longitude to 0-360 format
lon_min_360 = (LON_MIN + 360) % 360
lon_max_360 = (LON_MAX + 360) % 360

print(f"\nConverting longitude range:")
print(f"Original: {LON_MIN}° to {LON_MAX}°")
print(f"0-360 format: {lon_min_360}° to {lon_max_360}°")

# Print the first few and last few latitude values
print("\nChecking latitude values:")
print("First 5 latitudes:", ds.latitude.values[:5])
print("Last 5 latitudes:", ds.latitude.values[-5:])

# Find the closest latitude indices
lat_indices = np.where((ds.latitude >= LAT_MIN) & (ds.latitude <= LAT_MAX))[0]
print("\nLatitude indices in our range:", lat_indices)
print("Corresponding latitude values:", ds.latitude.values[lat_indices])

# Find the closest longitude indices
lon_indices = np.where((ds.longitude >= lon_min_360) & (ds.longitude <= lon_max_360))[0]
print("\nLongitude indices in our range:", lon_indices)
print("Corresponding longitude values:", ds.longitude.values[lon_indices])

# Get data using numerical indexing instead of coordinate selection
if len(lat_indices) > 0 and len(lon_indices) > 0:
    print("\nExtracting data using indices...")
    data = ds.isel(
        latitude=lat_indices,
        longitude=lon_indices,
        time=0
    )
    
    print("\nData dimensions in selected region:")
    print(f"Longitude points: {len(data.longitude)}")
    print(f"Latitude points: {len(data.latitude)}")
    
    print("\nWind components:")
    print("\nU10 values:")
    print(data.u10.values)
    print("\nV10 values:")
    print(data.v10.values)
    
    # Calculate wind speed
    wind_speed = np.sqrt(data.u10**2 + data.v10**2)
    
    print("\nWind Speed:")
    print(wind_speed.values)
    
    print("\nSummary statistics:")
    print(f"U10 range: {data.u10.min().values:.2f} to {data.u10.max().values:.2f} {data.u10.units}")
    print(f"V10 range: {data.v10.min().values:.2f} to {data.v10.max().values:.2f} {data.v10.units}")
    print(f"Wind Speed range: {wind_speed.min().values:.2f} to {wind_speed.max().values:.2f} {data.u10.units}")
else:
    print("\nNo matching indices found!")
    
# Print exact coordinate spacing
print("\nCoordinate spacing:")
print("Longitude spacing:", np.diff(ds.longitude.values[:5]))
print("Latitude spacing:", np.diff(ds.latitude.values[:5]))

ds.close()
