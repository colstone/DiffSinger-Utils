import os
import csv

# 输入包含lab文件的文件夹路径
lab_folder_path = input("请输入包含lab文件的文件夹路径：")

# 创建CSV文件并写入表头
csv_file_name = "transcriptions.csv"
csv_file_path = os.path.join(lab_folder_path, csv_file_name)
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["name", "ph_seq", "ph_dur"])

# 遍历lab文件夹中的lab文件
for lab_file_name in os.listdir(lab_folder_path):
    if lab_file_name.endswith(".lab"):
        lab_file_path = os.path.join(lab_folder_path, lab_file_name)
        
        # 从lab文件名提取name部分
        name = os.path.splitext(lab_file_name)[0]
        
        # 读取lab文件内容并提取音素和持续时间信息
        ph_seq = []
        ph_dur = []
        with open(lab_file_path, 'r') as lab_file:
            for line in lab_file:
                parts = line.strip().split()
                if len(parts) == 3:
                    ph_seq.append(parts[2])
                    duration_htk = int(parts[1]) - int(parts[0])
                    duration = duration_htk / 1e7  # 转换为秒
                    ph_dur.append(str(duration))
        
        # 将音素和持续时间信息写入CSV文件
        with open(csv_file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([name, ' '.join(ph_seq), ' '.join(ph_dur)])

print(f"已将lab文件还原为CSV文件：{csv_file_path}")
