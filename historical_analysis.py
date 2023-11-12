import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def column_trends_over_time(df, column, time_column):
    """
    Analyzes trends for a specific column over time.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column (str): The column to analyze trends for.
        time_column (str): The column representing time.

    Returns:
        pd.Series: A series representing the mean value of the column over time.
    """
    """Analyzes trends for a specific column over time."""
    logging.info(f"Analyzing trends over time for column: {column}")
    return df.groupby(time_column)[column].mean()

def most_frequently_changed_columns(df):
    """
    Identifies columns that are most frequently changed.

    Args:
        df (pd.DataFrame): The DataFrame containing change history.

    Returns:
        pd.Series: A series with the counts of changes for each column.
    """
    """Identifies columns that are most frequently changed."""
    logging.info("Identifying most frequently changed columns.")
    changes = df['column_name'].value_counts()
    return changes
