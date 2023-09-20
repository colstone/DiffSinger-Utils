import os
from praatio import tgio

def convert_textgrid_to_lab(textgrid_path):
    # Load the TextGrid file
    tg = tgio.openTextgrid(textgrid_path)

    # Create output folders for each tier
    output_folder = os.path.dirname(textgrid_path)
    tier_names = tg.tierNameList

    for tier_name in tier_names:
        tier_folder = os.path.join(output_folder, tier_name)
        os.makedirs(tier_folder, exist_ok=True)

        # Get annotations from the tier
        tier = tg.tierDict[tier_name]
        annotations = tier.entryList

        # Create .lab files for each annotation
        for annotation in annotations:
            start, end, label = annotation
            start_htk = int(start * 1e7)
            end_htk = int(end * 1e7)
            lab_content = f"{start_htk} {end_htk} {label}"
            lab_filename = os.path.splitext(os.path.basename(textgrid_path))[0] + ".lab"
            lab_filepath = os.path.join(tier_folder, lab_filename)

            with open(lab_filepath, "a") as lab_file:
                lab_file.write(lab_content + "\n")

def batch_convert_textgrid_to_lab(folder_path):
    textgrid_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".textgrid")]

    for filename in textgrid_files:
        textgrid_path = os.path.join(folder_path, filename)
        convert_textgrid_to_lab(textgrid_path)
        print(f"转换完成：{textgrid_path}")

if __name__ == "__main__":
    batch_mode = input("是否开启批量转换模式？（输入'y'开启）：")
    
    if batch_mode == "y":
        folder_path = input("请输入文件夹路径：")
        batch_convert_textgrid_to_lab(folder_path)
        print("批量转换完成！")
    else:
        textgrid_path = input("请输入TextGrid文件的路径：")
        convert_textgrid_to_lab(textgrid_path)
        print("转换完成！")
