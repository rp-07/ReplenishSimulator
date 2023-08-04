Q-Pix Data Processing, Simulation, and Visualization Project

Overview
This project demonstrates a Python-based data processing and visualization workflow using the xarray library. The project focuses on loading data representing changes in charge on a q-pix array, creating 3D structures, applying the data to simulated pixel arrays, and visualizing results.

Project Structure
Pixel.py: Defines the Pixel class responsible for simulating electron charge behavior and replenishment.
Tile.py: Implements the Tile class, which represents a 2D array of Pixel objects for data manipulation.
Input.py: Contains functions to load data from CSV files and convert them into 3D xarray structures.
Environment.py: Provides functions for simulating different environmental effects on the data.
Output.py: Defines the Output class for visualizing the 3D xarray data using animations and plots.
save_xarray_to_hdf5.py: Converts the xarray data into an HDF5 file and saves it.

Key Components and Behavior

Data Loading and 3D Xarray Creation
CSV Data Loading (Input.py): Use file_to_2d() to load data from a CSV file into a 2D NumPy array.

Creating 3D Xarray (Input.py): Utilize three_d_array() to convert a 2D array into a 3D xarray structure with time, x, and y dimensions.

Data Manipulation and Visualization
Pixel Behavior (Pixel.py, Tile.py): The Pixel class simulates electron charge dynamics, replenishment, and environmental effects. The Tile class represents a 2D array of Pixel objects.

Visualization (Output.py): The Output class offers methods to visualize the 3D xarray data:

time_lapse(): Animates the 3D xarray over time using 2D plots.
time_lapse_histogram(): Creates an animated 3D surface plot of data.
plot_coordinates_over_time(): Produces a 3D scatter plot highlighting non-zero values over time.
HDF5 Conversion
HDF5 Conversion (save_xarray_to_hdf5.py): Converts the 3D xarray data into an HDF5 file and saves it in the "Downloads" folder.

How to Run
Requirements:

Python 3.x
Required libraries: numpy, xarray, matplotlib, h5netcdf (for HDF5 conversion)

Steps:

Follow the instructions provided in each script's comments to understand its purpose and usage.
Modify parameters and settings as needed for your specific use case.
Execute the simulation using main.py

Output:

Depending on the script, visualizations will be displayed or saved.
The generated HDF5 file will be saved in your "Downloads" folder.

Note
This project serves as a learning resource and a starting point for data processing and visualization using xarray. Feel free to modify, extend, or integrate it into your own projects.
For questions or comments, contact rpanday@seas.upenn.edu