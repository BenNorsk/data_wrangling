from scripts.s01_read_data import read_data
from scripts.s02_transform_data import transform_data
from scripts.s03_generate_random_data import generate_random_data
import pandas as pd
import os
import sys


def main():
    """
    Main function to read and transform the data. Manages all other functions.
    """
    # Read the flag from the command line. It can either be a path to the data file or the flag --test
    if ((len(sys.argv) > 3) or (len(sys.argv) < 2) or (sys.argv[1] == "--help") or (sys.argv[1] == "-h")):
        print(
            """
            Usage: program_name [OPTIONS]

            Options:
            --file PATH       Path to the data file.
            --test            Runs the tests of the program.
            --random          Generate random data.
            -h, --help        Show this message and exit.
    """
        )
        print("Please provide either the path to the data file, or the flag --test, or the flag --random to generate random data.")
        return
    
    # Check if the flag is --test
    if sys.argv[1] == "--test":
        # Run the tests
        os.system("pytest")
        return
    
    data = pd.DataFrame()
    name = "random_data"
    # Check if the flag is --random
    if sys.argv[1] == "--random":
        # Generate random data
        data = generate_random_data()
        print("Random data generated successfully.")

    elif sys.argv[1] == "--file":
        try:
            # Read the data
            data = read_data(sys.argv[2])
        except:
            print("File not found. Please provide a valid path to the data file.")
            return
        print("Data read successfully")
        # Get the name of the file
        name = os.path.basename(sys.argv[1]).split(".")[0]
        
    # Transform the data
    aggregate_data = transform_data(data)
    print("Data transformed successfully. See the result below:")
    print(aggregate_data)
    # Save the data
    aggregate_data.to_csv(f'data/aggregate_{name}.csv', index=False)
    return



if __name__ == '__main__':
    main()