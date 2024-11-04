import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime

def process_era5_data(input_file, output_file):
    """
    Process ERA5 data to match the specified NetCDF format
    """
    # Open the file
    ds = xr.open_dataset(input_file)

    # Convert longitude to [-180, 180] range if needed
#    if ds.longitude.max() > 180:
#        ds = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180))
#        ds = ds.sortby('longitude')

    # Ensure latitude is in ascending order (-90 to 90)
#    if ds.latitude[0] > ds.latitude[-1]:
#        ds = ds.reindex(latitude=ds.latitude[::-1])

    # Convert time to hours since 1900-01-01
    reference_date = pd.Timestamp('1900-01-01')
    time_hours = np.array([(pd.Timestamp(t) - reference_date).total_seconds() / 3600
                          for t in ds.valid_time.values], dtype=np.int32)

    # Create new dataset with desired structure
    new_ds = xr.Dataset(
        coords={
            'time': ('time', time_hours),
            'longitude': ('longitude', ds.longitude.values.astype(np.float32)),
            'latitude': ('latitude', ds.latitude.values.astype(np.float32))
        }
    )

    # Add coordinate attributes
    new_ds.time.attrs = {
        'standard_name': 'time',
        'long_name': 'time',
        'units': 'hours since 1900-01-01 00:00:00.0',
        'calendar': 'standard',
        'axis': 'T'
    }

    new_ds.longitude.attrs = {
        'standard_name': 'longitude',
        'long_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X'
    }

    new_ds.latitude.attrs = {
        'standard_name': 'latitude',
        'long_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y'
    }

    # Function to convert float32 data to scaled short
    def convert_to_scaled_short(data, name):
        data_min = float(data.min())
        data_max = float(data.max())

        # Calculate optimal scale_factor and add_offset
        scale_factor = (data_max - data_min) / 65534  # Leave room for fill value
        add_offset = (data_max + data_min) / 2

        # Scale the data
        scaled_data = ((data - add_offset) / scale_factor)

        # Handle NaN values using numpy masked array
        mask = np.isnan(data)
        fill_value = -32767
        scaled_data = np.where(mask, fill_value, scaled_data.astype(np.short))

        return scaled_data, scale_factor, add_offset

    # Process each variable
    variables = {
        'u10': ('10 metre U wind component', 'm s**-1'),
        'v10': ('10 metre V wind component', 'm s**-1'),
        'msl': ('Mean sea level pressure', 'Pa')
    }

    for var_name, (long_name, units) in variables.items():
        print(f"Processing variable: {var_name}")
        data = ds[var_name].values
        scaled_data, scale_factor, add_offset = convert_to_scaled_short(data, var_name)

        new_ds[var_name] = (('time', 'latitude', 'longitude'), scaled_data)

        attrs = {
            'long_name': long_name,
            'units': units,
            'scale_factor': scale_factor,
            'add_offset': add_offset,
            '_FillValue': -32767,
            'missing_value': -32767
        }

        if var_name == 'msl':
            attrs['standard_name'] = 'air_pressure_at_mean_sea_level'

        new_ds[var_name].attrs = attrs

    # Add global attributes
    new_ds.attrs = {
        'CDI': 'Climate Data Interface version 1.9.10 (https://mpimet.mpg.de/cdi)',
        'Conventions': 'CF-1.6',
        'history': f'{datetime.now().strftime("%a %b %d %H:%M:%S %Y")}: ERA5 data processed to match specified format',
        'CDO': 'Climate Data Operators version 1.9.10 (https://mpimet.mpg.de/cdo)'
    }

    # Save to netCDF file with correct encoding
    encoding = {
        'time': {
            'dtype': 'int32',
            '_FillValue': None,
            'zlib': True,
            'complevel': 1
        },
        'longitude': {
            'dtype': 'float32',
            '_FillValue': None,
            'zlib': True,
            'complevel': 1
        },
        'latitude': {
            'dtype': 'float32',
            '_FillValue': None,
            'zlib': True,
            'complevel': 1
        },
        'u10': {
            'dtype': 'int16',
            'zlib': True,
            'complevel': 1
        },
        'v10': {
            'dtype': 'int16',
            'zlib': True,
            'complevel': 1
        },
        'msl': {
            'dtype': 'int16',
            'zlib': True,
            'complevel': 1
        }
    }

    new_ds.to_netcdf(output_file,
                     format='NETCDF4_CLASSIC',
                     unlimited_dims=['time'],
                     encoding=encoding)

    print(f"Processed file saved as: {output_file}")
    return new_ds

# Run the processing
input_file = 'era5_data_19941012_19941014.nc'
output_file = 'era5_data_19941012_19941014_rot_fix.nc'
processed_ds = process_era5_data(input_file, output_file)
