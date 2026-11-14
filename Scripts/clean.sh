
#!/bin/bash

set -euo pipefail

# Check command-line arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: bash Scripts/clean.sh <input_file> <output_file>"
    exit 1
fi

OriginalFile="$1"
FinalFile="$2"

# Check whether input file exists
if [ ! -f "$OriginalFile" ]; then
    echo "Error: Input file not found: $OriginalFile"
    exit 1
fi

# Create output directory if needed
mkdir -p "$(dirname "$FinalFile")"

# Keep header, remove failed and empty rows, sort by date
{
    head -n 1 "$OriginalFile"

    tail -n +2 "$OriginalFile" |
        grep -v "FAILED" |
        sed '/^[[:space:]]*$/d' |
        sort -t',' -k2,2
} > "$FinalFile"

echo "Raw Data File cleaned successfully: $FinalFile"

