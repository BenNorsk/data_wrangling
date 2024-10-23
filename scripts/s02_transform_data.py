import pandas as pd
from typing import Union

# Read the data
def add_children_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column to the DataFrame indicating if the person is a child
    Args:
        df: pd.DataFrame, the DataFrame with the data
    Returns:
        pd.DataFrame
    """
    # If the age is less than 18, the person is a child
    df['child'] = df['age'] < 18
    return df

def convert_income_nans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert NaN values in the income column to 0
    Args:
        df: pd.DataFrame, the DataFrame with the data
    Returns:
        pd.DataFrame
    """
    df['income'] = df['income'].fillna(0)
    return df

def add_main_earner(df: pd.DataFrame) -> pd.DataFrame:
    """
    Indicate the main earner in the household
    Args:
        df: pd.DataFrame, the DataFrame with the data
    Returns:
        pd.DataFrame
    """
    # Group by the household
    households = df.groupby('household_id')
    # Create a new empty DataFrame
    new_df = pd.DataFrame()
    
    # Iterate over the groups
    for household_id, household in households:
        # Sort the household by income (highest income last)
        household = household.sort_values('income')
        # Indicate the main earner
        household['main_earner'] = False
        household.loc[household.index[-1], 'main_earner'] = True  # Last person is the main earner
        # Append the household to the new DataFrame
        new_df = pd.concat([new_df, household])
    
    return new_df


def aggregate_household_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate the data at the household level
    Args:
        data: pd.DataFrame, the DataFrame with the data
    Returns:
        pd.DataFrame
    """
    # Group by  the household
    households = data.groupby('household_id')
    # Create a new empty DataFrame
    df = pd.DataFrame()
    # Iterate over the groups
    for household_id, household in households:
        # Initialize a dictionary to hold the household summary data
        household_summary = {}
        # Add the household-level metrics to the dictionary
        household_summary["household_id"] = household_id
        household_summary["size_hh"] = len(household)
        household_summary["mean_age"] = round(household["age"].mean(), 1) # Rounding to 1 decimal
        household_summary["min_age"] = household["age"].min()
        household_summary["max_age"] = household["age"].max()
        household_summary["nr_children"] = household["child"].sum()
        household_summary["nr_female"] = household["female"].sum()
        household_summary["mean_income"] = round(household["income"].mean(), 1) # Rounding to 1 decimal
        household_summary["total_income"] = household["income"].sum()
        
        # Find the main earner
        main_earner = household[household["main_earner"] == True]
        
        # Check if the main earner is female
        if not main_earner.empty and main_earner["female"].values[0]:
            household_summary["main_earner_female"] = "yes"
        else:
            household_summary["main_earner_female"] = "no"
        
        # Convert the household summary dictionary to a DataFrame
        household_df = pd.DataFrame([household_summary])

        # Use pd.concat to append the new row
        df = pd.concat([df, household_df], ignore_index=True)
    
    return df


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    # Add the children column
    data = add_children_column(data)
    # Convert NaN values in the income column to 0
    data = convert_income_nans(data)
    # Indicate the main earner
    data = add_main_earner(data)
    # Aggregate the data at the household level
    data = aggregate_household_data(data)
    return data
