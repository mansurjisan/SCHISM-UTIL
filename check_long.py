import xarray as xr
import numpy as np

def check_and_fix_longitude(file_path, output_file=None):
    """
    Check longitude format and convert if needed
    """
    # Open the file
    ds = xr.open_dataset(file_path)
    
    print("Original Data:")
    print("Longitude range:", ds.longitude.min().values, "to", ds.longitude.max().values)
    print("First few longitude values:", ds.longitude.values[:10])
    
    # Check if we need to convert
    if ds.longitude.max() > 180:
        print("\nConverting longitudes from [0,360] to [-180,180]...")
        
        # Convert longitude values
        ds = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180))
        
        # Sort by the new longitude values
        ds = ds.sortby('longitude')
        
        print("\nAfter conversion:")
        print("Longitude range:", ds.longitude.min().values, "to", ds.longitude.max().values)
        print("First few longitude values:", ds.longitude.values[:10])
        
        if output_file:
            ds.to_netcdf(output_file)
            print(f"\nSaved converted file to: {output_file}")
    else:
        print("\nLongitudes already in [-180,180] format")
    
    return ds

# Check and fix the file
input_file = '463b6126c4bd8f1a9ea574a1fb1b8333.nc'
output_file = '463b6126c4bd8f1a9ea574a1fb1b8333_lonfix.nc'

# Run the check and conversion
ds = check_and_fix_longitude(input_file, output_file)

# Print specific region for Duck, NC
lon_min, lon_max = -76.0, -75.0
lat_min, lat_max = 35.5, 36.5

print("\nChecking data for Duck, NC region:")
region = ds.sel(longitude=slice(lon_min, lon_max),
                latitude=slice(lat_min, lat_max))

print(f"Points in region: {len(region.longitude)} x {len(region.latitude)}")
print("\nLongitude values in region:")
print(region.longitude.values)
print("\nLatitude values in region:")
print(region.latitude.values)
