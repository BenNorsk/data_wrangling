import pytest
import pandas as pd
from scripts import s02_transform_data as s02


def test_add_children_column():
    # Arrange: Create a sample DataFrame
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [17, 20, 15, 18, 0]
    })
    
    # Act: Call the function
    result_df = s02.add_children_column(df)
    
    # Assert: Check that the 'child' column was added correctly
    expected_child_column = [True, False, True, False, True]
    assert (result_df['child'] == expected_child_column).all()


def test_convert_income_nans():
    # Arrange: Create a sample DataFrame with NaN values in the income column
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'income': [10000, None, 30000]
    })
    
    # Act: Call the function
    result_df = s02.convert_income_nans(df)
    
    # Assert: Check that the NaN values have been converted to 0
    expected_income_column = [10000, 0, 30000]
    assert (result_df['income'] == expected_income_column).all()



def test_add_main_earner():
    # Arrange: Create a sample DataFrame with multiple households
    df = pd.DataFrame({
        'household_id': [1, 1, 1, 2, 2],
        'person': ['A', 'B', 'C', 'D', 'E'],
        'income': [5000, 12000, 8000, 6000, 10000]
    })
    
    # Act: Call the add_main_earner function
    result_df = s02.add_main_earner(df)
    print(result_df)
    
    # Assert: Check that the main_earner column is correctly assigned
    expected_main_earner = [False, True, False, False, True]  # Person B in household 1 and person E in household 2
    
    # Check whether person B in household 1 is correctly identified as the main earner
    assert result_df.loc[result_df['person'] == 'B', 'main_earner'].values[0] == True, "Person B should be the main earner in household 1"
    
    # Check whether person E in household 2 is correctly identified as the main earner
    assert result_df.loc[result_df['person'] == 'E', 'main_earner'].values[0] == True, "Person E should be the main earner in household 2"
    
    # Check whether other persons in household 1 are not main earners
    assert result_df.loc[result_df['person'] == 'A', 'main_earner'].values[0] == False, "Person A should not be the main earner in household 1"
    assert result_df.loc[result_df['person'] == 'C', 'main_earner'].values[0] == False, "Person C should not be the main earner in household 1"
    
    # Check whether person D in household 2 is not the main earner
    assert result_df.loc[result_df['person'] == 'D', 'main_earner'].values[0] == False, "Person D should not be the main earner in household 2"



def test_add_main_earner_single_person_household():
    # Arrange: Test case where households have only one person
    df = pd.DataFrame({
        'household_id': [1, 2],
        'person': ['A', 'B'],
        'income': [5000, 12000]
    })
    
    # Act: Call the add_main_earner function
    result_df = s02.add_main_earner(df)
    
    # Assert: In single-person households, the single person should always be the main earner
    assert result_df.loc[result_df['person'] == 'A', 'main_earner'].values[0] == True
    assert result_df.loc[result_df['person'] == 'B', 'main_earner'].values[0] == True


def test_aggregate_household_data():
    # Arrange: Create a sample DataFrame
    data = pd.DataFrame({
        'household_id': [1, 1, 1, 2, 2],
        'person': ['A', 'B', 'C', 'D', 'E'],
        'age': [30, 25, 5, 50, 20],
        'child': [False, False, True, False, True],
        'female': [True, False, True, True, False],
        'income': [10000, 20000, 500, 40000, 10000],
        'main_earner': [False, True, False, True, False]
    })
    
    # Act: Call the function to aggregate household data
    result_df = s02.aggregate_household_data(data)
    
    # Assert: Check that the household-level aggregation is correct
    expected_df = pd.DataFrame({
        'household_id': [1, 2],
        'size_hh': [3, 2],
        'mean_age': [20.0, 35.0],  # Rounded to 1 decimal
        'min_age': [5, 20],
        'max_age': [30, 50],
        'nr_children': [1, 1],
        'nr_female': [2, 1],
        'mean_income': [10166.7, 25000.0],  # Rounded to 1 decimal
        'total_income': [30500, 50000],
        'main_earner_female': ['no', 'yes']  # Based on the 'main_earner' and 'female' columns
    })
    
    # Check if the resulting DataFrame matches the expected DataFrame (ignoring index)
    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


def test_transform_data():
    # Arrange: Create a sample DataFrame with missing values in income and multiple households
    data = pd.DataFrame({
        'household_id': [1, 1, 1, 2, 2],
        'person': ['A', 'B', 'C', 'D', 'E'],
        'age': [30, 25, 5, 50, 20],
        'income': [10000, None, 500, 40000, None],  # None represents NaN values
        'female': [True, False, True, False, False]
    })
    
    # Act: Call the transform_data function
    result_df = s02.transform_data(data)
    
    # Assert: Check that the final transformed DataFrame is correct
    expected_df = pd.DataFrame({
        'household_id': [1, 2],
        'size_hh': [3, 2],
        'mean_age': [20.0, 35.0],  # Rounded to 1 decimal
        'min_age': [5, 20],
        'max_age': [30, 50],
        'nr_children': [1, 0],
        'nr_female': [2, 0],
        'mean_income': [3500.0, 20000.0],  # NaN values replaced with 0 and rounded to 1 decimal
        'total_income': [10500.0, 40000.0],  # Sum of income with NaNs treated as 0
        'main_earner_female': ['yes', 'no']  # Based on main earner gender
    })
    
    # Check if the resulting DataFrame matches the expected DataFrame (ignoring index)
    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))