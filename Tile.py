import numpy as np
import Pixel

class Tile:
    def __init__(self, x_dim=8, y_dim=8) -> None:
        """
        Initialize a Tile object with a 2D array of Pixels.

        Args:
            x_dim (int): Number of rows in the Tile grid.
            y_dim (int): Number of columns in the Tile grid.
        """
        self.arr = np.empty((x_dim, y_dim), dtype=object)
        self.x_dim = x_dim
        self.y_dim = y_dim

        # Create Pixel objects and populate the array with them
        for i in range(0, self.x_dim):
            for j in range(0, self.y_dim):
                self.arr[i][j] = Pixel.Pixel(id=(i, j))

    def __str__(self) -> str:
        """
        Generate a string representation of the Tile object.

        Returns:
            str: A formatted string representation of the Tile object.
        """
        for i in range(0, self.x_dim):
            for j in range(0, self.y_dim):
                print("ID: (" + str(i) + ", " + str(j) + "):\n")
                print(self.arr[i][j])

    def replenish(self, arr, t) -> np.ndarray:
        """
        Replenish the charge in each Pixel based on input array and time.

        Args:
            arr (np.ndarray): 2D array containing charge values to replenish with.
            t (float): Current time.
        Returns:
            np.ndarray: A 2D array containing the replenished charge values.
        Raises:
            Exception: If input array dimensions do not match Tile dimensions.
        """
        if self.x_dim != len(arr) or self.y_dim != len(arr[0]):
            raise Exception("Tile and time series data must have the same dimension. Tile has dimension (" + str(self.x_dim) + "," + str(self.y_dim) + ") and data has dimension (" + str(len(arr)) + "," + str(len(arr[0])) + ").")
        
        output = np.zeros((self.x_dim, self.y_dim))
        for i in range(0, self.x_dim):
            for j in range(0, self.y_dim):
                # Call the replenish method of each Pixel with the corresponding charge and time.
                output[i][j] = self.arr[i][j].replenish(charge=arr[i][j], time=float(t))
        
        return output
