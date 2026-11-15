# Personal Finance & Expense Analytics Tool

An end-to-end, reproducible pipeline that turns a raw bank-transaction CSV into cleaned data, categorised expenses, monthly and category statistics, budget-violation reports and charts, all with a single command.

> Course project, Indian Institute of Technology Dharwad.

```
Raw CSV ──clean.sh──▶ unix_clean.csv ──load.py──▶ cleaned_expenses.csv ──classify.py──▶ categorized.csv
                                                                                              │
                          ┌───────────────────────────────┬───────────────────────────────────┤
                          ▼                               ▼                                   ▼
                      stats.py                        budget.py                      plots.py + plots.gp
                   summary tables                  budget reports                       PNG charts
```

## Topics Covered

- **Unix text processing**: `grep`, `sed` and `sort` to clean the raw file (`Scripts/clean.sh`)
- **Data wrangling** with Python, Pandas and NumPy (loading, grouping, pivoting, rolling averages)
- **Rule-based classification** of transactions using keywords from a JSON file
- **Statistics**: monthly spend, category share, month × category pivot, per-category summary, monthly savings, 7-day moving average of daily spend
- **Budget checking** with `OK` / `WARNING` / `EXCEEDED` statuses
- **Visualisation** with Gnuplot
- **Automation** with a Bash driver script
- **Reporting** with a LaTeX report and slides (PDFs included)

## Project Structure

```
Expense-Analytics/
├── Config/
│   ├── budgets.json              # monthly budget per category (INR)
│   └── categories.json           # keyword rules for classification
├── Data/
│   ├── raw/                      # input CSV (personal_transactions-3.csv)
│   └── processed/                # intermediate and result CSVs
├── Src/
│   ├── load.py                   # load, drop incomplete rows, add Month column
│   ├── classify.py               # assign a Category to each transaction
│   ├── stats.py                  # monthly / category statistics
│   ├── budget.py                 # budget vs actual, violation detection
│   └── plots.py                  # writes .dat files and calls Gnuplot
├── Scripts/
│   ├── run.sh                    # runs the whole pipeline
│   ├── clean.sh                  # Unix-based raw data cleaning
│   └── plots.gp                  # Gnuplot script for all charts
├── Reports/                      # generated PNG charts + gnuplot_data/*.dat
├── Report.pdf                    # project report
├── Detailed_Presentation.pdf     # project slides
└── requirements.txt
```

## Installation

**Requirements**

