# generate_csv.py
import os
import SimpleITK as sitk
import csv
import numpy as np

task_dir = r"D:\incerc\Task001_MyStudy"
labelsTr = os.path.join(task_dir, "labelsTr")
SAFE_BORDER = 10
csv_path = os.path.join(task_dir, "bounding_boxes.csv")
mask_dict_path = os.path.join(task_dir, "mask_dict.txt")


mask_dict = {}
with open(mask_dict_path) as f:
    for line in f:
        k,v = line.strip().split(",")
        mask_dict[k] = v

csv_rows = [["case_id","x_min","x_max","y_min","y_max","z_min","z_max"]]

x_mins, x_maxs, y_mins, y_maxs, z_mins, z_maxs = [], [], [], [], [], []

for case_prefix, mask_file in mask_dict.items():
    mask = sitk.ReadImage(mask_file)
    arr = sitk.GetArrayFromImage(mask)
    #print(np.unique(arr))
    coords = (arr > 0).nonzero()
    if len(coords[0]) == 0:
        print(f"{case_prefix}: empty mask")
        continue
    z_min, z_max = int(coords[0].min()), int(coords[0].max())
    y_min, y_max = int(coords[1].min()), int(coords[1].max())
    x_min, x_max = int(coords[2].min()), int(coords[2].max())

    x_mins.append(x_min); x_maxs.append(x_max)
    y_mins.append(y_min); y_maxs.append(y_max)
    z_mins.append(z_min); z_maxs.append(z_max)

    csv_rows.append([case_prefix, x_min, x_max, y_min, y_max, z_min, z_max])

gx_min, gx_max = min(x_mins)-SAFE_BORDER, max(x_maxs)+SAFE_BORDER
gy_min, gy_max = min(y_mins)-SAFE_BORDER, max(y_maxs)+SAFE_BORDER
gz_min, gz_max = min(z_mins)-SAFE_BORDER, max(z_maxs)+SAFE_BORDER
global_bbox = (gx_min, gx_max, gy_min, gy_max, gz_min, gz_max)
csv_rows.append(["GLOBAL", gx_min, gx_max, gy_min, gy_max, gz_min, gz_max])

with open(csv_path, "w", newline="") as f:
    csv.writer(f).writerows(csv_rows)

print(f"Bounding boxes saved to CSV: {csv_path}")
