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
    

## For all IMGVR hits (get IMGVR.2ndRound_mirusMCP.faa)
all_faa_file__IMGVR = "/storage2/databases/IMGVR-NCBI_phages/IMGVR_V4/IMGVR_all_proteins.faa"
all_faa_seq__IMGVR = store_seq(all_faa_file__IMGVR)
mirusvirus_MCP_hits__IMGVR = []
with open('2ndRound_DIAMOND_BLASTP_result/IMGVR_all_proteins_Match2_mirusvirus_MCP_db.2ndRound.tsv', 'r') as lines:
    for line in lines:
        line = line.rstrip('\n')
        MCP_hit = line.split('\t')[0]
        mirusvirus_MCP_hits__IMGVR.append(MCP_hit)
        
MCP_hits_faa_seq__IMGVR = {}
for header in all_faa_seq__IMGVR:
    header_wo_arrow = header[1:]
    if header_wo_arrow in mirusvirus_MCP_hits__IMGVR:
        if len(all_faa_seq__IMGVR[header]) >= 180 and len(all_faa_seq__IMGVR[header]) <= 4000:
            MCP_hits_faa_seq__IMGVR[header] = all_faa_seq__IMGVR[header]  

write_down_seq(MCP_hits_faa_seq__IMGVR, 'IMGVR.2ndRound_mirusMCP.faa')
