import pandas as pd

from data_generator import generate_data
from data_model import DataModelV5
from analytics import describe_data, plot_distribution
from data_validation import check_missing_values, check_duplicates, check_anomalies, check_regex, check_normalization, \
    check_allowed_values, check_unique_values, check_date_range, check_column_dependency
from historical_analysis import column_trends_over_time
from analytics import plot_column_trends, plot_heatmap
from data_management import UnifiedDataManager
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, ttk


def main_v2():
    """
    The main function for the MDM project. It coordinates the interaction between different modules and provides a user interface.
    """
    model = DataModelV5()

    while True:
        # Text-based User Interface Section
        print("=== Historical MDM ===")
        print("1. Generate and load new data")
        print("2. View current data")
        print("3. View change history")
        print("4. Statistical data analysis")
        print("5. Data distribution visualization")
        print("6. Exit")
        print("7. Check data types")
        print("8. Check missing values")
        print("9. Check duplicates")
        print("10. Check column anomalies")
        print("11. Show column trends over time")
        print("12. Show heatmap of correlations")
        print("13. Check dates for valid range")
        print("14. Check rare values in categorical columns")
        print("15. Check rows for regular expression match")
        print("16. Check for Unique Values")
        print("17. Check Allowed Values")

        choice = input("Select an action: ")

        if choice == "1":
            new_data = generate_data()
            model.load_data(new_data)
            print("Data loaded successfully!")
        elif choice == "2":
            print(model.get_data())
        elif choice == "3":
            print(model.get_history())
        elif choice == "4":
            print(describe_data(model.get_data()))
        elif choice == "5":
            column = input("Input the column name for visualization: ")
            plot_distribution(model.get_data(), column)
        elif choice == "6":
            break
        elif choice == "7":
            expected_types = {"col_string1": "str", "col_string2": "str", "col_num1": "float64", "col_num2": "int64",
                              "col_date": "datetime64[ns]"}
            mismatches = check_data_types(model.get_data(), expected_types)
            if mismatches:
                print("Data type mismatches detected:", mismatches)
            else:
                print("All data types match the expected ones.")

        elif choice == "8":
            missing_values = check_missing_values(model.get_data())
            if not missing_values.empty:
                print("Missing values detected:", missing_values)
            else:
                print("No missing values.")

        elif choice == "9":
            duplicates = check_duplicates(model.get_data())
            if not duplicates.empty:
                print("Duplicates detected:", duplicates)
            else:
                print("No duplicates found.")

        elif choice == "10":
            column = input("Enter the column name for checking: ")
            lower_bound = float(input("Enter the lower bound (or leave empty): ") or float('-inf'))
            upper_bound = float(input("Enter the upper bound (or leave empty): ") or float('inf'))
            anomalies = check_anomalies(model.get_data(), column, lower_bound, upper_bound)
            if not anomalies.empty:
                print("Anomalies detected:", anomalies)
            else:
                print("No anomalies in the specified range.")

        elif choice == "11":
            column = input("Enter the column name for analysis: ")
            time_column = input("Enter the time column name: ")
            trends = column_trends_over_time(model.get_data(), column, time_column)
            plot_column_trends(trends, column, time_column)

        elif choice == "12":
            plot_heatmap(model.get_data())
        elif choice == "13":
            column = input("Enter the column name with dates for checking: ")
            start_date = input("Enter the start date (format YYYY-MM-DD or leave empty): ")
            end_date = input("Enter the end date (format YYYY-MM-DD or leave empty): ")
            anomalies = check_anomalies(model.get_data(), columns=[column], date_range=(start_date, end_date))
            if not anomalies.empty:
                print("Anomalous dates detected:", anomalies)
            else:
                print("All dates within the specified range.")

        elif choice == "14":
            column = input("Enter the name of the categorical column to check: ")
            anomalies = check_anomalies(model.get_data(), columns=[column])
            if not anomalies.empty:
                print("Rare categories detected:", anomalies)
            else:
                print("No rare categories found.")

        elif choice == "15":
            column = input("Enter the name of the column with strings for checking: ")
            pattern = input("Enter the regular expression for checking: ")
            anomalies = check_anomalies(model.get_data(), columns=[column], regex_patterns={column: pattern})
            if not anomalies.empty:
                print("Strings that do not match the regular expression:", anomalies)
            else:
                print("All rows match the regular expression.")

        elif choice == "16":
            column = input("Enter the column name to check for uniqueness: ")
            is_unique = check_unique_values(model.get_data(), column)
            if is_unique:
                print("All values in the column are unique.")
            else:
                print("There are non-unique values in the column.")

        elif choice == "17":
            column = input("Enter the column name to check allowed values: ")
            allowed_values = input("Enter allowed values separated by comma: ").split(',')
            is_allowed = check_allowed_values(model.get_data(), column, allowed_values)
            if is_allowed:
                print("All values in the column are within the allowed list.")
            else:
                print("There are values in the column not within the allowed list.")

        else:
            print("Incorrect choice. Please try again.")


