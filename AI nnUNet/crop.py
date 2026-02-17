import os
import SimpleITK as sitk
import re
import csv
import numpy as np 

task_dir = r"D:\incerc\Task001_MyStudy"
imagesTr = os.path.join(task_dir, "imagesTr")
labelsTr = os.path.join(task_dir, "labelsTr")
imagesTr_cropped = os.path.join(task_dir, "imagesTr_cropped_final")
labelsTr_cropped = os.path.join(task_dir, "labelsTr_cropped_final")

# Safe zone
PADDING_PIXELS = 25 

os.makedirs(imagesTr_cropped, exist_ok=True)
os.makedirs(labelsTr_cropped, exist_ok=True)

bbox_csv = os.path.join(task_dir, "bounding_boxes.csv")
bbox_dict = {}

def resample_mask_to_image(mask, image):
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(image)
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    return resampler.Execute(mask)


def crop_safe(img, bbox, padding):
    """ Cropează imaginea/masca adăugând padding. """
    sx, sy, sz = img.GetSize()
    x_min, x_max, y_min, y_max, z_min, z_max = bbox

    x_start = max(0, x_min - padding)
    x_end = min(sx - 1, x_max + padding)
    y_start = max(0, y_min - padding)
    y_end = min(sy - 1, y_max + padding)
    z_start = max(0, z_min - padding)
    z_end = min(sz - 1, z_max + padding)

    if x_start > x_end: x_start, x_end = x_end, x_start 
    if y_start > y_end: y_start, y_end = y_end, y_start
    if z_start > z_end: z_start, z_end = z_end, z_start
    
    start = [x_start, y_start, z_start]
    size = [
        max(1, x_end - x_start + 1),
        max(1, y_end - y_start + 1),
        max(1, z_end - z_start + 1),
    ]
    
    if any(s <= 0 for s in size):
         raise ValueError(f"Dimensiunea cropului invalidă: {size}")
         
    return sitk.RegionOfInterest(img, size, start)


with open(bbox_csv) as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        case_id = row[0].strip()
        if case_id == "GLOBAL":
            continue
        try:
            bbox = tuple(map(int, row[1:]))
            bbox_dict[case_id] = bbox
        except ValueError:
            print(f"[WARN] Failed to load BBox for {case_id}")


def extract_prefix(fname):
    m = re.match(r"(\d+)", fname)
    return m.group(1) if m else None

def find_mask(prefix):
    for f in os.listdir(labelsTr):
        if f.startswith(prefix):
            return os.path.join(labelsTr, f)
    return None

print("=== CROPPING INDIVIDUAL CU CONTEXT (Versiune Robustă) ===")
print(f"Padding: {PADDING_PIXELS} pixeli. Foldere output: {os.path.basename(imagesTr_cropped)}")

for img_file in sorted(os.listdir(imagesTr)):
    if not img_file.endswith(".nii.gz"):
        continue

    prefix = extract_prefix(img_file)

    if prefix not in bbox_dict:
        print(f"[WARN] No bounding box for {img_file}. Skipping.")
        continue

    try:
        bbox = bbox_dict[prefix]
        img_path = os.path.join(imagesTr, img_file)
        mask_path = find_mask(prefix)

        if mask_path is None:
            print(f"[ERROR] No mask found for prefix {prefix}. Skipping.")
            continue

        mask_name = os.path.basename(mask_path)


        img = sitk.ReadImage(img_path)
        mask = sitk.ReadImage(mask_path, sitk.sitkUInt8) 
        mask_resampled = resample_mask_to_image(mask, img)
        img_c = crop_safe(img, bbox, PADDING_PIXELS)
        mask_c = crop_safe(mask_resampled, bbox, PADDING_PIXELS) 
        
        if np.max(sitk.GetArrayFromImage(mask_c)) == 0:
            print(f"[WARN] Segmentare pierdută pentru {prefix} după crop. BBox ar putea fi prea strâns.")
        
        sitk.WriteImage(img_c, os.path.join(imagesTr_cropped, img_file))
        sitk.WriteImage(mask_c, os.path.join(labelsTr_cropped, mask_name))

        print(f"[OK] Cropped case {prefix}: saved {img_file} & {mask_name}")

    except Exception as e:
        print(f"[FAIL] Error processing {img_file}: {e}")
        continue
        
print("=== DONE: All cases cropped individually with context ===")