- Python 3
- Bash and standard Unix tools (`grep`, `sed`, `sort`, `head`, `tail`)
- [Gnuplot](http://www.gnuplot.info/) (needs the `pngcairo` terminal)

```bash
# 1. Clone and enter the project
git clone <repository-url>
cd Expense-Analytics

# 2. (Optional) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Python dependencies (pandas, numpy)
pip install -r requirements.txt

# 4. Install Gnuplot
sudo apt install gnuplot        # Debian / Ubuntu
brew install gnuplot            # macOS
```

## Usage

Run everything from the project root:

```bash
bash Scripts/run.sh                      # uses Data/raw/personal_transactions-3.csv
bash Scripts/run.sh path/to/other.csv    # use your own transactions file
```

The script stops at the first error (`set -e`). Results are written to:

- `Data/processed/` for the cleaned, categorised and summary CSVs
- `Reports/` for the PNG charts (and `Reports/gnuplot_data/` for the plot data)

### Running individual stages

```bash
bash   Scripts/clean.sh Data/raw/personal_transactions-3.csv Data/processed/unix_clean.csv
python3 Src/load.py     Data/processed/unix_clean.csv Data/processed/cleaned_expenses.csv
python3 Src/classify.py Data/processed/cleaned_expenses.csv Config/categories.json Data/processed/categorized.csv
python3 Src/stats.py    Data/processed/categorized.csv Data/processed
python3 Src/budget.py   Data/processed/categorized.csv Config/budgets.json Data/processed
python3 Src/plots.py    Data/processed/categorized.csv Reports
```

### Input format

The raw CSV must contain these columns:

| Column           | Meaning                          | Example                          |
|------------------|----------------------------------|----------------------------------|
| `Transaction_ID` | Unique identifier                | `TXN1001`                        |
| `Date`           | Transaction date (`YYYY-MM-DD`)  | `2026-01-02`                     |
| `Description`    | Payment mode, reference, merchant| `UPI/201100/MYNTRA DESIGNS`      |
| `Type`           | `Debit` (expense) or `Credit` (income) | `Debit`                    |
| `Amount`         | Value in INR                     | `1650.0`                         |
| `Status`         | `SUCCESS` or `FAILED`            | `SUCCESS`                        |

### Customising

- **Categories**: edit `Config/categories.json`. Each category maps to a list of lower-case keywords matched against the description. The first category with a matching keyword wins; anything unmatched becomes `Others`.
- **Budgets**: edit `Config/budgets.json` (monthly limit per category, in INR). A category is flagged `WARNING` at 80% of its limit (`WARN_AT` in `Src/budget.py`) and `EXCEEDED` above 100%.

## Outputs

**Processed data (`Data/processed/`)**

| File | Content |
|------|---------|
| `unix_clean.csv` | Failed and blank rows removed, sorted by date |
| `cleaned_expenses.csv` | Incomplete rows dropped, `Month` column added |
| `categorized.csv` | Transactions with their `Category` |
| `monthly_spend.csv` | Total expenses per month |
| `category_totals.csv` | Spend per category with percentage share |
| `month_category_pivot.csv` | Month × category spend |
| `category_summary.csv` | Count, sum, mean, median, max, std per category |
| `monthly_savings.csv` | Income, spend and savings per month |
| `daily_spend.csv` | Daily spend with 7-day moving average |
| `budget_vs_actual.csv` | Budget comparison for every month and category |
| `budget_violations.csv` | Only the `EXCEEDED` rows |

**Charts (`Reports/`)**: `monthly_expenses.png`, `category_distribution.png`, `income_vs_expenses.png`, `monthly_savings.png`, `daily_spending.png`, `budget_vs_actual.png`.

## Sample Results

On the bundled synthetic dataset (305 transactions covering calendar year 2026):

- 13 failed rows removed by the cleaning step; 268 expense records classified
- Total spend of INR 202,516 against income of INR 198,500, a net deficit of INR 4,016
- Bills & Rent (37.9%) and Shopping (23.5%) make up over 60% of spending
- 28 budget violations across 12 months; Shopping exceeded its budget in 10 of them

## Compilation (LaTeX Report and Slides)

The final `Report.pdf` (article) and `Detailed_Presentation.pdf` (Beamer slides) are included in the repository. The `.tex` sources are not part of this folder; if you add them (for example under `docs/`), build with:

```bash
pdflatex Report.tex && pdflatex Report.tex                 # run twice for the table of contents
pdflatex Detailed_Presentation.tex && pdflatex Detailed_Presentation.tex
```

## Assumptions and Limitations

- The dataset is synthetic. Real bank statements may have more varied descriptions and formats.
- Classification is keyword-based and order-dependent: the first matching category wins, and unknown merchants fall into `Others`.
- The `Entertainment` budget (INR 500) is never used because `categories.json` has no Entertainment keywords. Netflix, Spotify, PVR and BookMyShow transactions land in `Others`, which inflates its violations. Pharmacy purchases are also in `Others`.
- Monthly budgets are fixed and identical for every month.
- Failed transactions are removed by matching the text `FAILED` anywhere in a row.
- `clean.sh` sorts by the second CSV column, so the `Date` column must stay in position two.
- The budget-vs-actual chart shows only the latest month in the data.
- The `.gitignore` lists lower-case paths (`data/processed/*`, `reports/*`), which do not match the capitalised `Data/` and `Reports/` folders. Update it if you want generated files excluded from version control.

## Testing and Profiling

There are no automated unit tests or profiling yet. Correctness was checked by running the pipeline end to end and inspecting the intermediate CSVs, which are kept on disk after each stage. A quick smoke test:

```bash
bash Scripts/run.sh && ls Data/processed Reports
```

To time the pipeline: `time bash Scripts/run.sh`.

## Team

Shivam Tripathi, Vuppugandla Aarush, Mukhil Mariappan, Dinesh Karthik and Achintya Das, Indian Institute of Technology Dharwad.
