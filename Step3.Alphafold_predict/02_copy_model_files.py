import os
import shutil

ptm_file = 'ptm_values.txt'
source_dir = 'fold_25_0620'
target_dir = 'ptm>0.5'

# 创建目标目录（如果不存在）
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 读取ptm_values.txt，筛选ptm > 0.5的name
selected_names = set()
with open(ptm_file, 'r') as f:
    next(f)  # 跳过表头
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

print(f"筛选出 {len(selected_names)} 个ptm>0.5的name。")

# 用于避免复制重复文件内容
seen_hashes = set()

# 遍历 source_dir，找到对应的model_0.cif文件并复制
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if not file.endswith('model_0.cif'):
            continue
        # 判断文件名是否包含选中name中的任何一个
        # 这里假设文件名格式中包含name作为子串
        for name in selected_names:
            if name in file:
                source_file = os.path.join(root, file)
                with open(source_file, 'rb') as f:
                    content_hash = hash(f.read())
                if content_hash not in seen_hashes:
                    shutil.copy(source_file, target_dir)
                    seen_hashes.add(content_hash)
                    print(f"复制文件: {source_file}")
                else:
                    print(f"跳过重复文件: {source_file}")
                break  # 找到匹配就跳出内层循环，继续下一文件

print("所有符合条件的文件复制完成。")
