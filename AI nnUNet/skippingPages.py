import os
import SimpleITK as sitk
import numpy as np
import csv
import re

labels_cropped = r"D:\incerc\nou\labelsTr_cropped"
csv_path = r"D:\incerc\nou\slices_info_3axes.csv"

rows = [["case_id", 
         "first_axial", "last_axial",
         "first_coronal", "last_coronal",
         "first_sagittal", "last_sagittal"]]

for mask_file in os.listdir(labels_cropped):
    if not mask_file.endswith(".nii.gz"):
        continue

    mask_path = os.path.join(labels_cropped, mask_file)
    case_id = re.match(r"\d+", mask_file).group(0)

    mask = sitk.ReadImage(mask_path)
    arr = sitk.GetArrayFromImage(mask)

    if np.max(arr) == 0:
        print(f"{case_id}: mask empty")
        continue

    total_x_slices = arr.shape[0]

    nonzero_slices_z = [i for i in range(arr.shape[0]) if np.any(arr[i,:,:] > 0)]
    first_axial = total_x_slices - int(nonzero_slices_z[-1]) - 1
    last_axial = total_x_slices -  int(nonzero_slices_z[0]) - 1

    nonzero_slices_y = np.where(arr.sum(axis=(0,2)) > 0)[0]
    first_coronal = int(nonzero_slices_y[0])
    last_coronal = int(nonzero_slices_y[-1])

    nonzero_slices_x = np.where(arr.sum(axis=(0,1)) > 0)[0]
    first_sagittal = int(nonzero_slices_x[0])
    last_sagittal = int(nonzero_slices_x[-1])

    rows.append([case_id, 
                 first_axial, last_axial,
                 first_coronal, last_coronal,
                 first_sagittal, last_sagittal])

    print(f"{case_id}: Axial [{first_axial}-{last_axial}], "
          f"Coronal [{first_coronal}-{last_coronal}], "
          f"Sagittal [{first_sagittal}-{last_sagittal}]")

with open(csv_path, "w", newline="") as f:
    csv.writer(f).writerows(rows)

print(f"CSV with slices info (3 axes) saved to: {csv_path}")
