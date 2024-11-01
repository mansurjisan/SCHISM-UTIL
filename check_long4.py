import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def check_lat_lon_data(file_path, output_file=None):
    """
    Comprehensive check of latitude and longitude data with wind speed calculation
    """
    # Open the file
    ds = xr.open_dataset(file_path)
    
    print("=== Data Overview ===")
    print("\nDimensions:")
    print(ds.dims)
    
    print("\nVariables:")
    for var in ds.variables:
        print(f"{var}: {ds[var].shape}")
    
    print("\n=== Coordinate Information ===")
    print("\nLatitude:")
    print(f"Range: {ds.latitude.min().values:.3f} to {ds.latitude.max().values:.3f}")
    print(f"Number of points: {len(ds.latitude)}")
    print(f"Resolution: {abs(float(ds.latitude[1] - ds.latitude[0])):.3f} degrees")
    print("First few values:", ds.latitude.values[:5])
    print("Last few values:", ds.latitude.values[-5:])
    
    print("\nLongitude:")
    print(f"Range: {ds.longitude.min().values:.3f} to {ds.longitude.max().values:.3f}")
    print(f"Number of points: {len(ds.longitude)}")
    print(f"Resolution: {abs(float(ds.longitude[1] - ds.longitude[0])):.3f} degrees")
    print("First few values:", ds.longitude.values[:5])
    print("Last few values:", ds.longitude.values[-5:])
    
    # Check ordering of latitude
    print("\nLatitude ordering:", "Descending" if ds.latitude[0] > ds.latitude[-1] else "Ascending")
    
    # Calculate wind speed for first valid_time step
    print("\n=== Wind Speed at First Time Step ===")
    u10_t0 = ds.u10.isel(valid_time=0)
    v10_t0 = ds.v10.isel(valid_time=0)
    wind_speed_t0 = np.sqrt(u10_t0**2 + v10_t0**2)
    
    print(f"Wind Speed Statistics:")
    print(f"Minimum: {wind_speed_t0.min().values:.2f} m/s")
    print(f"Maximum: {wind_speed_t0.max().values:.2f} m/s")
    print(f"Mean: {wind_speed_t0.mean().values:.2f} m/s")
    
    # Check if longitude needs conversion
    needs_conversion = ds.longitude.max() > 180
    if needs_conversion:
        print("\nLongitude needs conversion from [0,360] to [-180,180]")
        
        # Convert longitude values
        ds_converted = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180))
        ds_converted = ds_converted.sortby('longitude')
        
        if output_file:
            ds_converted.to_netcdf(output_file)
            print(f"Saved converted file to: {output_file}")
    else:
        ds_converted = ds
        print("\nLongitude already in [-180,180] format")
    
    # Check specific region (Duck, NC area)
    lon_min, lon_max = -76.0, -75.0
    lat_min, lat_max = 35.5, 36.5
    
    print(f"\n=== Duck, NC Region Check ===")
    print(f"Target region: Lon [{lon_min}, {lon_max}], Lat [{lat_min}, {lat_max}]")
    
    # For descending latitude, we need to reverse min/max
    if ds.latitude[0] > ds.latitude[-1]:
        lat_slice = slice(lat_max, lat_min)  # For descending latitude
    else:
        lat_slice = slice(lat_min, lat_max)  # For ascending latitude
    
    region = ds_converted.sel(longitude=slice(lon_min, lon_max),
                            latitude=lat_slice)
    
    print(f"\nPoints found in region:")
    print(f"Longitude points: {len(region.longitude)}")
    print(f"Latitude points: {len(region.latitude)}")
    
    print("\nExact longitude values in region:")
    print(region.longitude.values)
    print("\nExact latitude values in region:")
    print(region.latitude.values)
    
    # Calculate wind speed for region at first valid_time step
    if len(region.longitude) > 0 and len(region.latitude) > 0:
        region_u10_t0 = region.u10.isel(valid_time=0)
        region_v10_t0 = region.v10.isel(valid_time=0)
        region_wspd_t0 = np.sqrt(region_u10_t0**2 + region_v10_t0**2)
        
        print("\nWind Speed in Region (First Time Step):")
        print(f"Minimum: {region_wspd_t0.min().values:.2f} m/s")
        print(f"Maximum: {region_wspd_t0.max().values:.2f} m/s")
        print(f"Mean: {region_wspd_t0.mean().values:.2f} m/s")
        
        # Print wind speed values at each point
        print("\nWind Speed values at each point:")
        for i in range(len(region.latitude)):
            for j in range(len(region.longitude)):
                lat = region.latitude.values[i]
                lon = region.longitude.values[j]
                wspd = region_wspd_t0.values[i,j]
                print(f"Lat: {lat:.2f}, Lon: {lon:.2f}, Wind Speed: {wspd:.2f} m/s")
    
    print("\n=== Time Information ===")
    print(f"Number of valid_timesteps: {len(ds.valid_time)}")
    print("Time values:")
    for t in ds.valid_time.values:
        print(pd.Timestamp(t))

# Run the check
input_file = 'era5_data_202209_202210_rot.nc'
output_file = 'download_inv_fix2.nc'
check_lat_lon_data(input_file, output_file)
