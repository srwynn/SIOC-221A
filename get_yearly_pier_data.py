def get_yearly_pier_data(year_start, year_end, date_start=None, date_end=None):
    """
    Return temperature, pressure, and time data for the specified year range.

    Parameters:
    year_start (int): Start year for data retrieval.
    year_end (int): End year for data retrieval.
    date_start (datetime): Start date for data retrieval (default: None, uses minimum date in dataset).
    date_end (datetime): End date for data retrieval (default: None, uses maximum date in dataset).

    Returns:
    dict: Dictionary containing time, temperature, pressure, and readme information.
    """

    # check for valid year range
    if year_end < year_start:
        raise ValueError("Invalid year range. 'year_end' should be greater than or equal to 'year_start'.")

    # name the file path and create space to input the wanted year ({})
    file_paths = ['http://sccoos.org/thredds/dodsC/autoss/scripps_pier-{}.nc'.format(year) for year in range(year_start, year_end + 1)]

    # create arrays to store the data
    all_time, all_temperature, all_pressure = [], [], []

    # loop through each file and get data
    for file_path in file_paths:
        with Dataset(file_path, 'r') as dataset:
            time = dataset.variables['time'][:]
            temperature = dataset.variables['temperature'][:]
            pressure = dataset.variables['pressure'][:]

        # change time data to datenum 
        date0 = datetime(1970, 1, 1)
        dnum = np.array(time) / 3600 / 24  + date0.toordinal()

        # now after specific year(s) choose the data based on date range
        if date_start is None:
            date_start = min(dnum)
        if date_end is None:
            date_end = max(dnum)

        i1 = np.where((dnum > date_start) & (dnum < date_end))[0]

        # store/formate data for this year
        all_time.append(dnum[i1])
        all_temperature.append(temperature[i1])
        all_pressure.append(pressure[i1])

    # Merge data from all years
    pier = {
        'dnum': np.concatenate(all_time),
        'temperature': np.concatenate(all_temperature),
        'pressure': np.concatenate(all_pressure),
        'readme': 'Pier data for years {} to {}, function get_yearly_pier_data'.format(year_start, year_end)
    }

    return pier