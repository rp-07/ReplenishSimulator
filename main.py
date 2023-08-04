import Input
import Tile
import numpy as np
import Environment
import Output

# Path to the CSV file containing data
file = 'Test.csv'

# Clock period in nanoseconds
CLOCK_FREQ = 20

# Convert CSV file to a 2D NumPy array
arr = Input.file_to_2d(file)

# Convert 2D array to a 3D xarray with Gaussian noise
arr_3d = Input.three_d_array(arr, Environment.make_gaussian_noise)

# Extract the 'time' dimension from the 3D array and convert it into an numpy array
temp = np.array(arr_3d['time'])

# Initialize an Output object to store the results
output = Output.Output(temp[::CLOCK_FREQ])

def iterate(tile, arr, output):
    """
    Iterate over time and update the 'tile' object and 'output' (executing replenishes)

    Parameters:
        tile (Tile): The Tile object representing a grid of pixels.
        arr (xarray): The 3D xarray containing data over time and coordinates.
        output (Output): The Output object to store simulation results.
    """
    # Get the dimensions of the 3D xarray
    time_dim, x_dim, y_dim = arr.dims

    # Loop over each time step
    for t in range(len(arr[time_dim])):
        # Replenish the 'tile' with data for the current time step and coordinates
        status = tile.replenish(arr[t], arr[time_dim][t])

        # Store the status for every 'CLOCK_FREQ' time step in 'output' (ie only store data at every clock tick - and therefore replenish)
        if t % CLOCK_FREQ == 0:
            output.set_frame(t=int(t/CLOCK_FREQ), arr=status)

# Create a Tile object representing a grid of pixels
tile = Tile.Tile()

# Call the 'iterate' function to simulate and update the 'tile' and 'output'
iterate(tile, arr_3d, output)

# # Plot the coordinates over time using 'output' with a threshold value
# output.plot_coordinates_over_time(1.2e-17)

# # Plot a time lapse of the tile
# output.time_lapse()

# # Plot a time lapse of the tile but as a histogram
# output.time_lapse_histogram()

output_file_path = output.save_xarray_to_hdf5('output_data.h5')
print(f"Xarray saved to: {output_file_path}")