import pandas as pd


def check_missing_values(df):
    """
    Checks for missing values in the DataFrame and returns columns with missing values and their count.

    Args:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        pd.Series: A series with the count of missing values per column.
    """
    missing = df.isnull().sum()
    return missing[missing > 0]


def check_duplicates(df):
    """
    Checks for duplicate rows in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        pd.DataFrame: A DataFrame with duplicate rows.
    """
    return df[df.duplicated()]


import numpy as np


def check_anomalies(df, columns=None, method="iqr", date_range=None, rare_threshold=0.01, regex_patterns=None):
    """
    Checks for anomalies in specified columns using different methods.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        columns (list, optional): List of columns to check. Defaults to all columns.
        method (str, optional): The method to use for anomaly detection. Defaults to "iqr" (interquartile range).
        date_range (tuple, optional): The date range for anomaly detection. Defaults to None.
        rare_threshold (float, optional): Threshold for rare value detection. Defaults to 0.01.
        regex_patterns (dict, optional): Regex patterns for anomaly detection. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame with detected anomalies.
    """
    if columns is None:
        columns = df.columns

    anomalies = pd.DataFrame()
    regex_patterns = regex_patterns or {}

    for column in columns:
        if df[column].dtype in ['int64', 'float64']:
            if method == "iqr":
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                column_anomalies = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            else:
                raise ValueError("Unknown method for anomaly detection.")

        elif np.issubdtype(df[column].dtype, np.datetime64):
            if date_range:
                column_anomalies = df[(df[column] < date_range[0]) | (df[column] > date_range[1])]
            else:
                continue

        elif df[column].dtype == 'object':
            value_counts = df[column].value_counts(normalize=True)
            rare_categories = value_counts[value_counts < rare_threshold].index
            column_anomalies = df[df[column].isin(rare_categories)]

            if column in regex_patterns:
                pattern = regex_patterns[column]
                column_anomalies = pd.concat([column_anomalies, df[~df[column].str.match(pattern)]])

        else:
            continue

        anomalies = pd.concat([anomalies, column_anomalies])

    return anomalies.drop_duplicates()


def detect_outliers_iqr(df, column):
    if column not in df:
        raise ValueError(f"Column '{column}' not found in dataframe.")

    if df[column].dtype not in ["float64", "int64"]:
        raise ValueError(f"Column '{column}' is not numeric.")

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]


def check_unique_values(df, column):
    return df[column].nunique() == len(df)


def check_allowed_values(df, column, allowed_values):
    return df[column].isin(allowed_values).all()


def check_date_range(df, column, start_date=None, end_date=None):
    if start_date:
        start_date = pd.Timestamp(start_date)
        if not (df[column] >= start_date).all():
            return False
    if end_date:
        end_date = pd.Timestamp(end_date)
        if not (df[column] <= end_date).all():
            return False
    return True


def check_regex(df, column, pattern):
    return df[column].str.match(pattern).all()


def check_column_dependency(df, column1, value1, column2, value2):
    subset = df[df[column1] == value1]
    return subset[column2].eq(value2).all()


def check_normalization(df, column):
    normalized_values = df[column].str.strip().str.lower()
    return normalized_values.nunique() == df[column].nunique()
