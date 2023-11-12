import pandas as pd
import numpy as np


def generate_random_string_column(num_rows):
    """
    Generates a list of random string values.

    Args:
        num_rows (int): The number of rows (strings) to generate.

    Returns:
        list: A list of randomly generated strings.
    """
    return [''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 5)) for _ in range(num_rows)]


def generate_data(num_rows=100):
    """
    Generates a mock DataFrame with specified structure.

    Args:
        num_rows (int, optional): The number of rows to generate. Default is 100.

    Returns:
        pd.DataFrame: A DataFrame with generated data.
    """
    """Generate a test dataset that imitates the structure of big_table_new."""

    try:
        data = {
            'col_string1': generate_random_string_column(num_rows),
            'col_string2': generate_random_string_column(num_rows),
            'col_date1': pd.date_range(start='2020-01-01', periods=num_rows, freq='D'),
            'col_date2': pd.date_range(start='2021-01-01', periods=num_rows, freq='D'),
            'col_number1': np.random.randint(0, 100, size=num_rows),
        }

        # Generating more columns for the additional tables
        for i in range(2, 3):  # 2 more tables
            data[f'table{i}_col_string1'] = generate_random_string_column(num_rows)
            data[f'table{i}_col_date1'] = pd.date_range(start='2020-01-01', periods=num_rows, freq='D')
            data[f'table{i}_col_float1'] = np.random.uniform(0, 100, size=num_rows).astype(float)
            for j in range(2, 52):  # Adding up to 50 columns
                data[f'table{i}_col_string{j}'] = generate_random_string_column(num_rows)
                data[f'table{i}_col_date{j}'] = pd.date_range(start='2020-01-01', periods=num_rows, freq='D')
                data[f'table{i}_col_float{j}'] = np.random.uniform(0, 100, size=num_rows).astype(float)

        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise RuntimeError('Error generating data: ' + str(e))
