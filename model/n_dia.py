import datetime

def day_number(dia, mes):
    """
    Calculate the n-th day of the year.

    Parameters:
    - dia (int): The chosen day (1-31).
    - mes (int): The chosen month (1-12).

    Returns:
    - day_number (int): The n-th day of the year.
    """
    date = datetime.date(1, mes, dia)
    end_of_year = datetime.date(1, 12, 31)

    day_number = (date - end_of_year).days  # The n-th day of the year for a non-leap year

    return day_number
