import pandas as pd


def check_missing_values(df):
    """Проверяет пропущенные значения в df и возвращает столбцы с пропущенными значениями и их количество."""
    missing = df.isnull().sum()
    return missing[missing > 0]


def check_duplicates(df):
    """Проверяет на наличие дубликатов строк в df."""
    return df[df.duplicated()]


import numpy as np


def check_anomalies(df, columns=None, method="iqr", date_range=None, rare_threshold=0.01, regex_patterns=None):
    """
    Проверяет аномалии в столбцах.
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
            # Проверка на редкие категории
            value_counts = df[column].value_counts(normalize=True)
            rare_categories = value_counts[value_counts < rare_threshold].index
            column_anomalies = df[df[column].isin(rare_categories)]

            # Проверка на соответствие регулярному выражению
            if column in regex_patterns:
                pattern = regex_patterns[column]
                column_anomalies = pd.concat([column_anomalies, df[~df[column].str.match(pattern)]])

        else:
            continue

        anomalies = pd.concat([anomalies, column_anomalies])

    return anomalies.drop_duplicates()


def detect_outliers_iqr(df, column):
    """Использует IQR для обнаружения выбросов в числовом столбце."""
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
    """Проверяет, являются ли все значения в столбце уникальными."""
    return df[column].nunique() == len(df)

def check_allowed_values(df, column, allowed_values):
    """Проверяет, что все значения в столбце находятся в списке допустимых значений."""
    return df[column].isin(allowed_values).all()

def check_date_range(df, column, start_date=None, end_date=None):
    """Проверяет, что все даты в столбце находятся в допустимом диапазоне."""
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
    """Проверяет соответствие всех значений в столбце регулярному выражению."""
    return df[column].str.match(pattern).all()

def check_column_dependency(df, column1, value1, column2, value2):
    """Проверяет, что если столбец column1 имеет значение value1, то столбец column2 имеет значение value2."""
    subset = df[df[column1] == value1]
    return subset[column2].eq(value2).all()

def check_normalization(df, column):
    """Проверяет на нормализацию, удостоверяясь, что данные в столбце не имеют дублирующихся значений из-за пробелов, разных регистров и т.д."""
    normalized_values = df[column].str.strip().str.lower()
    return normalized_values.nunique() == df[column].nunique()