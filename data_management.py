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

    # Load table method
    def load_table(self, table_name, df):
        self.tables[table_name] = df.copy()

    # Merge tables method
    def merge_tables_on_key(self, table1_name, table2_name, key):
        if table1_name in self.tables and table2_name in self.tables:
            return pd.merge(self.tables[table1_name], self.tables[table2_name], on=key, how='outer')
        else:
            return None

    # Data quality method
    def clean_strings(self, df, columns):
        for col in columns:
            df[col] = df[col].str.strip().str.lower()
        return df

    # Audit logger methods
    def log_action(self, action, user, details):
        self.log = self.log.append({
            "timestamp": pd.Timestamp.now(),
            "action": action,
            "user": user,
            "details": details
        }, ignore_index=True)

    def get_log(self):
        return self.log.copy()

    # Data versioning methods
    def save_version(self, df):
        version_hash = hashlib.md5(df.to_string().encode()).hexdigest()
        self.versions.append({"data": df.copy(), "hash": version_hash, "timestamp": pd.Timestamp.now()})

    def restore_version(self, version_hash):
        for version in self.versions:
            if version["hash"] == version_hash:
                return version["data"].copy()
        return None
