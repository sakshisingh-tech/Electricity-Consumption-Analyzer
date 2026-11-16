# Electricity-Consumption-Analyzer
# Electricity Consumption Analyzer

**PS No. 8** | Programming Fundamentals and Logic Building using Python | First Semester
School of Computer Science and Engineering, B.Tech CSE

## Problem Statement
Analyse monthly electricity consumption from a CSV file using NumPy and Pandas to find
the total and average usage, the highest and lowest months and the months above average,
and visualise the trend with Matplotlib charts.

## Features
- Lists the CSV files in the project folder and lets the user choose one by number
- Cleans the data: rows with missing, non-numeric or negative Units are skipped with a message
- Calculates total, average, highest month, lowest month and standard deviation (population value, `np.std` default)
- Finds months above the average using boolean filtering
- Draws a bar chart (Monthly Consumption) and a line chart (Electricity Consumption Trend)
- Saves the charts as `bar_chart.png` and `line_chart.png`
- Handles errors: missing file, empty file, wrong column names, invalid menu choices

## Requirements
- Python 3
- NumPy, Pandas, Matplotlib

```
python -m pip install numpy pandas matplotlib
```

## Project Structure
```
electricity_analyzer/
|-- electricity_analyzer.py     main program
|-- usage.csv                   sample data
|-- test1_normal.csv            Test Case 1
|-- test2_boundary.csv          Test Case 2
|-- test3_invalid.csv           Test Case 3
|-- test4_above_average.csv     Test Case 4
|-- README.md
```

## How to Run
1. Keep the `.py` file and all the CSV files in the same folder.
2. Run:
   ```
   python electricity_analyzer.py
   ```
3. Choose a CSV file from the list by typing its number.
4. Choose an option from the menu.

## CSV Format
The file must have two columns named `Month` and `Units`.
```
Month,Units
Jan,200
Feb,250
Mar,300
```

## Menu
| Option | Action |
|--------|--------|
| 1 | Summary (total, average, highest, lowest, standard deviation) |
| 2 | Months above average and the bar chart |
| 3 | Trend line chart |
| 4 | Choose another CSV file |
| 5 | Exit |

## Test Cases
| No. | Type | File | Menu option | Expected output |
|-----|------|------|-------------|-----------------|
| 1 | Normal input | `test1_normal.csv` | 1 | Total: 750 units, Average: 250.00 / Highest: Mar (300), Lowest: Jan (200) / Std Dev: 40.82 |
| 2 | Boundary (1 row) | `test2_boundary.csv` | 1 | Total: 150 units, Average: 150.00 / Highest: Jan (150), Lowest: Jan (150) / Std Dev: 0.00 |
| 3 | Invalid input | `test3_invalid.csv` | 1 | Row 2 skipped: invalid Units 'abc'. / Row 3 skipped: Units cannot be negative. / Valid rows: 1, Total: 200 units |
| 4 | Different valid scenario | `test4_above_average.csv` | 2 | Months above average (250.00): Mar (300) / Bar chart 'Monthly Consumption' displayed |

### Sample Output (Test Case 1)
```
Total: 750 units | Average: 250.00
Highest: Mar (300) | Lowest: Jan (200)
Std Dev: 40.82
```

## Concepts Used
- Variables, type casting, `if-elif-else`, loops, functions
- Strings (methods, f-strings, `format()`)
- Lists, list comprehension, dictionaries, dictionary comprehension, sets
- Exception handling (`try / except`)
- NumPy: `sum`, `mean`, `std`, `argmax`, `argmin`
- Pandas: `read_csv`, DataFrame, data cleaning, boolean filtering
- Matplotlib: bar chart and line chart with title and labels

## Author
Name: Sakshi Singh 
