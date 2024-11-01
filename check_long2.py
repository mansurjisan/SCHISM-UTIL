import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def check_lat_lon_data(file_path, output_file=None):
    """
    Comprehensive check of latitude and longitude data
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
    
    region = ds_converted.sel(longitude=slice(lon_min, lon_max),
                            latitude=slice(lat_min, lat_max))
    
    print(f"\nPoints found in region:")
    print(f"Longitude points: {len(region.longitude)}")
    print(f"Latitude points: {len(region.latitude)}")
    
    print("\nExact longitude values in region:")
    print(region.longitude.values)
    print("\nExact latitude values in region:")
    print(region.latitude.values)
    
    # Check data values for one timestep
    print("\n=== Data Value Check ===")
    print("\nChecking first timestep:")
    time_step = 0
    
    for var in ['u10', 'v10', 'msl']:
        if var in ds:
            data = region[var].isel(time=time_step)
            print(f"\n{var}:")
            print(f"Min: {data.min().values:.2f}")
            print(f"Max: {data.max().values:.2f}")
            print(f"Mean: {data.mean().values:.2f}")
            
            # Check for missing or invalid values
            nans = np.isnan(data).sum()
            if nans > 0:
                print(f"Warning: Found {nans} NaN values!")
    
    # Create validation plot
    plt.figure(figsize=(15, 5))
    
    # Plot 1: Global coverage
    plt.subplot(121)
    plt.pcolormesh(ds_converted.longitude, ds_converted.latitude, 
                   ds_converted.u10.isel(time=0), shading='auto')
    plt.colorbar(label='U10 (m/s)')
    plt.title('Global Coverage (First Timestep)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    # Plot 2: Duck region
    plt.subplot(122)
    plt.pcolormesh(region.longitude, region.latitude, 
                   region.u10.isel(time=0), shading='auto')
    plt.colorbar(label='U10 (m/s)')
    plt.title('Duck Region (First Timestep)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    plt.tight_layout()
    plt.savefig('data_validation.png')
    plt.close()
    
    print("\n=== Time Information ===")
    print(f"Number of timesteps: {len(ds.time)}")
    print("Time values:")
    for t in ds.time.values:
        print(pd.Timestamp(t))

# Run the check
input_file = '463b6126c4bd8f1a9ea574a1fb1b8333.nc'
output_file = '463b6126c4bd8f1a9ea574a1fb1b8333_lonfix.nc'
check_lat_lon_data(input_file, output_file)
