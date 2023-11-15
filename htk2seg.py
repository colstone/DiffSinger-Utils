import os
import glob

def convert_to_seg(lab_lines):
    seg_content = ['REVISED!\n', 'nPhonemes {}\n'.format(len(lab_lines)), 'articulationsAreStationaries = 0\n',
                   'phoneme\t\tBeginTime\t\tEndTime\n', '===================================================\n']
    for line in lab_lines:
        parts = line.split()
        if len(parts) == 3:
            begin_time = int(parts[0]) / 10000000  # Convert from 100 nanoseconds to seconds
            end_time = int(parts[1]) / 10000000  # Convert from 100 nanoseconds to seconds
            phoneme = parts[2]
            seg_content.append('{}\t\t{:.6f}\t\t{:.6f}\n'.format(phoneme, begin_time, end_time))
    return seg_content

def process_file(lab_file_path):
    with open(lab_file_path, 'r', encoding='utf-8') as file:
        lab_content = file.readlines()
    seg_content = convert_to_seg(lab_content)
    seg_file_path = lab_file_path.replace('.lab', '.seg')
    with open(seg_file_path, 'w', encoding='utf-8') as file:
        for line in seg_content:
            file.write(line)
    print(f"Processed: {seg_file_path}")

def main():
    batch_mode = input("是否开启批处理模式？(y/n): ").strip().lower()
    if batch_mode == 'y':
        folder_path = input("请输入.lab文件所在的文件夹路径: ").strip()
        for lab_file_path in glob.glob(os.path.join(folder_path, '*.lab')):
            process_file(lab_file_path)
    else:
        lab_file_path = input("请输入.lab文件的路径: ").strip()
        process_file(lab_file_path)

if __name__ == "__main__":
    main()
