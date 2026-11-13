#!/bin/bash

Orginal_file = $1 
Clean_file = "data/cleanedCSV.csv"


grep -v  "FAILED "  "$Original_file" | sed  '/^$/d' > "$Clean_file"

echo "Data Cleaned using Unix tools" 


python3 Src/analytics.py "$Clean_file" 

echo "Data Analytics completed and Reports are available "


