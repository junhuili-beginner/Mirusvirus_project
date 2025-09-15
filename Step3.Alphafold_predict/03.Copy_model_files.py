import os
import shutil

ptm_file = 'ptm_values.txt'
source_dir = 'your_alphafold_predict.files'
target_dir = 'ptm>0.5'

# Create the target directory if it does not exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Read ptm_values.txt and filter names with ptm > 0.5
selected_names = set()
with open(ptm_file, 'r') as f:
    next(f)  # Skip header
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) != 2:
            continue
        name, ptm_str = parts
        try:
            ptm = float(ptm_str)
        except ValueError:
            continue
        if ptm > 0.5:
            selected_names.add(name)

print(f"Filter out {len(selected_names)} names with ptm>0.5。")

# Used to avoid copying duplicate file contents
seen_hashes = set()

# Traverse source_dir, find the corresponding model_0.cif file and copy it
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if not file.endswith('model_0.cif'):
            continue
        # Determine whether the file name contains any of the selected names
        # Here it is assumed that the file name format contains name as a substring
        for name in selected_names:
            if name in file:
                source_file = os.path.join(root, file)
                with open(source_file, 'rb') as f:
                    content_hash = hash(f.read())
                if content_hash not in seen_hashes:
                    shutil.copy(source_file, target_dir)
                    seen_hashes.add(content_hash)
                    print(f"Copy files: {source_file}")
                else:
                    print(f"跳过重复文件: {source_file}")
                break  # 找到匹配就跳出内层循环，继续下一文件

print("所有符合条件的文件复制完成。")
