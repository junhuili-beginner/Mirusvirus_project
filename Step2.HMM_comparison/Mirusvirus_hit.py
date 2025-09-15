import pandas as pd
from Bio import SeqIO

# 读取筛选后的 XLSX 文件
filtered_df = pd.read_excel('hmm_mirusvirus_filtered.xlsx')

# 提取需要的序列标识符（'target_name'列）
target_names = filtered_df['target_name'].tolist()

# 打印前几个 target_name，确认读取正确
print(f"前几个 target_name：{target_names[:10]}")

# 创建一个输出文件用于存储匹配的序列
output_file = 'mirusvirus_hits.faa'

# 打开输出文件并写入
with open(output_file, 'w') as output_handle:
    # 处理每个原始的 FASTA 文件
    for fasta_file in [
        '/storage2/scratch/zzhou388/Mirusvirus_project/IMGVR.2ndRound_mirusMCP.faa', 
        '/storage2/scratch/zzhou388/Mirusvirus_project/201704_MF1.2ndRound_mirusMCP.faa', 
        '/storage2/scratch/zzhou388/Mirusvirus_project/TYMEFLIES.2ndRound_mirusMCP2.faa'
    ]:
        print(f"正在处理文件：{fasta_file}")
        
        # 读取每个 FASTA 文件
        for record in SeqIO.parse(fasta_file, 'fasta'):
            # 如果序列标识符在 target_names 中，则写入新的文件
            if record.id in target_names:
                SeqIO.write(record, output_handle, 'fasta')

print(f"提取的序列已保存到 {output_file}")
