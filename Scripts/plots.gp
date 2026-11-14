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
# 4. MONTHLY SAVINGS
# ============================================================

set output OUTPUT_DIR . "/monthly_savings.png"

set title "Monthly Savings" font ",16"
set xlabel "Month"
set ylabel "Savings (INR)"

set style data boxes
set boxwidth 0.6
set zeroaxis
set xtics rotate by -30

plot DATA_DIR . "/monthly_savings.dat" \
    using 0:2:xtic(1) \
    with boxes title "Monthly Savings"

unset output
unset xlabel
unset ylabel
unset title
unset xtics
unset zeroaxis

# ============================================================
# 5. DAILY SPENDING TREND
# ============================================================

set output OUTPUT_DIR . "/daily_spending.png"

set title "Daily Spending Trend" font ",16"
set xlabel "Date"
set ylabel "Amount (INR)"

set xdata time
set timefmt "%Y-%m-%d"
set format x "%d-%b"
set xtics rotate by -30
set yrange [0:*]
set style data lines
set key outside

plot DATA_DIR . "/daily_spending.dat" \
    using 1:2 \
    with linespoints linewidth 1.5 pointtype 7 \
    title "Daily Spending", \
    '' using 1:3 \
    with lines linewidth 2 \
    title "7-Day Moving Average"

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