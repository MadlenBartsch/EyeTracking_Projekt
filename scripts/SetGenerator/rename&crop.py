import os
from PIL import Image

# this function takes a folder path and names the jpg images in it after the folder name incrementally (e.g.: name_001)
# it also crops the images to a format of 512x512 pixels

def rename_and_crop_images(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg'))]
    files.sort()
    folder_name = os.path.basename(os.path.normpath(folder_path))

    for idx, file_name in enumerate(files, start=1):
        file_path = os.path.join(folder_path, file_name)
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                min_dim = min(width, height)
                left = (width - min_dim) // 2
                top = (height - min_dim) // 2
                right = left + min_dim
                bottom = top + min_dim
                img_cropped = img.crop((left, top, right, bottom))

                img_resized = img_cropped.resize((512, 512), Image.Resampling.LANCZOS)

                new_file_name = f"{folder_name}_{idx:03}.png"
                new_file_path = os.path.join(folder_path, new_file_name)
                img_resized.save(new_file_path)

                if file_name != new_file_name:
                    os.remove(file_path)

                print(f"Processed and saved: {new_file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    folder_path = input("Folder path: ").strip()
    rename_and_crop_images(folder_path)