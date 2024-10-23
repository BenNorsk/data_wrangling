import pandas as pd
from typing import Union

# Read the data
def read_data(file: str) -> pd.DataFrame:
    """
    Read the data from the file
    Args:
        file: str, path to the file
    Returns:
        pd
    """
    return pd.read_csv(file)