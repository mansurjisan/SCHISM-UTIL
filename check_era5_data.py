import netCDF4 as nc
from datetime import datetime, timezone
import numpy as np

def check_file_ranges(filename):
    """
    Check the time range and spatial coverage of a NetCDF file
    
    Parameters:
    filename (str): Path to the NetCDF file
    """
    try:
        # Open the NetCDF file
        ds = nc.Dataset(filename, 'r')
        
        print("=== Temporal Information ===")
        # Get the valid_time variable
        time_var = ds.variables['valid_time']
        
        # Get the time values (these are seconds since 1970-01-01)
        time_values = time_var[:]
        
        # Convert seconds since epoch to datetime objects
        start_date = datetime.fromtimestamp(time_values[0], tz=timezone.utc)
        end_date = datetime.fromtimestamp(time_values[-1], tz=timezone.utc)
        
        print(f"Time dimension size: {len(time_values)} timesteps")
        print(f"Start time: {start_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"End time: {end_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        # Print all timestamps 
        if len(time_values) <= 50:
            print("\nAll timestamps:")
            for t in time_values:
                dt = datetime.fromtimestamp(t, tz=timezone.utc)
                print(f"  {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        print("\n=== Spatial Information ===")
        # Get latitude and longitude variables
        lat = ds.variables['latitude'][:]
        lon = ds.variables['longitude'][:]

        lat_first = ds.variables['latitude'][0]
        lat_last = ds.variables['latitude'][-1]
        
        lon_first = ds.variables['longitude'][0]
        lon_last = ds.variables['longitude'][-1]


        # Print latitude range
        print("Latitude range:")
        print(f"  Min: {np.nanmin(lat):.4f}°N")
        print(f"  Max: {np.nanmax(lat):.4f}°N")
        print(f"  Resolution: {abs(lat[1] - lat[0]):.4f}°")
        print(f"  Number of points: {len(lat)}")
        print(f"First longitude point: {lat_first:.4f}°E")
        print(f"Last longitude point: {lat_last:.4f}°E")

        # Print longitude range
        print("\nLongitude range:")
        print(f"  Min: {np.nanmin(lon):.4f}°E")
        print(f"  Max: {np.nanmax(lon):.4f}°E")
        print(f"  Resolution: {abs(lon[1] - lon[0]):.4f}°")
        print(f"  Number of points: {len(lon)}")
        print(f"First longitude point: {lon_first:.4f}°E")
        print(f"Last longitude point: {lon_last:.4f}°E")
        
        # Print grid size
        print(f"\nTotal grid points: {len(lat) * len(lon):,}")
        
        # Print available variables
        print("\n=== Available Variables ===")
        for var_name, var in ds.variables.items():
            if len(var.dimensions) > 1:  # Only print variables that are likely to be data fields
                print(f"  {var_name}: {var.dimensions}")
        
        ds.close()
        
    except Exception as e:
        print(f"Error reading netCDF file: {str(e)}")

# Usage example
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "f27b25f3938b43a8e9c79d2979cc20ba.nc"  # default filename
    
    check_file_ranges(filename)
