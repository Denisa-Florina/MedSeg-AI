import os
import shutil
import re

imagesTr = r"D:\incerc\Task001_MyStudy\imagesTr_cropped_final"   # folderul inițial
imagesTr_fixed = r"D:\incerc\Task001_MyStudy\imagesTr_final"  # folder nou

os.makedirs(imagesTr_fixed, exist_ok=True)

for f in os.listdir(imagesTr):
    if not f.endswith(".nii.gz"):
        continue

    # eliminam sufixul _sXX_XXXX
    new_name = re.sub(r'_s\d{2}_\d{4}', '_0000', f)

    src_path = os.path.join(imagesTr, f)
    dst_path = os.path.join(imagesTr_fixed, new_name)

    shutil.copy(src_path, dst_path)
    print(f"Copied: {f} → {new_name}")

print("All images copied and renamed to imagesTr_fixed.")
