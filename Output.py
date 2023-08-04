import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from decimal import Decimal
import os
import h5netcdf

class Output:
    
    def __init__(self, time):
        """
        Initialize the Output class.

        Parameters:
        - time (array-like): Array containing time stamps.

        This constructor initializes the Output class with time stamps and creates a 3D xarray to store data.
        """
        x_coords = np.zeros(8)  # Initialize 'x' coordinates with 0
        y_coords = np.zeros(8)  # Initialize 'y' coordinates with 0

        # Create an empty 3D array filled with NaN values
        data = np.empty((len(time), len(x_coords), len(y_coords)), dtype = float)
        data[:] = np.nan

        # Create the 3D xarray with the given dimensions and coordinates
        xarray_3d = xr.DataArray(data, dims=('time', 'x', 'y'), coords={'time': time, 'x': x_coords, 'y': y_coords})

        self.arr = xarray_3d

    def set_frame(self, t, arr):
        """
        Set a frame of the 3D xarray with the given array data.

        Parameters:
        - t (int): Frame index.
        - arr (array-like): Data to be stored in the frame.

        This method sets the data for a specific frame in the 3D xarray.
        """
        self.arr[t] = arr
    
    def time_lapse(self):
        """
        Create an animation to visualize the 3D xarray over time using imshow.

        This method generates an animation that shows the 3D xarray's data changing over time using imshow.
        """
        # Create a figure and axes for the animation
        fig, ax = plt.subplots()

        # Create an initial empty plot
        img = ax.imshow(np.zeros_like(self.arr[0]), cmap='viridis', origin='lower', extent=[0, 1, 0, 1], vmin = 0, vmax = 1e-11)

        # Create a color bar for the plot
        cbar = plt.colorbar(img, fraction=0.046, pad=0.04)
        cbar.set_label('Instantaneous Current')
        
        def update(frame):
            plt.cla()  # Clear the current plot

            # Extract the data for the current time step
            grid_data = self.arr[frame].values

            # Plot the 2D chess grid for the current time step
            img = plt.imshow(grid_data, cmap='viridis', origin='lower', vmin = 0, vmax = 1e-11)
            img.autoscale()

            # Customize the plot as needed
            plt.title(f'Tile Time Step: {frame}')
            plt.xlabel('X')
            plt.ylabel('Y')
        
        # Create the animation
        ani = FuncAnimation(fig, update, frames=np.arange(len(self.arr['time'])), interval=100)
        plt.show()

    def time_lapse_histogram(self):
        """
        Create an animation to visualize the 3D xarray data over time using a 3D surface plot.

        This method generates an animation that shows the 3D xarray's data changing over time using a 3D surface plot.
        """
        # Create a figure and axes for the animation
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plot = None
        # Function to update the 3D plot for each animation frame
        def update(frame):
            plt.cla()  # Clear the current plot

            # Extract the data for the current time step
            data_at_time = self.arr[frame].values

            # Create a meshgrid for the x and y coordinates
            X, Y = np.meshgrid(np.arange(len(self.arr['x'])), np.arange(len(self.arr['y'])))

            # Plot the 3D surface for the current time step
            plot = ax.plot_surface(X, Y, data_at_time, cmap='viridis', rstride=1, cstride=1)

            # Customize the plot as needed
            ax.set_title(f'Time step: {frame}')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Instantaneous Current')
            ax.set_zlim(0, 1e-14)

        # Create the animation
        ani = FuncAnimation(fig, update, frames=np.arange(len(self.arr['time'])), interval=100) #this should be the last line before the plt.show()
        plt.show()

    def plot_coordinates_over_time(self, threshold):
        """
        Create a scatter plot of coordinates over time.

        Parameters:
        - threshold (float): Threshold value for non-zero data points.

        This method generates a scatter plot showing the coordinates changing over time for above threshold data points.
        """
        # Create a 3D scatter plot with time as one axis, and x and y as the other two axes
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Extract the meshgrid for time, x, and y
        T, X, Y = np.meshgrid(self.arr['time'], np.arange(len(self.arr['x'])), np.arange(len(self.arr['y'])), indexing='ij')

        # Reshape the data to 1D arrays
        T_1d = T.ravel()
        X_1d = X.ravel()
        Y_1d = Y.ravel()
        data_1d = self.arr.values.ravel()

        # Filter data points above the threshold
        nonzero_mask = np.where(data_1d > threshold)[0]
        T_1d_nonzero = T_1d[nonzero_mask]
        X_1d_nonzero = X_1d[nonzero_mask]
        Y_1d_nonzero = Y_1d[nonzero_mask]
        data_1d_nonzero = data_1d[nonzero_mask]

        # Plot the 3D scatter plot for above threshold data points
        sc_nonzero = ax.scatter(T_1d_nonzero, X_1d_nonzero, Y_1d_nonzero, c=data_1d_nonzero, cmap='viridis', marker='o')

        # Customize the plot as needed
        ax.set_xlabel('Time')
        ax.set_ylabel('X')
        ax.set_zlabel('Y')
        ax.set_title('X and Y over Time (Scatter Plot)')
        plt.colorbar(sc_nonzero)

        plt.show()

    def save_xarray_to_hdf5(self, filename):
        """
        Save an xarray to an HDF5 file and store it in the "Downloads" folder.

        Args:
            filename (str): Name of the HDF5 file to be created.

        Returns:
            str: Full path to the saved HDF5 file.
        """
        # Get the full path to the "Downloads" folder
        downloads_folder = os.path.expanduser('~/Downloads')

        # Combine the downloads folder path with the provided filename
        file_path = os.path.join(downloads_folder, filename)

        # Save the xarray to the HDF5 file
        self.arr.to_netcdf(file_path, engine='h5netcdf')

        return file_path