#!/usr/bin/env python3

try:
    import warnings
    import sys
    import os
    from collections import defaultdict
    warnings.filterwarnings("ignore")
    from pathlib import Path
    from glob import glob
except Exception as e:
    sys.stderr.write(str(e) + "\n\n")
    exit(1)

# Aim: Cluster all 1st round Mirusvirus MCP proteins  
   
    
def store_seq(input_seq_file): # The input sequence file should be a file with full path
    head = "" # Store the header line
    seq_dict = {} # Store the sequence dict
    
    with open(input_seq_file, "r") as seq_lines:
        for line in seq_lines:
            line = line.rstrip("\n") # Remove "\n" in the end
            if ">" in line:
                head = line.split(None, 1)[0] # Cut at the first " " or "\t", use the first part
                seq_dict[head] = ""                 
            else:
                seq_dict[head] += line
    
    return seq_dict
    
def write_down_seq(seq_dict, path_to_file): 
    # Two inputs are required:
    # (1) The dict of the sequence
    # (2) The path that you want to write your sequence down
    
    seq_file = open(path_to_file,"w")
    for head in seq_dict:
        seq_file.write(head + "\n")
        seq_file.write(seq_dict[head] + "\n")
    seq_file.close()    
    
'''    
# Step 1 Collect all mirusvirus MCP hits
## Step 1.1 For all 201704 MF1 hits (get 201704_MF1.1stRound_mirusMCP.faa)
all_faa_file__201704_MF1 = "/storage2/scratch/zzhou388/Giant_virus_project/IAS_mangrove_metagenome_assembly_and_cov_dir/201704_MF1.contigs_1000bp.faa"
all_faa_seq__201704_MF1 = store_seq(all_faa_file__201704_MF1)
mirusvirus_MCP_hits__201704_MF1 = []
with open('201704_MF1_Match2_mirusvirus_MCP_db.tsv', 'r') as lines:
    for line in lines:
        line = line.rstrip('\n')
        MCP_hit = line.split('\t')[0]
        bitscore = float(line.split('\t')[-1])
        if bitscore >= 50:
            mirusvirus_MCP_hits__201704_MF1.append(MCP_hit)
        
MCP_hits_faa_seq__201704_MF1 = {}
for header in all_faa_seq__201704_MF1:
    header_wo_arrow = header[1:]
    if header_wo_arrow in mirusvirus_MCP_hits__201704_MF1:
        if len(all_faa_seq__201704_MF1[header]) >= 180:
            MCP_hits_faa_seq__201704_MF1[header] = all_faa_seq__201704_MF1[header]  

write_down_seq(MCP_hits_faa_seq__201704_MF1, '201704_MF1.1stRound_mirusMCP.faa')

## Step 1.2 For all IMGVR hits (get IMGVR.1stRound_mirusMCP.faa)
all_faa_file__IMGVR = "/storage2/databases/IMGVR-NCBI_phages/IMGVR_V4/IMGVR_all_proteins.faa"
all_faa_seq__IMGVR = store_seq(all_faa_file__IMGVR)
mirusvirus_MCP_hits__IMGVR = []
with open('IMGVR_all_proteins_Match2_mirusvirus_MCP_db.tsv', 'r') as lines:
    for line in lines:
        line = line.rstrip('\n')
        MCP_hit = line.split('\t')[0]
        bitscore = float(line.split('\t')[-1])
        if bitscore >= 50:
            mirusvirus_MCP_hits__IMGVR.append(MCP_hit)
        
MCP_hits_faa_seq__IMGVR = {}
for header in all_faa_seq__IMGVR:
    header_wo_arrow = header[1:]
    if header_wo_arrow in mirusvirus_MCP_hits__IMGVR:
        if len(all_faa_seq__IMGVR[header]) >= 180:
            MCP_hits_faa_seq__IMGVR[header] = all_faa_seq__IMGVR[header]  

write_down_seq(MCP_hits_faa_seq__IMGVR, 'IMGVR.1stRound_mirusMCP.faa')
'''
## Step 1.3 For all TYMEFLIES hits (get TYMEFLIES.1stRound_mirusMCP.faa)
all_faa_files__TYMEFLIES = glob("/storage1/data11/TYMEFLIES_phage/*/VIBRANT_*.a/*.a.prodigal.faa") 

all_faa_seq__TYMEFLIES = {}
for faa_file in all_faa_files__TYMEFLIES:
    all_faa_seq__TYMEFLIES.update(store_seq(faa_file))

mirusvirus_MCP_hits__TYMEFLIES = []
# Adjusting to read each TSV file individually
tsv_files = glob("VIBRANT_*.a_Match2_mirusvirus_MCP_db.tsv")
for tsv_file in tsv_files:
    with open(tsv_file, 'r') as lines:
        for line in lines:
            line = line.rstrip('\n')
            MCP_hit = line.split('\t')[0]
            bitscore = float(line.split('\t')[-1])
            if bitscore >= 50:
                mirusvirus_MCP_hits__TYMEFLIES.append(MCP_hit)

MCP_hits_faa_seq__TYMEFLIES = {}
for header in all_faa_seq__TYMEFLIES:
    header_wo_arrow = header[1:]
    if header_wo_arrow in mirusvirus_MCP_hits__TYMEFLIES:
        if len(all_faa_seq__TYMEFLIES[header]) >= 180:
            MCP_hits_faa_seq__TYMEFLIES[header] = all_faa_seq__TYMEFLIES[header]

write_down_seq(MCP_hits_faa_seq__TYMEFLIES, 'TYMEFLIES.1stRound_mirusMCP.faa')  

    
