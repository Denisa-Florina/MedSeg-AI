import os
import subprocess
import SimpleITK as sitk
import re

base_input = r"D:\45segmentari\segmentari"
task_dir = r"D:\incerc\Task001_MyStudy"
dcm2niix_path = r"D:\dcm2niix_win\dcm2niix.exe"

imagesTr = os.path.join(task_dir, "imagesTr")
labelsTr = os.path.join(task_dir, "labelsTr")
os.makedirs(imagesTr, exist_ok=True)
os.makedirs(labelsTr, exist_ok=True)

mask_dict_path = os.path.join(task_dir, "mask_dict.txt")
mask_dict = {}

def align_mask(mask_img, ref_img):
    """Resample mask to match reference DICOM volume."""
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(ref_img)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    resampler.SetOutputPixelType(sitk.sitkUInt8)

    aligned = resampler.Execute(mask_img)

    aligned.SetOrigin(ref_img.GetOrigin())
    aligned.SetSpacing(ref_img.GetSpacing())
    aligned.SetDirection(ref_img.GetDirection())

    return aligned


for folder_name in os.listdir(base_input):
    case_folder = os.path.join(base_input, folder_name)
    if not os.path.isdir(case_folder):
        continue

    case_id = folder_name.replace(" ", "_")

    print("\n==============================")
    print(" Processing:", case_id)
    print("==============================")

    dicom_dirs = [
        os.path.join(case_folder, d)
        for d in os.listdir(case_folder)
        if os.path.isdir(os.path.join(case_folder, d))
        and any(f.lower().endswith(".dcm") for f in os.listdir(os.path.join(case_folder, d)))
    ]

    if not dicom_dirs:
        print(f"No DICOM folders for {case_id}, skipping...")
        continue

    out_names = []
    for i, dcm_dir in enumerate(dicom_dirs):
        out_name = f"{case_id}_s{i:02d}_0000"
        out_names.append(out_name)
        subprocess.run([
            dcm2niix_path, "-z", "y", "-f", out_name, "-o", imagesTr, dcm_dir
        ], check=True)

    ref_path = os.path.join(imagesTr, out_names[0] + ".nii.gz")
    ref_img = sitk.ReadImage(ref_path)

    masks = [f for f in os.listdir(case_folder) if f.lower().endswith(".nrrd")]
    if not masks:
        print(f"No mask found for {case_id}, skipping mask...")
        continue

    mask_path = os.path.join(case_folder, masks[0])
    mask_img = sitk.ReadImage(mask_path)

    aligned_mask = align_mask(mask_img, ref_img)

    mask_out = os.path.join(labelsTr, f"{case_id}.nii.gz")
    sitk.WriteImage(aligned_mask, mask_out)

    mask_dict[re.match(r"\d+", case_id).group(0)] = mask_out

    print("Saved aligned mask:", mask_out)
    print(" Mask size:", aligned_mask.GetSize())
    print(" Volume size:", ref_img.GetSize())


with open(mask_dict_path, "w") as f:
    for k, v in mask_dict.items():
        f.write(f"{k},{v}\n")

print("\nConversion complete. Mask alignment DONE. mask_dict saved.")
