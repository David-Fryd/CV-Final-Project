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

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_files.sort()

    for index, image_file in enumerate(image_files):
        src_path = os.path.join(input_dir, image_file)
        if index % 2 == 0:
            dst_path = os.path.join(output_dir1, image_file)
        else:
            dst_path = os.path.join(output_dir2, image_file)
        shutil.copy(src_path, dst_path)
        print(f"Copied '{src_path}' to '{dst_path}'")

if __name__ == "__main__":
    input_directory = "path/to/input_directory"
    output_directory1 = "path/to/output_directory1"
    output_directory2 = "path/to/output_directory2"

    split_images(input_directory, output_directory1, output_directory2)