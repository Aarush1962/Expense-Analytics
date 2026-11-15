import json
import os
import sys
import pandas as pd

WARN_AT = 0.8  

def check_budgets(input_path, budgets_path, out_dir):
    df = pd.read_csv(input_path)
    df["Date"] = pd.to_datetime(df["Date"])
    if "Month" not in df.columns:
        df["Month"] = df["Date"].dt.strftime("%Y-%m")
    os.makedirs(out_dir, exist_ok=True)

    with open(budgets_path) as f:
        budgets = json.load(f)

    expenses = df[df["Type"] == "Debit"]
    actual = expenses.pivot_table(
        index="Month", columns="Category", values="Amount",
        aggfunc="sum", fill_value=0,
    )

    rows = []
    for month in actual.index:
        for category, limit in budgets.items():
            spent = float(actual.loc[month, category]) if category in actual.columns else 0.0
            used = spent / limit if limit else 0.0
            if spent > limit:
                status = "EXCEEDED"
            elif used >= WARN_AT:
                status = "WARNING"
            else:
                status = "OK"
            rows.append({
                "Month": month,
                "Category": category,
                "Budget": limit,
                "Actual": round(spent, 2),
                "Difference": round(limit - spent, 2),
                "Percent_Used": round(used * 100, 1),
                "Status": status,
            })

    report = pd.DataFrame(rows)
    violations = report[report["Status"] == "EXCEEDED"]

    report.to_csv(os.path.join(out_dir, "budget_vs_actual.csv"), index=False)
    violations.to_csv(os.path.join(out_dir, "budget_violations.csv"), index=False)

    unbudgeted = [c for c in actual.columns if c not in budgets]

    report_path = os.path.join(out_dir, "summary_report.txt")
    with open(report_path, "a") as f:
        f.write("\n===== BUDGET REPORT =====\n")
        f.write(report.to_string(index=False))
        f.write(f"\n\n{len(violations)} budget violation(s) found.\n")
        for _, r in violations.iterrows():
            f.write(f"  EXCEEDED: {r['Month']} {r['Category']} - "
                    f"spent {r['Actual']} of {r['Budget']}\n")
        if unbudgeted:
            f.write("No budget set for: " + ", ".join(unbudgeted) + "\n")

    if unbudgeted:
        print("No budget set for:", ", ".join(unbudgeted), "\n")
    print("Budget vs actual:\n", report.to_string(index=False), "\n")
    print(f"{len(violations)} budget violation(s) found.")


    monthly = report.groupby("Month")[["Budget", "Actual"]].sum()
    monthly["Deviation"] = (monthly["Actual"] - monthly["Budget"]).round(2)
    data_dir = os.path.join(out_dir, "gnuplot_data")
    os.makedirs(data_dir, exist_ok=True)
    monthly[["Budget", "Actual", "Deviation"]].to_csv(os.path.join(data_dir, "budget_deviation.dat"), sep="\t", header=False,)


if __name__ == "__main__":
    check_budgets(sys.argv[1], sys.argv[2], sys.argv[3])
