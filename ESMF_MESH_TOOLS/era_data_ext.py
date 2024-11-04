import xarray as xr
import numpy as np

# Read the ERA5 file
ds = xr.open_dataset('era5_data_19941012_19941014.nc')

# Get the first timestep
time_index = 0

# Extract u10 and v10 components for the first timestep
u10 = ds.u10.isel(valid_time=time_index)
v10 = ds.v10.isel(valid_time=time_index)

# Get the time value
time_value = ds.valid_time[time_index]

# Calculate wind speed magnitude
wind_speed = np.sqrt(u10**2 + v10**2)

# Print basic information
print(f"\nTime: {time_value.values}")

print("\nU10 Wind Component:")
print(f"Min: {u10.min().values:.2f} m/s")
print(f"Max: {u10.max().values:.2f} m/s")
print(f"Mean: {u10.mean().values:.2f} m/s")

print("\nV10 Wind Component:")
print(f"Min: {v10.min().values:.2f} m/s")
print(f"Max: {v10.max().values:.2f} m/s")
print(f"Mean: {v10.mean().values:.2f} m/s")

print("\nWind Speed (magnitude):")
print(f"Min: {wind_speed.min().values:.2f} m/s")
print(f"Max: {wind_speed.max().values:.2f} m/s")
print(f"Mean: {wind_speed.mean().values:.2f} m/s")

# For Duck Island region specifically
LON_MIN = -76.0
LON_MAX = -75.6
LAT_MIN = 36.0
LAT_MAX = 36.4

# Convert longitude to 0-360 format if needed
lon_min_360 = LON_MIN % 360
lon_max_360 = LON_MAX % 360

# Extract data for Duck Island region
duck_region = ds.sel(
    longitude=slice(lon_min_360, lon_max_360),
    latitude=slice(LAT_MAX, LAT_MIN),  # Note: ERA5 latitudes are typically in descending order
    valid_time=ds.valid_time[0]
)

# Calculate wind speed for Duck Island region
duck_u10 = duck_region.u10
duck_v10 = duck_region.v10
duck_wind_speed = np.sqrt(duck_u10**2 + duck_v10**2)

print("\nDuck Island Region:")
print(f"Number of points in region: {duck_wind_speed.size}")
print("\nU10 Wind Component (Duck Island):")
print(f"Min: {duck_u10.min().values:.2f} m/s")
print(f"Max: {duck_u10.max().values:.2f} m/s")
print(f"Mean: {duck_u10.mean().values:.2f} m/s")

print("\nV10 Wind Component (Duck Island):")
print(f"Min: {duck_v10.min().values:.2f} m/s")
print(f"Max: {duck_v10.max().values:.2f} m/s")
print(f"Mean: {duck_v10.mean().values:.2f} m/s")

print("\nWind Speed (Duck Island):")
print(f"Min: {duck_wind_speed.min().values:.2f} m/s")
print(f"Max: {duck_wind_speed.max().values:.2f} m/s")
print(f"Mean: {duck_wind_speed.mean().values:.2f} m/s")

# Close the dataset
ds.close()
