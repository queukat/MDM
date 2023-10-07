import pandas as pd

def column_trends_over_time(df, column, time_column):
    """Analyzes trends for a specific column over time."""
    return df.groupby(time_column)[column].mean()

def most_frequently_changed_columns(df):
    """Identifies columns that are most frequently changed."""
    changes = df['column_name'].value_counts()
    return changes
