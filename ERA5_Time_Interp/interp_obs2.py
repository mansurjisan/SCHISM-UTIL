import xarray as xr
import pandas as pd
import numpy as np
from metpy.units import units
from metpy.calc import wind_components

def read_wind_data(filename):
    """
    Read wind data from file (keeping 30-minute intervals).
    """
    df = pd.read_csv(filename, sep='\s+', names=['date', 'time', 'speed', 'direction'])
    df['speed'] = df['speed'].astype(float)
    df['direction'] = df['direction'].astype(float)
    return df

def calculate_wind_components(speed, direction):
    """
    Calculate U and V components using MetPy.
    """
    speed = speed * units('m/s')
    direction = direction * units('degrees')
    u, v = wind_components(speed, direction)
    return float(u.magnitude), float(v.magnitude)

def interpolate_era5_with_obs_wind(ds, wind_df, n_timesteps=17):
    """
    Interpolate ERA5 data to 30-minute intervals and replace wind components with observed data.

    Parameters:
    -----------
    ds : xarray.Dataset
        Input ERA5 dataset with hourly data
    wind_df : pandas.DataFrame
        DataFrame containing observed wind speed and direction
    n_timesteps : int
        Number of timesteps to process

    Returns:
    --------
    xarray.Dataset
        Dataset with variables interpolated to 30-minute intervals
    """
    print("Processing first {} timesteps...".format(n_timesteps))

    # Limit to specified number of timesteps
    ds = ds.isel(valid_time=slice(0, n_timesteps))

    # Create new time array with 30-min intervals
    time_orig = pd.to_datetime(ds.valid_time.values, unit='s')
    time_new = pd.date_range(start=time_orig[0], end=time_orig[-1], freq='30min')
    time_new_unix = (time_new - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")

    # Calculate number of 30-min intervals
    n_new_times = len(time_new_unix)

    # Initialize new dataset
    ds_new = xr.Dataset(
        coords={
            'valid_time': time_new_unix,
            'latitude': ds.latitude,
            'longitude': ds.longitude
        }
    )

    # First interpolate MSL (pressure) data
    print("Interpolating msl...")
    msl_data = ds['msl'].values
    new_msl = np.zeros((n_new_times,) + msl_data.shape[1:])

    # Interpolate MSL data
    for i in range(len(msl_data)-1):
        idx = i * 2
        new_msl[idx] = msl_data[i]
        new_msl[idx + 1] = (msl_data[i] + msl_data[i + 1]) / 2
    new_msl[-1] = msl_data[-1]

    # Add MSL to new dataset
    ds_new['msl'] = (('valid_time', 'latitude', 'longitude'), new_msl)
    ds_new['msl'].attrs = ds['msl'].attrs

    # Calculate and assign wind components
    print("\nCalculating wind components from observations...")
    u_data = np.zeros((n_new_times,) + ds['u10'].shape[1:])
    v_data = np.zeros((n_new_times,) + ds['v10'].shape[1:])

    print(f"Creating new file with {n_new_times} 30-minute timesteps")
    print(f"Available wind data has {len(wind_df)} entries")

    # For each new timestep
    for t in range(n_new_times):
        wind_idx = t % len(wind_df)
        speed = wind_df['speed'].iloc[wind_idx]
        direction = wind_df['direction'].iloc[wind_idx]

        # Calculate wind components
        u, v = calculate_wind_components(speed, direction)

        # Assign uniform values
        u_data[t,:,:] = u
        v_data[t,:,:] = v

        print(f"Timestep {t+1}/{n_new_times} - Using wind data entry {wind_idx + 1}")
        print(f"Wind data: speed={speed:.2f} m/s, direction={direction:.2f}°")
        print(f"Calculated u={u:.2f} m/s, v={v:.2f} m/s")
        print("-" * 50)

    # Add wind components to new dataset
    ds_new['u10'] = (('valid_time', 'latitude', 'longitude'), u_data)
    ds_new['v10'] = (('valid_time', 'latitude', 'longitude'), v_data)

    # Copy wind variable attributes
    ds_new['u10'].attrs = ds['u10'].attrs
    ds_new['v10'].attrs = ds['v10'].attrs

    # Copy remaining variables
    for var in ds.variables:
        if var not in ['u10', 'v10', 'msl', 'valid_time', 'latitude', 'longitude']:
            ds_new[var] = ds[var]

    # Copy coordinate attributes
    for coord in ['latitude', 'longitude']:
        ds_new[coord].attrs = ds[coord].attrs

    # Set time attributes
    ds_new.valid_time.attrs = {
        'long_name': 'time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01',
        'calendar': 'proleptic_gregorian'
    }

    # Copy global attributes
    ds_new.attrs = ds.attrs

    return ds_new

if __name__ == "__main__":
    print("Reading ERA5 data...")
    # Read ERA5 data
    ds = xr.open_dataset('era5_data_201210_sandy_sv.nc')

    print("Reading wind observations...")
    # Read wind data from file
    wind_df = read_wind_data('spd_dir.txt')

    print("Performing interpolation and wind component calculation...")
    # Perform interpolation and wind component calculation
    ds_30min = interpolate_era5_with_obs_wind(ds, wind_df)

    print("Renaming valid_time to time...")
    # Rename valid_time to time before saving
    ds_30min = ds_30min.rename({'valid_time': 'time'})

    print("Saving interpolated data...")
    # Save interpolated data with proper encoding
    encoding = {
        'time': {  # Changed from valid_time to time
            'dtype': 'int64',
            '_FillValue': None
        },
        'u10': {'dtype': 'float32'},
        'v10': {'dtype': 'float32'},
        'msl': {'dtype': 'float32'}
    }

    ds_30min.to_netcdf('era5_data_30min_obs_wind.nc', encoding=encoding)

    print("Done!")
    print(f"Original times: {len(ds.valid_time)} points")
    print(f"Interpolated times: {len(ds_30min.time)} points")  # Changed to time
