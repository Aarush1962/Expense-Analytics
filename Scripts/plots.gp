# ============================================================
# Personal Finance & Expense Analytics Tool
# GNUplot Visualization Script
# ============================================================

# Directories
if (!exists("DATA_DIR")) DATA_DIR = "Reports/gnuplot_data"
if (!exists("OUTPUT_DIR")) OUTPUT_DIR = "Reports"

# General settings
set terminal pngcairo size 1200,700 enhanced font "Arial,12"
set datafile separator "\t"
set border linewidth 1.2
set grid ytics
set key outside
set tics out
set style fill solid 0.75 border -1

# ============================================================
# 1. MONTHLY EXPENSE TREND
# ============================================================

set output OUTPUT_DIR . "/monthly_expenses.png"

set title "Monthly Expense Trend" font ",16"
set xlabel "Month"
set ylabel "Expenses (INR)"

set yrange [0:*]
set style data linespoints
set pointsize 1.5
set xtics rotate by -30

plot DATA_DIR . "/monthly_expenses.dat" \
    using 0:2:xtic(1) \
    with linespoints linewidth 2 pointtype 7 \
    title "Monthly Expenses"

unset output
unset yrange
unset xlabel
unset ylabel
unset title
unset xtics

# ============================================================
# 2. EXPENSE DISTRIBUTION BY CATEGORY
# ============================================================

set output OUTPUT_DIR . "/category_distribution.png"

set title "Expense Distribution by Category" font ",16"
set xlabel "Category"
set ylabel "Amount (INR)"

set yrange [0:*]
set style data boxes
set boxwidth 0.7
set xtics rotate by -30

plot DATA_DIR . "/category_totals.dat" \
    using 0:2:xtic(1) \
    with boxes linewidth 1 \
    title "Category Expenses"

unset output
unset yrange
unset xlabel
unset ylabel
unset title
unset xtics

# ============================================================
# 3. MONTHLY INCOME VS EXPENSES
# ============================================================

set output OUTPUT_DIR . "/income_vs_expenses.png"

set title "Monthly Income vs Expenses" font ",16"
set xlabel "Month"
set ylabel "Amount (INR)"

set yrange [0:*]
set style data histograms
set style histogram clustered gap 1
set style fill solid 0.75 border -1
set xtics rotate by -30

plot DATA_DIR . "/income_vs_expenses.dat" \
    using 2:xtic(1) title "Income", \
    '' using 3 title "Expenses"

unset output
unset yrange
unset xlabel
unset ylabel
unset title
unset xtics

# ============================================================
# 4. MONTHLY SAVINGS AND VIOLATIONS
# ============================================================

set output OUTPUT_DIR . "/monthly_savings.png"

set title "Monthly Savings and Violations" font ",16"
set xlabel "Month"
set ylabel "Amount (INR)"

set style data linespoints
set pointsize 1.5
set zeroaxis
set xtics rotate by -30

plot DATA_DIR . "/monthly_savings.dat" \
    using 0:2:xtic(1) \
    with linespoints linewidth 2 pointtype 7 linecolor rgb "#1f77b4" \
    title "Monthly Savings", \
    DATA_DIR . "/budget_deviation.dat" \
    using 0:4 \
    with linespoints linewidth 2 pointtype 5 linecolor rgb "#d62728" \
    title "Spending - Budget (above 0 = violation)"

unset output
unset xlabel
unset ylabel
unset title
unset xtics
unset zeroaxis

# ============================================================
# 5. DAILY SPENDING TREND (smooth lines, monthly markers)
# ============================================================

set output OUTPUT_DIR . "/daily_spending.png"

set title "Monthly Spending" font ",16"
set xlabel "Date"
set ylabel "Amount (INR)"

set xdata time
set timefmt "%Y-%m-%d"
set format x "%d-%b"
set xtics rotate by -30
set yrange [0:*]
set samples 500
set key outside

plot DATA_DIR . "/daily_spending.dat" \
    using 1:2 smooth csplines \
    with lines linewidth 1.5 linecolor rgb "#9ecae1" \
    title "Daily Spending", \
    '' using 1:3 smooth csplines \
    with lines linewidth 3 linecolor rgb "#1f77b4" \
    title "7-Day Moving Average", \
    '' using 1:(strftime("%d", timecolumn(1) + 86400) eq "01" ? $3 : 1/0) \
    with points pointtype 7 pointsize 1.8 linecolor rgb "#d62728" \
    title "Month end"

unset output
unset xdata
unset timefmt
unset format
unset xtics
unset yrange
unset xlabel
unset ylabel
unset title

# ============================================================
# 6. BUDGET VS ACTUAL SPENDING
# ============================================================

set output OUTPUT_DIR . "/budget_vs_actual.png"

set title "Budget vs Actual Spending" font ",16"
set xlabel "Category"
set ylabel "Amount (INR)"

set yrange [0:*]
set style data histograms
set style histogram clustered gap 1
set style fill solid 0.75 border -1
set xtics rotate by -30

plot DATA_DIR . "/budget_vs_actual.dat" \
    using 2:xtic(1) title "Budget", \
    '' using 3 title "Actual Spending"

unset output
unset yrange
unset xlabel
unset ylabel
unset title
unset xtics

# ============================================================
# END OF SCRIPT
# ============================================================

print "All six GNUplot charts generated successfully."
