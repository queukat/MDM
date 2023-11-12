
class DataProfiler:
    """
    A class for profiling data, providing functionalities like missing data analysis, unique value counts, and general data description.
    """
    @staticmethod
    def find_missing_data(df):
        """
        Finds missing data in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.

        Returns:
            pd.Series: A series containing counts of missing values per column.
        """
        return df.isnull().sum()

    @staticmethod
    def count_unique_values(df):
        """
        Counts unique values in each column of the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.

        Returns:
            pd.Series: A series containing counts of unique values per column.
        """
        return df.nunique()

    @staticmethod
    def profile_data(df):
        """
        Provides a general profile of the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to profile.

        Returns:
            pd.DataFrame: A DataFrame containing the general description of the input DataFrame.
        """
        return df.describe(include='all')
