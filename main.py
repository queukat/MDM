import pandas as pd

from data_generator import generate_data
from data_model import DataModelV5
from analytics import describe_data, plot_distribution
from data_validation import check_missing_values, check_duplicates, check_anomalies, check_regex, check_normalization, check_allowed_values, check_unique_values, check_date_range, check_column_dependency
from historical_analysis import column_trends_over_time
from analytics import plot_column_trends, plot_heatmap
from data_management import UnifiedDataManager
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, ttk

def main_v2():
    model = DataModelV5()

    while True:
        print("=== Исторический MDM ===")
        print("1. Генерировать и загрузить новые данные")
        print("2. Просмотреть актуальные данные")
        print("3. Просмотреть историю изменений")
        print("4. Статистический анализ данных")
        print("5. Визуализация распределения данных")
        print("6. Выход")
        print("7. Проверить типы данных")
        print("8. Проверить пропущенные значения")
        print("9. Проверить дубликаты")
        print("10. Проверить аномалии в столбце")
        print("11. Показать тенденции столбца со временем")
        print("12. Показать тепловую карту корреляций")
        print("13. Проверить даты на допустимый диапазон")
        print("14. Проверить редкие значения в категориальных столбцах")
        print("15. Проверить строки на соответствие регулярным выражениям")
        choice = input("Выберите действие: ")

        if choice == "1":
            new_data = generate_data()
            model.load_data(new_data)
            print("Данные успешно загружены!")
        elif choice == "2":
            print(model.get_data())
        elif choice == "3":
            print(model.get_history())
        elif choice == "4":
            print(describe_data(model.get_data()))
        elif choice == "5":
            column = input("Введите имя столбца для визуализации: ")
            plot_distribution(model.get_data(), column)
        elif choice == "6":
            break
        elif choice == "7":
            expected_types = {"col_string1": "str", "col_string2": "str", "col_num1": "float64", "col_num2": "int64",
                              "col_date": "datetime64[ns]"}
            mismatches = check_data_types(model.get_data(), expected_types)
            if mismatches:
                print("Обнаружены несоответствия в типах данных:", mismatches)
            else:
                print("Все типы данных соответствуют ожидаемым.")

        elif choice == "8":
            missing_values = check_missing_values(model.get_data())
            if not missing_values.empty:
                print("Обнаружены пропущенные значения:", missing_values)
            else:
                print("Пропущенных значений нет.")

        elif choice == "9":
            duplicates = check_duplicates(model.get_data())
            if not duplicates.empty:
                print("Обнаружены дубликаты:", duplicates)
            else:
                print("Дубликатов нет.")

        elif choice == "10":
            column = input("Введите имя столбца для проверки: ")
            lower_bound = float(input("Введите нижнюю границу (или оставьте пустым): ") or float('-inf'))
            upper_bound = float(input("Введите верхнюю границу (или оставьте пустым): ") or float('inf'))
            anomalies = check_anomalies(model.get_data(), column, lower_bound, upper_bound)
            if not anomalies.empty:
                print("Обнаружены аномалии:", anomalies)
            else:
                print("Аномалий в указанном диапазоне нет.")

        elif choice == "11":
            column = input("Введите имя столбца для анализа: ")
            time_column = input("Введите имя временного столбца: ")
            trends = column_trends_over_time(model.get_data(), column, time_column)
            plot_column_trends(trends, column, time_column)

        elif choice == "12":
            plot_heatmap(model.get_data())
        elif choice == "13":
            column = input("Введите имя столбца с датами для проверки: ")
            start_date = input("Введите начальную дату (формат YYYY-MM-DD или оставьте пустым): ")
            end_date = input("Введите конечную дату (формат YYYY-MM-DD или оставьте пустым): ")
            anomalies = check_anomalies(model.get_data(), columns=[column], date_range=(start_date, end_date))
            if not anomalies.empty:
                print("Обнаружены аномальные даты:", anomalies)
            else:
                print("Все даты в указанном диапазоне.")

        elif choice == "14":
            column = input("Введите имя категориального столбца для проверки: ")
            anomalies = check_anomalies(model.get_data(), columns=[column])
            if not anomalies.empty:
                print("Обнаружены редкие категории:", anomalies)
            else:
                print("Не найдено редких категорий.")

        elif choice == "15":
            column = input("Введите имя столбца со строками для проверки: ")
            pattern = input("Введите регулярное выражение для проверки: ")
            anomalies = check_anomalies(model.get_data(), columns=[column], regex_patterns={column: pattern})
            if not anomalies.empty:
                print("Строки, не соответствующие регулярному выражению:", anomalies)
            else:
                print("Все строки соответствуют регулярному выражению.")

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


def main_gui():
    root = tk.Tk()
    root.title("MDM Project GUI")

    def generate_and_load_data():
        new_data = generate_data()
        model.load_data(new_data)
        messagebox.showinfo("Info", "Данные успешно загружены!")

    def show_current_data():
        data = model.get_data()
        top = Toplevel(root)
        text = tk.Text(top)
        text.insert(tk.END, str(data))
        text.pack()

    def show_history():
        history = model.get_history()
        top = Toplevel(root)
        text = tk.Text(top)
        text.insert(tk.END, str(history))
        text.pack()

    # ... Другие функции для каждой из опций main_v2 ...

    label = tk.Label(root, text="MDM Project")
    label.pack(pady=20)

    btn1 = tk.Button(root, text="Generate and Load Data", command=generate_and_load_data)
    btn1.pack(pady=5)

    btn2 = tk.Button(root, text="Show Current Data", command=show_current_data)
    btn2.pack(pady=5)

    btn3 = tk.Button(root, text="Show Data History", command=show_history)
    btn3.pack(pady=5)

    # ... Другие кнопки для каждой из опций main_v2 ...

    exit_btn = tk.Button(root, text="Exit", command=root.quit)
    exit_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    interface_choice = input("Выберите интерфейс (1: Текстовый, 2: Графический): ")

    if interface_choice == "1":
        main_v2()
    elif interface_choice == "2":
        main_gui()
    else:
        print("Неверный выбор. Пожалуйста, попробуйте снова.")