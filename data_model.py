import pandas as pd
from tqdm import tqdm
class DataModelV5:
    def __init__(self):
        self.main_data = pd.DataFrame()
        self.history_data = pd.DataFrame(columns=['column_name', 'old_value', 'new_value', 'timestamp'])
        self.previous_schema = None

    def load_data(self, df):
        # Если главные данные пусты или новые данные имеют другие столбцы, просто заменяем данные.
        if self.main_data.empty or not df.columns.equals(self.main_data.columns):
            self.main_data = df.copy()
            return



        # Векторизованное сравнение данных
        differences = (self.main_data != df) & ~df.isna() & ~self.main_data.isna()
        # Проверка схемы
        current_schema = df.dtypes.to_dict()
        if self.previous_schema and self.previous_schema != current_schema:
            print("Warning: Data schema has changed!")
            for col, dtype in current_schema.items():
                if col not in self.previous_schema:
                    print(f"New column detected: {col} with type {dtype}")
                elif self.previous_schema[col] != dtype:
                    print(f"Column {col} type has changed from {self.previous_schema[col]} to {dtype}")
            for col in self.previous_schema:
                if col not in current_schema:
                    print(f"Column {col} has been removed!")
        else:
            print("Data schema check passed successfully!")

        # Создаем прогресс-бар
        total_changes = differences.sum().sum()
        progress_bar = tqdm(total=total_changes, desc="Processing changes")

        for column in df.columns:
            column_changes = df[differences[column]].index.tolist()
            for index in column_changes:
                new_row = {
                    'column_name': column,
                    'old_value': self.main_data.at[index, column],
                    'new_value': df.at[index, column],
                    'timestamp': pd.Timestamp.now()
                }
                self.history_data = pd.concat([self.history_data, pd.DataFrame([new_row])], ignore_index=True)
                progress_bar.update(1)  # обновляем прогресс-бар

        # Закрываем прогресс-бар
        progress_bar.close()
        # Обновляем основную таблицу
        self.main_data = df.copy()
        # Обновление схемы
        self.previous_schema = current_schema

    def get_data(self):
        return self.main_data

    def get_history(self):
        return self.history_data
