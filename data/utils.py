
import os
import math

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        number = int(round(number))
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def create_folder(folder_name):
    print(f"checking folder {folder_name}")
    if not os.path.exists(folder_name):
        print("folder not dounf, creating now...")
        os.makedirs(folder_name)