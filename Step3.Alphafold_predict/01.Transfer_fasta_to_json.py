from Bio import SeqIO
import json
import os

# Input file path
input_fasta = "mirus_mcp_updated.fasta"
score_file = "score_70to200_dedup.txt"
output_dir = "score_70to200_dedup"

# Output file path
os.makedirs(output_dir, exist_ok=True)

# Read the score_up_100.txt file and extract the sequence ID
with open(score_file, 'r') as f:
    sequence_ids = f.read().splitlines()

# Store the sequences in the FASTA file in a dictionary, with the key being the sequence ID and the value being the sequence
sequences = {}
for record in SeqIO.parse(input_fasta, "fasta"):
    seq_id = record.id.split()[0]  # Extract sequence ID (remove possible description information)
    sequences[seq_id] = str(record.seq)

# Filter out the required sequences and save them in JSON format
for seq_id in sequence_ids:
    if seq_id in sequences:
        sequence = sequences[seq_id]
        
        # Constructing JSON data
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

        # The output is a JSON file named sequence ID
        output_path = os.path.join(output_dir, f"{seq_id}.json")
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
