#!/bin/bash

# 设置你想要查找的目录路径
search_dir="fold_25_0620"

output="ptm_values.txt"
echo -e "name\tptm" > "$output"

find "$search_dir" -type f -name "*confidences_0.json" -print0 | while IFS= read -r -d '' file; do
    fname=$(basename "$file")
    name=$(echo "$fname" | sed -n 's/^fold_\(.*\)_summary_confidences_0\.json$/\1/p')
    if [[ -z "$name" ]]; then
        echo "Warning: 无法从文件名提取序列名: $fname" >&2
        continue
    fi

    ptm=$(jq -r '.ptm // "NA"' "$file")
    echo -e "${name}\t${ptm}" >> "$output"
done
