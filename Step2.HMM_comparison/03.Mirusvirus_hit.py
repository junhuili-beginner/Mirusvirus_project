import pandas as pd
from Bio import SeqIO

# Reading filtered XLSX files
filtered_df = pd.read_excel('hmm_mirusvirus_filtered.xlsx')

# Extract the required sequence identifier ('target_name' column)
target_names = filtered_df['target_name'].tolist()

# Print the first few target_names to confirm that they are read correctly
print(f"First few target_name：{target_names[:10]}")

# Create an output file to store the matched sequences
output_file = 'Potential_Mirusvirus_MCP.faa'

# Open the output file and write to it
with open(output_file, 'w') as output_handle:
    # Process each original FASTA file
    for fasta_file in [
        'example1.faa', 
        'example2.faa', 
        'example3.faa'
    ]:
        print(f"Processing file：{fasta_file}")
        
        # Read each FASTA file
        for record in SeqIO.parse(fasta_file, 'fasta'):
            # If the sequence identifier is in target_names, write to a new file
            if record.id in target_names:
                SeqIO.write(record, output_handle, 'fasta')

print(f"The extracted sequences are saved to {output_file}")
