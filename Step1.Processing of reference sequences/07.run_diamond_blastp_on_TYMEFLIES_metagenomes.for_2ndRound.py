import os
import glob
import subprocess

# Define the directory pattern to search for .faa files
search_pattern = "/storage1/data11/TYMEFLIES_phage/*/VIBRANT_*.a/*.a.prodigal.faa"

# Use glob to find all matching .faa files
faa_files = glob.glob(search_pattern)

# Diamond blastp command template
command_template = "diamond blastp --ultra-sensitive --max-target-seqs 1 --evalue 0.01 --threads 40 -d mirusvirus_mcp_2nd -q {query} -o {output}"

# Iterate over each found .faa file
for faa_file in faa_files:
    # Extract the identifier from the file path
    identifier = faa_file.split("/")[5]  # This assumes the identifier is in the 6th position
    
    # Construct the output file name
    output_file = f"{identifier}_Match2_mirusvirus_MCP_db.2ndRound.tsv"
    
    # Format the command with the current .faa file and output file
    command = command_template.format(query=faa_file, output=output_file)
    
    # Print the command for debugging purposes
    print(f"Running command: {command}")
    
    # Run the command using subprocess
    subprocess.run(command, shell=True)
