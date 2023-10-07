
class TableDependencyAnalyzer:
    def __init__(self, tables):
        self.tables = tables

    def determine_column_dependencies(self):
        dependencies = {}
        all_columns = {table_name: set(df.columns) for table_name, df in self.tables.items()}
        for table_name, columns in all_columns.items():
            for other_table, other_columns in all_columns.items():
                if table_name != other_table:
                    common_columns = columns.intersection(other_columns)
                    if common_columns:
                        if table_name not in dependencies:
                            dependencies[table_name] = {}
                        dependencies[table_name][other_table] = list(common_columns)
        return dependencies

    def analyze_data_dependencies(self):
        data_dependencies = {}
        for table_name, df in self.tables.items():
            for other_table, other_df in self.tables.items():
                if table_name != other_table:
                    common_columns = set(df.columns).intersection(set(other_df.columns))
                    for column in common_columns:
                        if df[column].equals(other_df[column]):
                            if table_name not in data_dependencies:
                                data_dependencies[table_name] = {}
                            if other_table not in data_dependencies[table_name]:
                                data_dependencies[table_name][other_table] = []
                            data_dependencies[table_name][other_table].append(column)
        return data_dependencies