
import sys
import json
import subprocess
from pathlib import Path

import pandas as pd


def write_dat(file_path, rows):
    """Write tab-separated data for GNUplot."""
    with open(file_path, "w") as file:
        for row in rows:
            values = []
            for value in row:
                if isinstance(value, str):
                    value = '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
                values.append(str(value))
            file.write("\t".join(values) + "\n")


def generate_plots(input_path, output_dir):

    # 1. Load and prepare transaction data
    df = pd.read_csv(input_path)

    required_columns = {"Date", "Type", "Amount", "Description", "Category"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Type"] = df["Type"].astype(str).str.strip().str.lower()

    df = df.dropna(subset=["Date", "Amount"]).copy()
    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    project_dir = Path(__file__).resolve().parents[1]
    output_dir = Path(output_dir).resolve()
    data_dir = output_dir / "gnuplot_data"

    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    expenses = df[df["Type"] == "debit"].copy()
    income = df[df["Type"] == "credit"].copy()

    if expenses.empty and income.empty:
        raise ValueError("No valid debit or credit transactions found.")

    # 2. Monthly expense trend
    monthly_expenses = expenses.groupby("Month")["Amount"].sum().sort_index()

    write_dat(
        data_dir / "monthly_expenses.dat",
        [(month, amount) for month, amount in monthly_expenses.items()]
    )

    # 3. Category-wise expense distribution
    category_totals = (
        expenses.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    write_dat(
        data_dir / "category_totals.dat",
        [(category, amount) for category, amount in category_totals.items()]
    )

    # 4. Monthly income vs expenses
    monthly_income = income.groupby("Month")["Amount"].sum()
    monthly_spend = expenses.groupby("Month")["Amount"].sum()

    comparison = pd.DataFrame({
        "Income": monthly_income,
        "Expenses": monthly_spend
    }).fillna(0).sort_index()

    write_dat(
        data_dir / "income_vs_expenses.dat",
        [
            (month, row["Income"], row["Expenses"])
            for month, row in comparison.iterrows()
        ]
    )

    # 5. Monthly savings
    savings = comparison["Income"] - comparison["Expenses"]

    write_dat(
        data_dir / "monthly_savings.dat",
        [(month, amount) for month, amount in savings.items()]
    )

    # 6. Daily spending and 7-day moving average
    if not expenses.empty:
        expenses["Date"] = expenses["Date"].dt.normalize()

        daily = expenses.groupby("Date")["Amount"].sum()

        full_dates = pd.date_range(
            daily.index.min(),
            daily.index.max(),
            freq="D"
        )

        daily = daily.reindex(full_dates, fill_value=0)
        moving_average = daily.rolling(window=7, min_periods=1).mean()

        write_dat(
            data_dir / "daily_spending.dat",
            [
                (date.strftime("%Y-%m-%d"), amount, average)
                for date, amount, average
                in zip(daily.index, daily.values, moving_average.values)
            ]
        )

    # 7. Budget vs actual spending
    budgets_path = project_dir / "Config" / "budgets.json"

    if budgets_path.exists() and not expenses.empty:
        with open(budgets_path, "r") as file:
            budgets = json.load(file)

        latest_month = expenses["Month"].max()
        latest_expenses = expenses[
            expenses["Month"] == latest_month
        ]

        actual = latest_expenses.groupby("Category")["Amount"].sum()

        write_dat(
            data_dir / "budget_vs_actual.dat",
            [
                (category, budgets[category], actual.get(category, 0))
                for category in budgets
            ]
        )

    # 8. Execute GNUplot
    gnuplot_script = project_dir / "Scripts" / "plots.gp"

    if not gnuplot_script.exists():
        raise FileNotFoundError(f"GNUplot script not found: {gnuplot_script}")

    command = (
        f'DATA_DIR="{data_dir}"; '
        f'OUTPUT_DIR="{output_dir}"'
    )

    subprocess.run(
        ["gnuplot", "-e", command, str(gnuplot_script)],
        check=True
    )

    print(f"GNUplot charts successfully saved in: {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Src/plots.py <input_csv> <output_directory>")
        sys.exit(1)

    generate_plots(sys.argv[1], sys.argv[2])
