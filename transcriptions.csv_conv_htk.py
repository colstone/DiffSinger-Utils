import os
import csv
from tqdm import tqdm

# 定义函数，创建目录
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 输入CSV文件路径
csv_file_path = input("请输入CSV文件的路径：")

# 读取CSV文件
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # 获取CSV文件名（不包含扩展名）
    csv_file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    
    # 创建存储lab文件的文件夹
    output_directory = f"{csv_file_name}_phoneme"
    create_directory(output_directory)

    # 遍历CSV文件的每一行
    for row in tqdm(csv_reader, desc="生成lab文件进度"):
        name = row["name"]
        ph_seq = row["ph_seq"].split()
        ph_dur = row["ph_dur"].split()
        
        # 创建lab文件并写入phoneme、起始时间和结束时间
        lab_file_path = os.path.join(output_directory, f"{name}.lab")
        with open(lab_file_path, 'w') as lab_file:
            start_time = 0  # 初始化起始时间
            for phoneme, duration in zip(ph_seq, ph_dur):
                duration_htk = int(float(duration) * 1e7)
                end_time = start_time + duration_htk
                lab_file.write(f"{start_time} {end_time} {phoneme}\n")
                start_time = end_time

print("lab文件生成完成！")
