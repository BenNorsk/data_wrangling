from scripts.s01_read_data import read_data
from scripts.s02_transform_data import transform_data
import pandas as pd


def main():
    """
    Main function to read and transform the data. Manages all other functions.
    """
    data = read_data('data/household_data.csv')
    print("Data read successfully")
    aggregate_data = transform_data(data)
    print("Data transformed successfully. See the result below:")
    print(aggregate_data)
    # Save the data
    aggregate_data.to_csv('data/aggregate_data.csv', index=False)
    return



if __name__ == '__main__':
    main()