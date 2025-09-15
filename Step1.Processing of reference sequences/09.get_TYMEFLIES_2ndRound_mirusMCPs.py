#!/usr/bin/env python3

import logging
from glob import glob
import os

# 设置日志记录
logging.basicConfig(filename='TYMEFLIES_2ndRound_mirusMCP2.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def process_hits(faa_files, tsv_files, output_file):
    """
    处理所有的 .faa 和 .tsv 文件，筛选出匹配的序列并写入到输出文件中。
    """
    all_faa_seq = {}
    mirusvirus_MCP_hits = set()

    # 处理所有 .faa 文件
    for faa_file in faa_files:
        logging.info(f"正在处理 .faa 文件: {faa_file}")
        all_faa_seq.update(store_seq(faa_file))

    # 处理所有 .tsv 文件并提取 MCP hits
    for tsv_file in tsv_files:
        logging.info(f"正在处理 .tsv 文件: {tsv_file}")
        try:
            with open(tsv_file, 'r') as tsv:
                for line in tsv:
                    mirusvirus_MCP_hits.add(line.split('	')[0])
        except Exception as e:
            logging.error(f"读取 .tsv 文件 {tsv_file} 时出错: {e}")

    # 筛选符合条件的序列
    MCP_hits_faa_seq = {}
    for header, sequence in all_faa_seq.items():
        header_wo_arrow = header[1:]
        if header_wo_arrow in mirusvirus_MCP_hits and 180 <= len(sequence) <= 4000:
            MCP_hits_faa_seq[header] = sequence

    # 写入结果到文件
    write_down_seq(MCP_hits_faa_seq, output_file)

if __name__ == "__main__":
    # 查找所有 .faa 文件和对应的 .tsv 文件
    faa_files = glob("/storage1/data11/TYMEFLIES_phage/*/VIBRANT_*.a/*.a.prodigal.faa")
    tsv_files = glob("2ndRound_DIAMOND_BLASTP_result/VIBRANT_*.a_Match2_mirusvirus_MCP_db.2ndRound.tsv")

    if not faa_files:
        logging.warning("未找到任何 .faa 文件。")
    if not tsv_files:
        logging.warning("未找到任何 .tsv 文件。")

    # 调用处理函数
    process_hits(faa_files, tsv_files, 'TYMEFLIES.2ndRound_mirusMCP2.faa')
    logging.info("脚本运行完成")





