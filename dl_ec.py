import cdsapi

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "mean_sea_level_pressure"
    ],
    "year": ["1994"],
    "month": ["10"],
    "day": ["12"],
    "time": [
        "17:00", "18:00", "19:00",
        "20:00", "21:00", "22:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived"
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
