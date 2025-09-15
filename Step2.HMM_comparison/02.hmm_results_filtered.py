import pandas as pd

# Input file path
pfam_xlsx = "Pfam-A_vs_mirusvirus_hits.xlsx"
mirus_xlsx = "hmm_mirusvirus.xlsx"

# Output file path
filtered_xlsx = "hmm_mirusvirus_filtered.xlsx"
removed_txt = "removed_sequences.txt"

# Read Pfam-A results and rename E-value
pfam_df = pd.read_excel(pfam_xlsx)
pfam_df = pfam_df.rename(columns={"E-value": "Epfam"})

# Read Mirusvirus results and rename E-value
mirus_df = pd.read_excel(mirus_xlsx)
mirus_df = mirus_df.rename(columns={"E-value": "Emirus"})

# Keep only relevant columns
pfam_df = pfam_df[["target_name", "Epfam", "score", "bias"]]
mirus_df = mirus_df[["target_name", "Emirus", "score", "bias"]]

# Remove duplicate target_name, keeping the first occurrence
pfam_df = pfam_df.drop_duplicates(subset=["target_name"])

# Match each sequence in the original data with the data in the Pfam-A results
mirus_df["Epfam"] = mirus_df["target_name"].map(pfam_df.set_index("target_name")["Epfam"])
mirus_df["score_pfam"] = mirus_df["target_name"].map(pfam_df.set_index("target_name")["score"])
mirus_df["bias_pfam"] = mirus_df["target_name"].map(pfam_df.set_index("target_name")["bias"])

# Filter sequences that meet the criteria (sequences with Emirus * 100 > Epfam will be removed)
filtered_df = mirus_df[~(mirus_df["Emirus"] * 100 > mirus_df["Epfam"])]

# Generate removed sequences (those present in the original file but not after filtering)
removed_sequences = mirus_df[~mirus_df["target_name"].isin(filtered_df["target_name"])]

# Save filtered data
filtered_df.to_excel(filtered_xlsx, index=False)

# Save the removed target_name as a txt file
removed_sequences["target_name"].to_csv(removed_txt, index=False, header=False)

print(f"Filtering completed, retaining {len(filtered_df)} data items, saved to {filtered_xlsx}")
print(f"Removed {len(removed_sequences)} data, the sequence names have been saved to {removed_txt}")

