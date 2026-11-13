import os
import sys
import numpy as np
import pandas as pd


def compute_stats(input_path, out_dir):
    df = pd.read_csv(input_path)
    df["Date"] = pd.to_datetime(df["Date"])
    os.makedirs(out_dir, exist_ok=True)

    expenses = df[df["Type"] == "Debit"]
    income = df[df["Type"] == "Credit"]
        # 1. Monthly spend
    monthly_spend = expenses.groupby("Month")["Amount"].sum()

    # 2. Category totals with percentage share
    category_total = (
        expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    )
    category_share = pd.DataFrame({
        "total": category_total,
        "percent": np.round(category_total / category_total.sum() * 100, 2),
    })
        # 3. Month x category pivot
    pivot = expenses.pivot_table(
        index="Month", columns="Category", values="Amount",
        aggfunc="sum", fill_value=0,
    )

    # 4. Per-category summary
    category_summary = (
        expenses.groupby("Category")["Amount"]
        .agg(["count", "sum", "mean", "median", "max", "std"])
        .round(2)
        .sort_values("sum", ascending=False)
    )
        # 5. Monthly savings
    monthly_income = income.groupby("Month")["Amount"].sum()
    savings = pd.DataFrame({
        "income": monthly_income,
        "spend": monthly_spend,
    }).fillna(0)
    savings["savings"] = savings["income"] - savings["spend"]

    # 6. 7-day moving average of daily spend
    daily = expenses.groupby("Date")["Amount"].sum()
    full_range = pd.date_range(daily.index.min(), daily.index.max())
    daily = daily.reindex(full_range, fill_value=0)
    daily_df = pd.DataFrame({
        "spend": daily,
        "moving_avg_7d": daily.rolling(7).mean().round(2),
    })
    daily_df.index.name = "Date"

        
    monthly_spend.to_csv(os.path.join(out_dir, "monthly_spend.csv"))
    category_share.to_csv(os.path.join(out_dir, "category_totals.csv"))
    pivot.to_csv(os.path.join(out_dir, "month_category_pivot.csv"))
    category_summary.to_csv(os.path.join(out_dir, "category_summary.csv"))
    savings.to_csv(os.path.join(out_dir, "monthly_savings.csv"))
    daily_df.to_csv(os.path.join(out_dir, "daily_spend.csv"))

    print("Monthly spend:\n", monthly_spend, "\n")
    print("Top categories:\n", category_share.head(5), "\n")
    print("Savings:\n", savings)


if __name__ == "__main__":
    compute_stats(sys.argv[1], sys.argv[2])