#!/bin/bash

# Set the directory path you want to search
search_dir="your_alphafold_predict.files"

output="ptm_values.txt"
echo -e "name\tptm" > "$output"

find "$search_dir" -type f -name "*confidences_0.json" -print0 | while IFS= read -r -d '' file; do
    fname=$(basename "$file")
    name=$(echo "$fname" | sed -n 's/^fold_\(.*\)_summary_confidences_0\.json$/\1/p')
    if [[ -z "$name" ]]; then
        echo "Warning: Unable to extract sequence name from file name: $fname" >&2
        continue
    fi

    ptm=$(jq -r '.ptm // "NA"' "$file")
    echo -e "${name}\t${ptm}" >> "$output"
done