def main_gui():
    """
    Main function for the MDM project. Coordinates interaction between different modules and provides a graphical user interface.
    """
    model = DataModelV5()

    root = tk.Tk()
    root.title("MDM Project GUI")
    root.configure(bg='#ADD8E6')

    style = ttk.Style(root)
    style.configure('TButton', background='#FFFFFF', borderwidth=0)
    style.map('TButton', background=[('active', '#E0E0E0')])  # Стиль кнопки при наведении

    def show_in_new_window(content):
        top = Toplevel(root)
        text = tk.Text(top)
        text.insert(tk.END, str(content))
        text.pack()

    def ask_text_input(title, prompt):
        def return_entry(en):
            user_input.set(entry.get())
            popup.destroy()

        popup = Toplevel(root)
        popup.title(title)
        label = tk.Label(popup, text=prompt)
        label.pack(side="top", fill="x", pady=10)
        user_input = tk.StringVar()
        entry = tk.Entry(popup, textvariable=user_input)
        entry.pack()
        entry.focus_set()
        submit_button = ttk.Button(popup, text="Submit", command=lambda: return_entry(None))
        popup.bind('<Return>', return_entry)
        submit_button.pack(pady=20)

        popup.grab_set()  # Modal window
        root.wait_window(popup)

        return user_input.get()

    def generate_and_load_data():
        new_data = generate_data()
        model.load_data(new_data)
        messagebox.showinfo("Info", "Data loaded successfully!")

    def show_current_data():
        data = model.get_data()
        show_in_new_window(data)

    def show_history():
        history = model.get_history()
        show_in_new_window(history)

    def show_statistics():
        stats = describe_data(model.get_data())
        show_in_new_window(stats)

    def plot_data_distribution():
        column = ask_text_input("Input", "Enter the column name for visualization:")
        if column:
            plot_distribution(model.get_data(), column)

    def check_data_types_gui():
        expected_types = {"column1": "str", "column2": "int"}
        mismatches = check_data_types(model.get_data(), expected_types)
        message = "Data type mismatches:" + str(
            mismatches) if mismatches else "All data types match the expected ones."
        messagebox.showinfo("Info", message)

    def check_missing_values_gui():
        missing_values = check_missing_values(model.get_data())
        if not missing_values.empty:
            show_in_new_window(missing_values)
        else:
            messagebox.showinfo("Info", "No missing values.")

    def plot_column_trends_gui():
        column = ask_text_input("Input", "Enter the column name for analysis:")
        time_column = simpledialog.askstring("Input", "Enter the time column name:")
        if column and time_column:
            trends = column_trends_over_time(model.get_data(), column, time_column)
            plot_column_trends(trends, column, time_column)

    def plot_heatmap_gui():
        plot_heatmap(model.get_data())

    def check_date_range_gui():
        column = ask_text_input("Input", "Enter the date column name:")
        start_date = ask_text_input("Input", "Enter start date (YYYY-MM-DD):")
        end_date = ask_text_input("Input", "Enter end date (YYYY-MM-DD):")
        if column:
            anomalies = check_anomalies(model.get_data(), columns=[column], date_range=(start_date, end_date))
            if not anomalies.empty:
                show_in_new_window(anomalies)
            else:
                messagebox.showinfo("Info", "All dates within the specified range.")

    def check_rare_categorical_values_gui():
        column = ask_text_input("Input", "Enter the categorical column name:")
        if column:
            anomalies = check_anomalies(model.get_data(), columns=[column])
            if not anomalies.empty:
                show_in_new_window(anomalies)
            else:
                messagebox.showinfo("Info", "No rare categories found.")

    def check_regex_match_gui():
        column = ask_text_input("Input", "Enter the column name:")
        pattern = ask_text_input("Input", "Enter the regular expression:")
        if column and pattern:
            anomalies = check_anomalies(model.get_data(), columns=[column], regex_patterns={column: pattern})
            if not anomalies.empty:
                show_in_new_window(anomalies)
            else:
                messagebox.showinfo("Info", "All rows match the regular expression.")

    def check_unique_values_gui():
        column = ask_text_input("Input", "Enter the column name to check for uniqueness:")
        if column:
            is_unique = check_unique_values(model.get_data(), column)
            message = "All values in the column are unique." if is_unique else "There are non-unique values in the column."
            messagebox.showinfo("Info", message)

    def check_allowed_values_gui():
        column = ask_text_input("Input", "Enter the column name to check allowed values:")
        allowed_values = ask_text_input("Input", "Enter allowed values separated by comma:").split(',')
        if column:
            is_allowed = check_allowed_values(model.get_data(), column, allowed_values)
            message = "All values in the column are within the allowed list." if is_allowed else "There are values in the column not within the allowed list."
            messagebox.showinfo("Info", message)

    label = tk.Label(root, text="MDM Project")
    label.pack(pady=20)

    buttons = [
        ("Generate and Load Data", generate_and_load_data),
        ("Show Current Data", show_current_data),
        ("Show Data History", show_history),
        ("Statistical Data Analysis", show_statistics),
        ("Data distribution visualization", plot_data_distribution),
        ("Check data types", check_data_types_gui),
        ("Check missing values", check_missing_values_gui),
        ("Show Column Trends Over Time", plot_column_trends_gui),
        ("Show Heatmap of Correlations", plot_heatmap_gui),
        ("Check Dates for Valid Range", check_date_range_gui),
        ("Check Rare Values in Categorical Columns", check_rare_categorical_values_gui),
        ("Check Rows for Regular Expression Match", check_regex_match_gui),
        ("Check Unique Values in Column", check_unique_values_gui),
        ("Check Allowed Values in Column", check_allowed_values_gui),

    ]

    for text, command in buttons:
        btn = ttk.Button(root, text=text, command=command, style='TButton')
        btn.pack(pady=10, padx=10, fill='x')

    exit_btn = tk.Button(root, text="Exit", command=root.quit)
    exit_btn.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    interface_choice = input("(Select the interface (1: Text-based, 2: Graphical): ")

    if interface_choice == "1":
        main_v2()
    elif interface_choice == "2":
        main_gui()
    else:
        print("Incorrect choice. Please try again.")
