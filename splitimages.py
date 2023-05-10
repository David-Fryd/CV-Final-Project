import os
import shutil

def split_images(input_dir, output_dir1, output_dir2):
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    if not os.path.exists(output_dir1):
        os.makedirs(output_dir1)

    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif'))]
    image_files = sorted(image_files, key=lambda x: int(x.split("_")[1]))

    for index, image_file in enumerate(image_files):
        src_path = os.path.join(input_dir, image_file)
        if index % 2 == 0:
            dst_path = os.path.join(output_dir1, image_file)
        else:
            dst_path = os.path.join(output_dir2, image_file)
        shutil.copy(src_path, dst_path)

if __name__ == "__main__":
    input_directory = "us-dataset"
    output_directory1 = "test/wildfire"
    output_directory2 = "train/wildfire"

    split_images(input_directory, output_directory1, output_directory2)