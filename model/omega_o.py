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
    omega_angle = abs(np.arctan(nn_y / nn_x))
    return np.degrees(omega_angle)

if __name__ == '__main__':
    print(omega_angle(12, 2))
