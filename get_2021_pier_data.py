def get_2021_pier_data(date_start=None, date_end=None):
    """
    Return temperature, pressure, and time data from the 2020 pier record.

    Parameters:
    date_start (datetime): Start date for data retrieval (default: None, uses minimum date in dataset).
    date_end (datetime): End date for data retrieval (default: None, uses maximum date in dataset).

    Returns:
    dict: Dictionary containing time, temperature, pressure, and readme information.
    """

    file_path = file = 'http://sccoos.org/thredds/dodsC/autoss/scripps_pier-2021.nc'

    with nc.Dataset(file_path, 'r') as dataset:
        time = dataset.variables['time'][:]
        temperature = dataset.variables['temperature'][:]
        pressure = dataset.variables['pressure'][:]

    date0 = datetime(1970, 1, 1)
    dnum = np.array(time) / 3600 / 24 + date0.toordinal()

    if date_start is None:
        date_start = min(dnum)   #refers to the number of input vairbles if date start and end is not included then take the entire dataset
    if date_end is None:
        date_end = max(dnum)

    i1 = np.where((dnum > date_start) & (dnum < date_end))[0]

    pier = {
        'dnum': dnum[i1],
        'temperature': temperature[i1],
        'pressure': pressure[i1],
        'readme': '2021 Pier data, SIO221a, function Get2021PierData.py'
    }

    return pier