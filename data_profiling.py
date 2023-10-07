
class DataProfiler:
    @staticmethod
    def find_missing_data(df):
        return df.isnull().sum()

    @staticmethod
    def count_unique_values(df):
        return df.nunique()

    @staticmethod
    def profile_data(df):
        return df.describe(include='all')
