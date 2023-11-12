import hashlib
import logging
import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)

class UnifiedDataManager:
    def __init__(self):
        self.tables = {}
        self.log = pd.DataFrame(columns=["timestamp", "action", "user", "details"])
        self.versions = []
        self.main_data = pd.DataFrame()
        self.history_data = pd.DataFrame(columns=['column_name', 'old_value', 'new_value', 'timestamp'])

    def load_table(self, table_name, df):
        """
        Load a table into the manager.

        Args:
            table_name (str): The name of the table to load.
            df (pd.DataFrame): The dataframe containing the table's data.
        """
        self.tables[table_name] = df.copy()

    def merge_tables_on_key(self, table1_name, table2_name, key):
        """
        Merge two tables on a common key.

        Args:
            table1_name (str): The name of the first table.
            table2_name (str): The name of the second table.
            key (str): The key to merge on.

        Returns:
            pd.DataFrame: The merged dataframe, or None if either table name is not found.
        """
        if table1_name in self.tables and table2_name in self.tables:
            return pd.merge(self.tables[table1_name], self.tables[table2_name], on=key, how='outer')
        else:
            return None

    def clean_strings(self, df, columns):
        """
        Clean and standardize string columns in a dataframe.

        Args:
            df (pd.DataFrame): The dataframe to clean.
            columns (list): The list of columns to standardize.

        Returns:
            pd.DataFrame: The dataframe with cleaned and standardized string columns.
        """
        for col in columns:
            df[col] = df[col].str.strip().str.lower()
        return df

    def log_action(self, action, user, details):
        """
        Log an action performed by a user.

        Args:
            action (str): The action performed.
            user (str): The user who performed the action.
            details (str): Additional details about the action.
        """
        self.log = self.log.append({
            "timestamp": pd.Timestamp.now(),
            "action": action,
            "user": user,
            "details": details
        }, ignore_index=True)

    def get_log(self):
        """
        Get a copy of the action log.

        Returns:
            pd.DataFrame: A copy of the log dataframe.
        """
        return self.log.copy()

    def save_version(self, df):
        """
        Save a version of the dataframe.

        Args:
            df (pd.DataFrame): The dataframe to save.
        """
        version_hash = hashlib.md5(df.to_string().encode()).hexdigest()
        self.versions.append({"data": df.copy(), "hash": version_hash, "timestamp": pd.Timestamp.now()})

    def restore_version(self, version_hash):
        """
        Restore a version of the dataframe.

        Args:
            version_hash (str): The hash of the version to restore.

        Returns:
            pd.DataFrame: The restored dataframe, or None if not found.
        """
        for version in self.versions:
            if version["hash"] == version_hash:
                return version["data"].copy()
        return None
