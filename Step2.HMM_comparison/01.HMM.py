import subprocess
import os
import pandas as pd

# ========= Configuration part (only need to change here) =========
# HMM file path
hmm_file = "your_hmm_file.hmm"

# Output Directory
output_dir = "hmm_results"

# List of files to be compared
faa_files = [
    "example1.faa",
    "example2.faa",
    "example3.faa"
]
# =========================================

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Column names for HMMER output (tblout format)
column_names = [
    "target_name", "accession", "query_name", "accession2", "E-value", "score", "bias",
    "E-value_dom", "score_dom", "bias_dom", "exp", "reg", "clu", "ov", "env", "dom", "rep", "inc", "description"
]

# Traverse each .faa file for comparison
for faa_file in faa_files:
    # Get the file name without the path (convenient for naming output)
    base_name = os.path.splitext(os.path.basename(faa_file))[0]

    output_txt = os.path.join(output_dir, f"{base_name}_vs_{os.path.basename(hmm_file).replace('.hmm','')}.txt")
    output_xlsx = os.path.join(output_dir, f"{base_name}_vs_{os.path.basename(hmm_file).replace('.hmm','')}.xlsx")

    # Execute hmmsearch
    subprocess.run(["hmmsearch", "--tblout", output_txt, hmm_file, faa_file], check=True)

    # Parsing HMMER Output
    with open(output_txt, "r") as infile:
        lines = infile.readlines()

    # Remove the commented line
    data = [line.split(maxsplit=18) for line in lines if not line.startswith("#")]

    if not data:
        print(f"⚠️ {faa_file} No hit results, skip conversion。")
        continue

    # Create DataFrame (adaptive number of columns)
    df = pd.DataFrame(data, columns=column_names[:len(data[0])])

    # Save as Excel file
    df.to_excel(output_xlsx, index=False)

print("✅ All HMM alignments are complete and the results have been saved as an XLSX file!")
