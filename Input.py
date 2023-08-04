import numpy as np
import xarray as xr
import csv

def file_to_2d(path):
    """
    Convert a CSV file to a NumPy 2D array.

    Args:
        path (str): Path to the CSV file.

    Returns:
        np.ndarray: A NumPy 2D array containing the data from the CSV file.
    """
    file_path = path

    # Initialize an empty list to store the data rows
    data_rows = []

    # Read the CSV file and skip the header row
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # Skip the header row
        for row in csvreader:
            data_rows.append(row)

    # Convert the data_rows list to a NumPy 2D array
    np_array = np.array(data_rows, dtype=float)

    return np_array


def three_d_array(arr, envir) -> xr.DataArray:
    """
    Convert a 2D NumPy array to a 3D xarray.

    Args:
        arr (np.ndarray): 2D NumPy array containing coordinate data.
        envir (callable): Function to apply an environment factor to the data.

    Returns:
        xr.DataArray: A 3D xarray containing the data in a 8x8 grid over time.
    """
    # Assuming your 2D NumPy array is named 'data'
    data = arr

    # Extract the time stamps from the first column of the data
    time_stamps = data[:, 0]

    # Initialize an empty list to store the 8x8 grids
    points_grids = []

    # Loop through each row to create the 8x8 grid for each timestamp
    for row in data:
        # Apply environment factor
        row[1:] + envir()

        # Extract the coordinate data (remaining 64 columns) for the current timestamp
        points_data = row[1:].reshape(8, 8).transpose()

        # Append the current grid to the list of grids
        points_grids.append(points_data)

    # Convert the list of grids into a 3D NumPy array
    points_grids = np.array(points_grids)

    # Create the x, y coordinates for the 8x8 grid
    x_coords = np.arange(8)
    y_coords = np.arange(8)

    # Create the xarray with the given dimensions and data
    xarray_3d = xr.DataArray(points_grids, dims=('time', 'x', 'y'), coords={'time': time_stamps, 'x': x_coords, 'y': y_coords})

    return xarray_3d