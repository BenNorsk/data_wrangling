import pytest
import pandas as pd
from scripts import s03_generate_random_data as s03  

def test_generate_random_data():
    # Act: Generate random data
    df = s03.generate_random_data()

    # Assert: Check that the result is a DataFrame
    assert isinstance(df, pd.DataFrame), "The output should be a pandas DataFrame."

    # Assert: Check that the DataFrame has the correct columns
    expected_columns = ["household_id", "person", "age", "income", "female"]
    assert list(df.columns) == expected_columns, f"DataFrame columns should be {expected_columns}"

    # Assert: Check that household_id, person, and age are not null
    assert df['household_id'].notnull().all(), "household_id should not contain null values."
    assert df['person'].notnull().all(), "person should not contain null values."
    assert df['age'].notnull().all(), "age should not contain null values."

    # Assert: Check the values in the 'age' column are within the expected range
    assert df['age'].between(1, 90).all(), "All ages should be between 1 and 90."

    # Assert: Check that 'female' is a boolean column
    assert df['female'].dtype == bool, "The 'female' column should contain boolean values."

    # Assert: Check that some income values can be None, but the column should exist and contain mostly float
    assert df['income'].dtype in [float, object], "The 'income' column should contain floats or None."

    # Assert: Check that at least one row is generated
    assert len(df) > 0, "The DataFrame should contain at least one row."
