import os
from pypinyin import lazy_pinyin
from tqdm import tqdm

def convert_to_pinyin(text):
    pinyin_list = lazy_pinyin(text)
    pinyin_without_tone = [p[:-1] if p[-1].isdigit() else p for p in pinyin_list]
    pinyin_without_special = [p for p in pinyin_without_tone if p.isalpha()]
    return ''.join(pinyin_without_special)

def process_directory(directory_path):
    if not os.path.exists(directory_path):
        print("The provided directory path does not exist.")
        return
    
    for root, dirs, files in os.walk(directory_path):
        for file in tqdm(files, desc="Converting files"):
            if file.lower().endswith('.wav'):
                original_path = os.path.join(root, file)
                pinyin_filename = convert_to_pinyin(file.split('.')[0])
                new_path = os.path.join(root, pinyin_filename + '.wav')
                os.rename(original_path, new_path)

if __name__ == "__main__":
    input_path = input("Enter the directory path: ")
    process_directory(input_path)
    print("Conversion complete.")
