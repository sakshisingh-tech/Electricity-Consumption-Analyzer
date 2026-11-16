# Electricity Consumption Analyzer (PS No. 8)
# Made using the topics of the first semester Python syllabus:
# variables, type casting, if-elif-else, loops, functions, lambda, modules (import),
# strings (methods, f-strings, format()), tuples, lists, list comprehension,
# dictionaries, dictionary comprehension, sets, exception handling,
# NumPy (arrays, statistics), Pandas (DataFrame, data cleaning, reading CSV),
# Matplotlib (bar chart, line chart)

import os
import sys

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    print("Pandas, NumPy or Matplotlib is not installed.")
    print("Install them with:  python -m pip install pandas numpy matplotlib")
    sys.exit()

# folder where this .py file is saved, so the CSV files are found from any terminal folder
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

NEEDED = {"Month", "Units"}              # set of the columns that every CSV file must have


def choose_file():
    # list comprehension: keep only the file names that end with .csv
    files = sorted([f for f in os.listdir(BASE_FOLDER) if f.lower().endswith(".csv")])
    if len(files) == 0:
        print("No CSV files found in " + BASE_FOLDER)
        return None

    print("")
    print("CSV files found in this folder:")
    for number, name in enumerate(files, start=1):   # enumerate gives 1, 2, 3 ... with each name
        print(f"{number}. {name}")

    while True:
        try:
            choice = int(input("Choose a file (1-{}): ".format(len(files))))
        except ValueError:
            print("Please enter a number from the list.")
            continue
        if 1 <= choice <= len(files):
            return files[choice - 1]     # list index starts from 0, so subtract 1
        print("Invalid choice")


def load_usage(file_name):
    path = os.path.join(BASE_FOLDER, file_name)

    # step 1: read the file (dtype=str reads everything as text so we can check each value ourselves)
    try:
        raw = pd.read_csv(path, dtype=str)
    except FileNotFoundError:
        print("Error: " + file_name + " not found in " + BASE_FOLDER)
        return None
    except pd.errors.EmptyDataError:
        print("Error: " + file_name + " is empty.")
        return None

    # step 2: check that all the needed columns are present (using sets)
    raw.columns = raw.columns.str.strip()
    missing = NEEDED - set(raw.columns)
    if len(missing) > 0:
        print("Error: missing column(s): " + ", ".join(sorted(missing)))
        return None

    # step 3: clean the data row by row, row numbers start from 1 (header is not counted)
    months = []
    units_list = []
    for row_no, (month, units) in enumerate(zip(raw["Month"], raw["Units"]), start=1):
        if pd.isna(month) or pd.isna(units) or units.strip() == "":
            print("Row {} skipped: missing data.".format(row_no))
            continue

        try:
            value = float(units)         # type casting: text -> number
        except ValueError:
            print(f"Row {row_no} skipped: invalid Units '{units}'.")
            continue

        if not np.isfinite(value):       # words like nan or inf are not real readings
            print(f"Row {row_no} skipped: invalid Units '{units}'.")
            continue

        if value < 0:
            print(f"Row {row_no} skipped: Units cannot be negative.")
            continue

        months.append(month.strip())     # row is good, so keep it
        units_list.append(value)

    df = pd.DataFrame({"Month": months, "Units": units_list})

    # if any row was skipped, show how many valid rows are left
    if len(df) < len(raw):
        print(f"Valid rows: {len(df)} | Total: {df['Units'].sum():g} units")
    return df


def pick_and_load():
    # keep asking until a file with at least one valid row is loaded
    while True:
        file_name = choose_file()
        if file_name is None:
            return None, None

        print("")
        print("Loading " + file_name + " ...")
        df = load_usage(file_name)
        if df is None:
            continue
        if len(df) == 0:
            print("No valid rows found. Please choose another file.")
            continue
        return file_name, df


def show_summary(df):
    units = df["Units"].to_numpy()       # Pandas column -> NumPy array

    total = np.sum(units)
    mean = np.mean(units)
    std = np.std(units)                  # population value (np.std default)
    high = np.argmax(units)              # position of the biggest value
    low = np.argmin(units)               # position of the smallest value

    print(f"Total: {total:g} units | Average: {mean:.2f}")
    print(f"Highest: {df['Month'][high]} ({units[high]:g}) | Lowest: {df['Month'][low]} ({units[low]:g})")
    print(f"Std Dev: {std:.2f}")


def bar_chart(df, average):
    # list comprehension: red bar if the month is above average, blue otherwise
    colors = ["tomato" if u > average else "steelblue" for u in df["Units"]]

    plt.figure(figsize=(8, 5))
    plt.bar(df["Month"], df["Units"], color=colors)
    plt.axhline(average, color="green", linestyle="--", label=f"Average ({average:.2f})")
    plt.title("Monthly Consumption")
    plt.xlabel("Month")
    plt.ylabel("Units (kWh)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_FOLDER, "bar_chart.png"))    # saved so it can be used in the report
    print("Bar chart 'Monthly Consumption' displayed.")
    plt.show()


def line_chart(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df["Month"], df["Units"], marker="o", color="darkorange", label="Units used")
    plt.title("Electricity Consumption Trend")
    plt.xlabel("Month")
    plt.ylabel("Units (kWh)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_FOLDER, "line_chart.png"))
    print("Line chart 'Electricity Consumption Trend' displayed.")
    plt.show()


def above_average(df):
    average = np.mean(df["Units"].to_numpy())
    mask = df["Units"] > average         # True/False for every month (boolean filtering)
    above = df[mask]                     # keep only the True rows

    if above.empty:
        print(f"No month is above the average ({average:.2f}).")
    else:
        # dictionary comprehension: month name -> units of that month
        months = {m: u for m, u in zip(above["Month"], above["Units"])}
        # items() gives month and units together, join puts ", " between the parts
        line = ", ".join([f"{m} ({u:g})" for m, u in months.items()])
        print(f"Months above average ({average:.2f}): {line}")
    bar_chart(df, average)


# ---------------- main program ----------------
file_name, data = pick_and_load()
if data is None:
    print("No valid usage data found.")
else:
    while True:
        print("")
        print(f"===== Electricity Consumption Analyzer ({file_name}) =====")
        print("1. Summary")
        print("2. Above-average months and chart")
        print("3. Trend line chart")
        print("4. Choose another CSV file")
        print("5. Exit")
        try:
            choice = int(input("Menu: "))
        except ValueError:
            print("Please enter 1, 2, 3, 4 or 5.")
            continue

        if choice == 1:
            show_summary(data)
        elif choice == 2:
            above_average(data)
        elif choice == 3:
            line_chart(data)
        elif choice == 4:
            new_name, new_data = pick_and_load()
            if new_data is not None:         # keep the old file if nothing new was loaded
                file_name, data = new_name, new_data
        elif choice == 5:
            print("Thank you for using the analyzer. Goodbye!")
            break
        else:
            print("Invalid choice")