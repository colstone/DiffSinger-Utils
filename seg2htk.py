# seg转htk

import os
import glob

def convert_to_lab(seg_lines):
    lab_content = []
    for line in seg_lines:
        if line.startswith(('REVISED', 'nPhonemes', 'articulationsAreStationaries', 'phoneme', '===')):
            continue
        parts = line.split()
        if len(parts) == 3:
            phoneme = parts[0]
            begin_time = float(parts[1]) * 10000000  # Convert to 100 nanoseconds unit
            end_time = float(parts[2]) * 10000000  # Convert to 100 nanoseconds unit
            lab_content.append(f"{int(begin_time)} {int(end_time)} {phoneme}")
    return lab_content

def process_file(seg_file_path):
    with open(seg_file_path, 'r', encoding='utf-8') as file:
        seg_content = file.readlines()
    lab_content = convert_to_lab(seg_content)
    lab_file_path = seg_file_path.replace('.seg', '.lab')
    with open(lab_file_path, 'w', encoding='utf-8') as file:
        for line in lab_content:
            file.write(line + '\n')
    print(f"Processed: {lab_file_path}")

def main():
    batch_mode = input("是否开启批处理模式？(y/n): ").strip().lower()
    if batch_mode == 'y':
        folder_path = input("请输入.seg文件所在的文件夹路径: ").strip()
        for seg_file_path in glob.glob(os.path.join(folder_path, '*.seg')):
            process_file(seg_file_path)
    else:
        seg_file_path = input("请输入.seg文件的路径: ").strip()
        process_file(seg_file_path)

if __name__ == "__main__":
    main()
