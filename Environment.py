import numpy as np

def make_gaussian_noise(sigma=1e-12, noise_vector_size=64):
    """
    Generate a vector of simulated noise with Gaussian distribution and leakage current events.

    Parameters:
    sigma (float): Standard deviation for Gaussian noise.
    noise_vector_size (int): Number of elements in the noise vector.

    Returns:
    numpy.ndarray: An array containing the simulated noise values.
    """
    noise = []
    for _ in range(noise_vector_size):
        # Generate random noise from Gaussian distribution with mean 0 and standard deviation sigma
        electronics = round(np.random.normal(0, sigma))

        # Probability of 100 attocoulombs leakage current (625 electrons per second)
        leakage_probability = 625 / 1e8

        # Determine if there's a leakage current event
        leakage_current = 1 if np.random.uniform() < leakage_probability else 0

        noise.append(electronics + leakage_current)

    return np.array(noise)

def ideal():
    """
    Returns an idealized noise value of 0 in an ideal environment.

    Returns:
    int: Idealized noise value (always 0).
    """
    return 0
