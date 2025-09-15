#!/usr/bin/env python3

import logging

# 设置日志记录
logging.basicConfig(filename='201704_MF1_2ndRound_mirusMCP.size.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def store_seq(input_seq_file):
    """
    将 .faa 文件中的序列存储到字典中，键为序列头部，值为序列本身。
    """
    seq_dict = {}
    head = ""

    try:
        with open(input_seq_file, "r") as seq_lines:
            for line in seq_lines:
                line = line.rstrip("\n")
                if line.startswith(">"):
                    head = line.split(None, 1)[0]
                    seq_dict[head] = ""
                else:
                    seq_dict[head] += line
    except Exception as e:
        logging.error(f"读取文件 {input_seq_file} 时出错: {e}")

    return seq_dict

def write_down_seq(seq_dict, output_file):
    """
    将筛选出的序列写入到指定的输出文件中。
    """
    try:
        with open(output_file, "w") as out_file:
            for head, seq in seq_dict.items():
                out_file.write(f"{head}\n{seq}\n")
        logging.info(f"成功写入 {len(seq_dict)} 个序列到文件: {output_file}")
    except Exception as e:
        logging.error(f"写入文件 {output_file} 时出错: {e}")

def read_fasta_in_chunks(faa_file, chunk_size=1000):
    """
    逐块读取 .faa 文件，每块的大小由 chunk_size 决定。
    """
    seq_dict = {}
    current_count = 0
    head = ""

    try:
        with open(faa_file, "r") as seq_lines:
            for line in seq_lines:
                line = line.rstrip("\n")
                if line.startswith(">"):
                    if current_count >= chunk_size:
                        yield seq_dict  # 返回当前块
                        seq_dict = {}  # 重置字典
                        current_count = 0

                    head = line.split(None, 1)[0]
                    seq_dict[head] = ""
                    current_count += 1
                else:
                    seq_dict[head] += line

            if seq_dict:  # 返回最后一块
                yield seq_dict
    except Exception as e:
        logging.error(f"读取文件 {faa_file} 时出错: {e}")

def process_hits_in_chunks(faa_file, tsv_file, output_file, chunk_size=1000):
    """按块处理 .faa 文件和 .tsv 文件，筛选出匹配的序列并写入到输出文件中"""
    logging.info(f"正在处理 .faa 文件: {faa_file}")

    # 读取 .tsv 文件并提取 MCP hits，转换为集合
    mirusvirus_MCP_hits = set()
    try:
        with open(tsv_file, 'r') as tsv:
            for line in tsv:
                MCP_hit = line.strip().split('	')[0]
                mirusvirus_MCP_hits.add(MCP_hit)  # 使用集合
    except Exception as e:
        logging.error(f"读取文件 {tsv_file} 时出错: {e}")

    # 逐块处理 .faa 文件
    with open(output_file, "w") as out_f:
        for chunk in read_fasta_in_chunks(faa_file, chunk_size=chunk_size):
            MCP_hits_faa_seq = {}
            for header, sequence in chunk.items():
                header_wo_arrow = header[1:]  # 去掉 '>'
                if header_wo_arrow in mirusvirus_MCP_hits and 180 <= len(sequence) <= 4000:
                    MCP_hits_faa_seq[header] = sequence

            # 将符合条件的序列写入输出文件
            for head, seq in MCP_hits_faa_seq.items():
                out_f.write(f"{head}\n{seq}\n")
    
    logging.info(f"处理完成并写入文件: {output_file}")

if __name__ == "__main__":
    # 指定 .faa 和 .tsv 文件
    faa_file = "/storage2/scratch/zzhou388/Giant_virus_project/IAS_mangrove_metagenome_assembly_and_cov_dir/201704_MF1.contigs_1000bp.faa"
    tsv_file = "2ndRound_DIAMOND_BLASTP_result/201704_MF1_Match2_mirusvirus_MCP_db.2ndRound.tsv"
    output_file = "201704_MF1.2ndRound_mirusMCP.faa"

    # 调用处理函数
    process_hits_in_chunks(faa_file, tsv_file, output_file)
    logging.info("脚本运行完成")



