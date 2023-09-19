import numpy as np

def diffuse_radiant_power(Gdbeta, D_int, L_tubo, F_form):
    """
    Calculate the diffuse radiant power in 1 vacuum tube [W].

    Parameters:
    - Gdbeta (float): Diffuse radiation with sun direction [W/m2].
    - D_int (float): Internal diameter [m].
    - L_tubo (float): Effective length of the tube [m].
    - F_form (float): Shape function for diffuse radiation [-].

    Returns:
    - radiant_power_diffuse (float): Diffuse radiant power in 1 vacuum tube [W].
    """
    radiant_power_diffuse = D_int * L_tubo * np.pi * Gdbeta * F_form  # Radiant power of diffuse in 1 vacuum tube [W]

    return radiant_power_diffuse
