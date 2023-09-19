def sunrise(omega_s):
    """
    Calculate the solar time of sunrise.

    Parameters:
    - omega_s (float): Hour angle at sunset in degrees.

    Returns:
    - solar_time_sunrise (float): Solar time of sunrise (in decimal format).
    """
    solar_time_sunrise = 12 - (omega_s / 15)  # Provides the solar time when the sun rises above the horizon.

    return solar_time_sunrise
