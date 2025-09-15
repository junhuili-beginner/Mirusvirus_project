import pandas as pd

# 输入文件路径
pfam_xlsx = "/storage2/scratch/zzhou388/Mirusvirus_project/hmm_results/hmm_MandEanF_mirusvirus/hmm_Pfam/Pfam-A_vs_mirusvirus_hits.xlsx"
mirus_xlsx = "/storage2/scratch/zzhou388/Mirusvirus_project/hmm_results/hmm_MandEanF_mirusvirus/hmm_mirusvirus_results/hmm_mirusvirus.xlsx"

# 输出文件路径
filtered_xlsx = "/storage2/scratch/zzhou388/Mirusvirus_project/hmm_results/hmm_MandEanF_mirusvirus/hmm_mirusvirus_filtered/hmm_mirusvirus_filtered.xlsx"
removed_txt = "/storage2/scratch/zzhou388/Mirusvirus_project/hmm_results/hmm_MandEanF_mirusvirus/hmm_mirusvirus_filtered/removed_sequences.txt"

# 读取 Pfam-A 结果，重命名 E-value
pfam_df = pd.read_excel(pfam_xlsx)
pfam_df = pfam_df.rename(columns={"E-value": "Epfam"})

# 读取 Mirusvirus 结果，重命名 E-value
mirus_df = pd.read_excel(mirus_xlsx)
mirus_df = mirus_df.rename(columns={"E-value": "Emirus"})

# 仅保留相关列
pfam_df = pfam_df[["target_name", "Epfam", "score", "bias"]]
mirus_df = mirus_df[["target_name", "Emirus", "score", "bias"]]

# 删除重复的 target_name，保留第一个出现的
pfam_df = pfam_df.drop_duplicates(subset=["target_name"])

# 将原始数据中的每个序列与 Pfam-A 结果中的数据对应
mirus_df["Epfam"] = mirus_df["target_name"].map(pfam_df.set_index("target_name")["Epfam"])
mirus_df["score_pfam"] = mirus_df["target_name"].map(pfam_df.set_index("target_name")["score"])
mirus_df["bias_pfam"] = mirus_df["target_name"].map(pfam_df.set_index("target_name")["bias"])

# 筛选满足条件的序列（Emirus * 100 > Epfam 的序列将被移除）
filtered_df = mirus_df[~(mirus_df["Emirus"] * 100 > mirus_df["Epfam"])]

# 生成移除的序列（在原始文件中有但筛选后没有的）
removed_sequences = mirus_df[~mirus_df["target_name"].isin(filtered_df["target_name"])]

# 保存筛选后的数据
filtered_df.to_excel(filtered_xlsx, index=False)

# 将被移除的 target_name 另存为 txt 文件
removed_sequences["target_name"].to_csv(removed_txt, index=False, header=False)

print(f"筛选完成，保留 {len(filtered_df)} 条数据，已保存至 {filtered_xlsx}")
print(f"移除 {len(removed_sequences)} 条数据，序列名已保存至 {removed_txt}")

