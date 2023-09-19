import numpy as np

def direct_radiant_power(Gbn, D_int, L_tubo, ang_theta, F_ac):
    """
    Calculate the direct radiant power in 1 vacuum tube [W].

    Parameters:
    - Gbn (float): Beam radiation in the direction of the sun [W/m2].
    - D_int (float): Internal diameter [m].
    - L_tubo (float): Effective length of the tube [m].
    - ang_theta (float): Angle of incidence [deg].
    - F_ac (float): Adeptance function [-].

    Returns:
    - radiant_power_direct (float): Direct radiant power in 1 vacuum tube [W].
    """
    radiant_power_direct = D_int * L_tubo * Gbn * np.cos(np.deg2rad(ang_theta)) * F_ac  # Radiant power of beam in 1 vacuum tube [W]

    return radiant_power_direct
