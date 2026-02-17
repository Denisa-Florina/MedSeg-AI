import os
import nibabel as nib
import numpy as np

# Folderul unde sunt mastile
labels_folder = r"D:/incerc/Task001_MyStudy/labelsTr_cropped_final"
files = [f for f in os.listdir(labels_folder) if f.endswith(".nii.gz")]

for f in files:
    path = os.path.join(labels_folder, f)
    
    img = nib.load(path)
    data = img.get_fdata()
    
    # Transforma toate valorile 2 în 1
    data[data == 2] = 1
    
    new_img = nib.Nifti1Image(data.astype(np.uint8), img.affine, img.header)
    nib.save(new_img, path)
    
    print(f"Processed {f}")

print("Toate mastile au fost convertite: 2 -> 1")
