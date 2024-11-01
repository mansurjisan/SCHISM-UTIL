import netCDF4 as nc
from datetime import datetime, timezone

def check_time_range(filename):
    """
    Check the time range of a NetCDF file with valid_time variable in seconds since 1970-01-01
    
    Parameters:
    filename (str): Path to the NetCDF file
    """
    try:
        # Open the NetCDF file
        ds = nc.Dataset(filename, 'r')
        
        # Get the valid_time variable
        time_var = ds.variables['time']
        
        # Get the time values (these are seconds since 1970-01-01)
        time_values = time_var[:]
        
        # Convert seconds since epoch to datetime objects
        start_date = datetime.fromtimestamp(time_values[0], tz=timezone.utc)
        end_date = datetime.fromtimestamp(time_values[-1], tz=timezone.utc)
        
        print(f"Time dimension size: {len(time_values)} timesteps")
        print(f"Start time: {start_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"End time: {end_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        # Print all timestamps if there are few of them
        if len(time_values) <= 10:
            print("\nAll timestamps:")
            for t in time_values:
                dt = datetime.fromtimestamp(t, tz=timezone.utc)
                print(f"  {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        ds.close()
        
    except Exception as e:
        print(f"Error reading netCDF file: {str(e)}")

# Usage example
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "download.nc"  # default filename
    
    check_time_range(filename)
