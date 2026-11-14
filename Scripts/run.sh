#!/bin/bash

set -e 

RAW_CSV=${1:-"Data/raw/personal_transactions.csv"}

bash Scripts/clean.sh "$RAW_CSV"  "Data/processed/unix_clean.csv" 
python3  Src/load.py "Data/processed/unix_clean.csv" "Data/processed/cleaned_expenses.csv"
python3  Src/classify.py "Data/processed/cleaned_expenses.csv" "Config/categories.json" "Data/processed/categorized.csv"
python3  Src/stats.py "Data/processed/categorized.csv"  "Reports/summary_report.txt" 
python3  Src/budget.py "Data/processed/categorized.csv" "Config/budgets.json" "Reports/summary_report.txt" 
python3 Src/plots.py "Data/processed/categorized.csv" "Reports"

echo "pipeline Finished , Check Reports Folder . All Plots are Available"