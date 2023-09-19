def beam_radiation(Gon, tau_b):
    """
    Calculate beam radiation in the direction of the sun.

    Parameters:
    - Gon (float): Direct normal radiation [W/m2].
    - tau_b (float): Sky transmissivity [-].

    Returns:
    - beam_radiation (float): Beam radiation in the direction of the sun [W/m2].
    """
    beam_radiation = Gon * tau_b  # Beam radiation in the direction of the sun [W/m2] (Duffie & Beckam, 2020)

    return beam_radiation
