import numpy as np

def omega_angle(nn_x, nn_y):
    """
    Calculate the OMEGA angle.

    Parameters:
    - nn_x (float): Normal direction to the inclined plane.
    - nn_y (float): Direction from east to south.

    Returns:
    - omega_angle (float): The OMEGA angle [degrees].
    """
    omega_angle = abs(np.arctan(nn_y / nn_x))  # Function that returns the OMEGA angle [degrees]

    return np.degrees(omega_angle)
