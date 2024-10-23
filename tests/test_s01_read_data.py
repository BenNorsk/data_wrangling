import pytest
import pandas as pd
from unittest import mock
from scripts import s01_read_data as s01

def test_read_data_success():
    # Arrange: Mock the pd.read_csv method
    with mock.patch('pandas.read_csv') as mock_read_csv:
        # Create a mock DataFrame to return
        mock_df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [25, 30]
        })
        mock_read_csv.return_value = mock_df

        # Act: Call the read_data function
        result_df = s01.read_data('fake_file.csv')

        # Assert: Check that the DataFrame returned matches the mock DataFrame
        pd.testing.assert_frame_equal(result_df, mock_df)
        # Check that pd.read_csv was called with the correct file path
        mock_read_csv.assert_called_once_with('fake_file.csv')

def test_read_data_file_not_found():
    # Arrange: Mock the pd.read_csv method to raise a FileNotFoundError
    with mock.patch('pandas.read_csv', side_effect=FileNotFoundError):
        # Act and Assert: Expect a FileNotFoundError when calling read_data
        with pytest.raises(FileNotFoundError):
            s01.read_data('non_existent_file.csv')