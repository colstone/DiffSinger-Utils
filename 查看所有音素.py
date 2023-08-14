import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', type=str, required=True, help='path to the folder containing lab files')
    parser.add_argument('--find_phoneme', type=str, help='find the lab file containing the specified phoneme')
    args = parser.parse_args()

    lab_file_paths = [os.path.join(args.folder_path, f) for f in os.listdir(args.folder_path) if f.endswith('.lab')]

    if args.find_phoneme:
        found_phoneme = False
        for lab_file_path in lab_file_paths:
            with open(lab_file_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    phoneme = line.split()[2]
                    if phoneme == args.find_phoneme:
                        print(f'音素：{args.find_phoneme} 位于 {lab_file_path} 第 {i+2} 行')
                        found_phoneme = True
                        break
                if found_phoneme:
                    break
        if not found_phoneme:
            print(f'未能在指定文件夹内所有lab文件里面找到该音素！')
    else:
        phonemes = set()
        for lab_file_path in lab_file_paths:
            with open(lab_file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    phoneme = line.split()[2]
                    if phoneme not in phonemes:
                        phonemes.add(phoneme)

        phonemes = sorted(list(phonemes))
        phonemes_per_line = 5  # Define the number of phonemes to display per line
        current_line_phonemes = []

        for phoneme in phonemes:
            current_line_phonemes.append(phoneme)
            if len(current_line_phonemes) == phonemes_per_line:
                print("\t".join(current_line_phonemes))
                current_line_phonemes = []

        if current_line_phonemes:
            print(" ".join(current_line_phonemes))
