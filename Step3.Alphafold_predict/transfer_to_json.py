from Bio import SeqIO
import json
import os

# 输入文件路径
input_fasta = "mirus_mcp_updated.fasta"
score_file = "score_70to200_dedup.txt"
output_dir = "score_70to200_dedup"

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 读取score_up_100.txt文件，提取序列ID
with open(score_file, 'r') as f:
    sequence_ids = f.read().splitlines()

# 将FASTA文件中的序列存储在字典中，键为序列ID，值为序列
sequences = {}
for record in SeqIO.parse(input_fasta, "fasta"):
    seq_id = record.id.split()[0]  # 提取序列ID（去掉可能的描述信息）
    sequences[seq_id] = str(record.seq)

# 过滤出需要的序列并保存为JSON格式
for seq_id in sequence_ids:
    if seq_id in sequences:
        sequence = sequences[seq_id]
        
        # 构建JSON数据
        data = [
            {
                "name": f"AlphaFold Job - {seq_id}",
                "modelSeeds": [],
                "sequences": [
                    {
                        "proteinChain": {
                            "sequence": sequence,
                            "count": 1
                        }
                    }
                ],
                "dialect": "alphafoldserver",
                "version": 1
            }
        ]

        # 输出为JSON文件，文件名为序列ID
        output_path = os.path.join(output_dir, f"{seq_id}.json")
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
