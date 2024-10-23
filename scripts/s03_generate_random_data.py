import pandas as pd
import numpy as np
import random


def generate_random_data() -> pd.DataFrame:
    # Create number of households
    num_households = random.randint(2, 10)
    # Generate random household ids
    household_ids = [random.randint(1, 1000) for _ in range(num_households)]
    
    data = []
    
    for household_id in household_ids:
        # Random number of people per household
        num_persons = random.randint(1, 4)
        
        for person in range(1, num_persons + 1):
            # Generate random age (range 0 to 100)
            age = random.randint(1, 90)
            # Generate random income with some people having None (representing missing income data)
            income = round(random.uniform(1000, 120000), 2) if random.random() > 0.2 else None
            # Randomly assign female gender
            female = random.choice([True, False])
            # Append to the data list
            data.append([household_id, person, age, income, female])
    
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=["household_id", "person", "age", "income", "female"])
    
    return df