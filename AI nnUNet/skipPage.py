import os
import numpy as np
import SimpleITK as sitk


images_dir = r"D:\incerc\nou\imagesTr_cropped"  
labels_dir = r"D:\incerc\nou\labelsTr_cropped"   
output_images_dir = r"D:\incerc\nou\imagesTr_global"
output_labels_dir = r"D:\incerc\nou\labelsTr_global"


margin = 5

def main():
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)

    print("1. Analizez mastile")
    
    min_x_list, max_x_list = [], []
    min_y_list, max_y_list = [], []
    min_z_list, max_z_list = [], []

    mask_files = [f for f in os.listdir(labels_dir) if f.endswith(".nii.gz")]

    if not mask_files:
        print("Eroare: Nu am găsit masti în folder!")
        return


    for mask_name in mask_files:
        mask_path = os.path.join(labels_dir, mask_name)
        mask = sitk.ReadImage(mask_path)
        arr = sitk.GetArrayFromImage(mask)

        if np.max(arr) == 0:
            continue

        z_ind, y_ind, x_ind = np.where(arr > 0)

        min_z_list.append(np.min(z_ind))
        max_z_list.append(np.max(z_ind))
        
        min_y_list.append(np.min(y_ind))
        max_y_list.append(np.max(y_ind))
        
        min_x_list.append(np.min(x_ind))
        max_x_list.append(np.max(x_ind))

    global_z_start = min(min_z_list)
    global_z_end   = max(max_z_list)

    global_y_start = min(min_y_list)
    global_y_end   = max(max_y_list)

    global_x_start = min(min_x_list)
    global_x_end   = max(max_x_list)

    print("-" * 50)
    print(f"Limitele brute gasite:")
    print(f"X: {global_x_start} - {global_x_end}")
    print(f"Y: {global_y_start} - {global_y_end}")
    print(f"Z: {global_z_start} - {global_z_end}")

    final_x_start = max(0, global_x_start - margin)
    final_y_start = max(0, global_y_start - margin)
    final_z_start = max(0, global_z_start - margin)
    

    final_x_end = global_x_end + margin
    final_y_end = global_y_end + margin
    final_z_end = global_z_end + margin

    print(f"Limitele finale cu margine (Ce vom taia):")
    print(f"X: {final_x_start} la {final_x_end}")
    print(f"Y: {final_y_start} la {final_y_end}")
    print(f"Z: {final_z_start} la {final_z_end}")
    print("-" * 50)

    apply_crop_folder(images_dir, output_images_dir, 
                      final_x_start, final_x_end, 
                      final_y_start, final_y_end, 
                      final_z_start, final_z_end)
                      
    apply_crop_folder(labels_dir, output_labels_dir, 
                      final_x_start, final_x_end, 
                      final_y_start, final_y_end, 
                      final_z_start, final_z_end, is_label=True)

def apply_crop_folder(in_dir, out_dir, x1, x2, y1, y2, z1, z2, is_label=False):
    files = [f for f in os.listdir(in_dir) if f.endswith(".nii.gz")]
    print(f"Procesez {len(files)} fișiere din {os.path.basename(in_dir)}...")

    for fname in files:
        path = os.path.join(in_dir, fname)
        img = sitk.ReadImage(path)
        
        size_x, size_y, size_z = img.GetSize()

        cur_x2 = min(x2, size_x)
        cur_y2 = min(y2, size_y)
        cur_z2 = min(z2, size_z)

        size_to_crop_x = cur_x2 - x1
        size_to_crop_y = cur_y2 - y1
        size_to_crop_z = cur_z2 - z1

        if size_to_crop_x <= 0 or size_to_crop_y <= 0 or size_to_crop_z <= 0:
            print(f"SKIP {fname}: Chenarul calculat e în afara imaginii!")
            continue

        roi_filter = sitk.RegionOfInterestImageFilter()
        roi_filter.SetIndex([int(x1), int(y1), int(z1)])
        roi_filter.SetSize([int(size_to_crop_x), int(size_to_crop_y), int(size_to_crop_z)])

        try:
            cropped_img = roi_filter.Execute(img)
            
            sitk.WriteImage(cropped_img, os.path.join(out_dir, fname))
        except Exception as e:
            print(f"Eroare la {fname}: {e}")

    print(f"Gata cu folderul {os.path.basename(in_dir)}.")

if __name__ == "__main__":
    main()