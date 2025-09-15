import subprocess
import os
import pandas as pd

# 设定变量
hmm_file = "/storage2/scratch/zzhou388/Mirusvirus_project/MandEandF_mirusvirus_MCP.HMM/MandEandF_mirusvirus_MCP.hmm"
output_dir = "/storage2/scratch/zzhou388/Mirusvirus_project/hmm_results/hmm_MandEanF_mirusvirus/hmm_mirusvirus_results/1"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 需要比对的 .faa 文件列表
faa_files = [
    "/storage2/scratch/zzhou388/Mirusvirus_project/IMGVR.2ndRound_mirusMCP.faa",
    "/storage2/scratch/zzhou388/Mirusvirus_project/201704_MF1.2ndRound_mirusMCP.faa",
    "/storage2/scratch/zzhou388/Mirusvirus_project/TYMEFLIES.2ndRound_mirusMCP2.faa"
]

# 对每个 .faa 文件进行比对并保存结果
for faa_file in faa_files:
    # 生成输出文件名
    output_txt = os.path.join(output_dir, f"{os.path.splitext(faa_file)[0]}_vs_mirusvirus_mcp.txt")
    output_xlsx = os.path.join(output_dir, f"{os.path.splitext(faa_file)[0]}_vs_mirusvirus_mcp.xlsx")

    # 执行比对并保存输出到 .txt 文件
    subprocess.run(["hmmsearch", "--tblout", output_txt, hmm_file, faa_file], check=True)

    # 解析 HMMER 输出并转换为 DataFrame
    with open(output_txt, "r") as infile:
        lines = infile.readlines()

    # 过滤掉注释行（以 "#" 开头）
    data = [line.split() for line in lines if not line.startswith("#")]

    # 提取表头（在 HMMER 的 `tblout` 输出格式中，表头信息位于 `#` 行内，但 HMMER 不直接输出表头）
    column_names = [
        "target_name", "accession", "query_name", "accession2", "E-value", "score", "bias",
        "E-value_dom", "score_dom", "bias_dom", "exp", "reg", "clu", "ov", "env", "dom", "rep", "inc", "description"
    ]

    # 创建 DataFrame
    df = pd.DataFrame(data, columns=column_names[:len(data[0])])  # 适配列数

    # 保存为 .xlsx 文件
    df.to_excel(output_xlsx, index=False)

print("HMM 比对完成，结果已转换为 XLSX 文件！")
