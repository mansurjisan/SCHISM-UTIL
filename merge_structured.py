import xarray as xr
import numpy as np
from netCDF4 import Dataset
import glob
import os
from datetime import datetime

def merge_structured_grid_files(base_pattern, start_id, end_id, output_file):
    """
    Merge multiple structured grid netCDF files into a single file.
    
    Parameters:
    -----------
    base_pattern : str
        Base pattern for files (e.g., 'pahm_windout-florence_STR{}.nc')
    start_id : int
        Starting ID number
    end_id : int
        Ending ID number
    output_file : str
        Name of the output merged file
    """
    # Generate list of files
    files = []
    for i in range(start_id, end_id + 1):
        filename = base_pattern.format(i)
        if os.path.exists(filename):
            files.append(filename)
        else:
            print(f"Warning: File not found - {filename}")
    
    if not files:
        raise ValueError("No files found to merge")
    
    print(f"Found {len(files)} files to merge")
    
    # Open all files using xarray
    datasets = []
    for f in files:
        print(f"Reading {f}")
        ds = xr.open_dataset(f)
        datasets.append(ds)
    
    # Merge along the time dimension
    print("Merging datasets...")
    merged = xr.concat(datasets, dim='time')
    
    # Sort by time
    merged = merged.sortby('time')
    
    # Remove any duplicate time steps
    _, index = np.unique(merged['time'], return_index=True)
    merged = merged.isel(time=index)
    
    # Update global attributes
    merged.attrs['source'] = 'PaHM'
    merged.attrs['field type'] = '1 hr'
    merged.attrs['content'] = '10-meter wind components and Pressure Reduced to MSL'
    merged.attrs['start_date'] = str(merged['time'].values[0])
    merged.attrs['stop_date'] = str(merged['time'].values[-1])
    
    # Save to netCDF file
    print(f"Saving merged data to {output_file}")
    merged.to_netcdf(output_file)
    
    # Close all datasets
    for ds in datasets:
        ds.close()
    
    # Print summary
    with Dataset(output_file, 'r') as nc:
        print("\nMerged file summary:")
        print(f"Dimensions:")
        for dim in nc.dimensions:
            print(f"  {dim}: {len(nc.dimensions[dim])}")
        print(f"\nTime range:")
        print(f"  Start: {nc.start_date}")
        print(f"  Stop: {nc.stop_date}")
        print(f"\nVariables:")
        for var in nc.variables:
            if var not in ['longitude', 'latitude', 'time']:
                print(f"  {var}: {nc.variables[var].shape}")

def verify_merged_file(output_file):
    """
    Verify the merged file for data consistency.
    """
    with Dataset(output_file, 'r') as nc:
        # Check for missing values
        for var in ['uwnd', 'vwnd', 'P']:
            data = nc.variables[var][:]
            missing = np.sum(data == nc.variables[var]._FillValue)
            total = np.prod(data.shape)
            print(f"\n{var} statistics:")
            print(f"  Total points: {total}")
            print(f"  Missing values: {missing} ({missing/total*100:.2f}%)")
            print(f"  Value range: {np.nanmin(data):.2f} to {np.nanmax(data):.2f}")

# Example usage
if __name__ == "__main__":
    base_pattern = "pahm_windout-florence_STR{}.nc"
    start_id = 1
    end_id = 21
    output_file = "merged_florence_structured.nc"
    
    merge_structured_grid_files(base_pattern, start_id, end_id, output_file)
    verify_merged_file(output_file)
