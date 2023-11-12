import vaex
import seaborn as sns
import matplotlib.pyplot as plt

def validate_data(df):
    """
    Validates the DataFrame for null values.

    Args:
        df (vaex.DataFrame): The DataFrame to be validated.

    Raises:
        ValueError: If null values are found in the DataFrame.
    """
    if df.isnull().sum().sum() > 0:
        raise ValueError("Data contains null values. Please clean the data before analysis.")
    return df

def describe_data(df):
    """
    Describes the DataFrame by calculating statistical metrics for each column.

    Args:
        df (vaex.DataFrame): The DataFrame to be described.

    Returns:
        dict: A dictionary containing statistical metrics for each column.
    """
    validate_data(df)
    stats = {}
    for col in df.column_names:
        stats[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'min': df[col].min(),
            'max': df[col].max(),
            'std': df[col].std(),
            'q1': df[col].quantile(0.25),
            'q3': df[col].quantile(0.75),
            'mode': df[col].mode()[0]
        }
    return stats

def plot_distribution(df, column_name):
    """
    Plots the distribution of a specified column in the DataFrame.

    Args:
        df (vaex.DataFrame): The DataFrame containing the data.
        column_name (str): The name of the column to plot.
    """
    validate_data(df)
    df.viz.histogram(column_name, show=True, figsize=(10, 5))

def plot_boxplot(df, column_name):
    """
    Plots a boxplot for a specified column in the DataFrame.

    Args:
        df (vaex.DataFrame): The DataFrame containing the data.
        column_name (str): The name of the column to plot.
    """
    validate_data(df)
    sns.boxplot(x=df[column_name].values)  # Convert vaex series to numpy for visualization
    plt.title(f'Box plot for {column_name}')
    plt.show()

def plot_scatter(df, x_column, y_column):
    validate_data(df)
    df.plot(x_column, y_column, kind='scatter', figsize=(10, 5))

def plot_pie_chart(df, column_name):
    validate_data(df)
    counts = df[column_name].value_counts().tolist()
    labels = df[column_name].unique().tolist()
    plt.pie(counts, labels=labels, autopct='%1.1f%%')
    plt.title(f'Pie chart for {column_name}')
    plt.show()

def plot_column_trends(df, column, time_column):
    validate_data(df)
    df.plot(time_column, column, figsize=(10, 5))

def plot_heatmap(df):
    validate_data(df)
    correlation_matrix = df.corr()
    plt.figure(figsize=(12, 9))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.show()

def plot_pairplots(df, columns):
    validate_data(df)
    df_pandas = df[columns].to_pandas_df()  # Convert selected columns to pandas DataFrame
    sns.pairplot(df_pandas)
    plt.show()
