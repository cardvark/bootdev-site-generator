import os
import shutil


def generate_site():
    source_path = "./static/"
    # os.path.join("working_dir", "static/")
    # destination_path = os.path.join(working_dir, "public/")
    destination_path = "./public/"

    abs_working_path = os.path.abspath(source_path)
    abs_dest_path = os.path.abspath(destination_path)
    
    # print(abs_source_path)
    # print(source_path)
    # print(destination_path)

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
        # print(f"Found destination: {destination_path}")
    
    os.mkdir(destination_path)

    copy_to_dest(abs_working_path, abs_dest_path)


def copy_to_dest(working_dir, dest_path):
    print(f"Starting copy process. Current working dir: {working_dir}")

    for path in os.listdir(working_dir):
        full_working_path = os.path.join(working_dir, path)
        full_dest_path = os.path.join(dest_path, path)

        if os.path.isfile(full_working_path):
            print(f"This is a file: {path}")
            print(f"Copying file to destination: {full_dest_path}")
            shutil.copy(full_working_path, full_dest_path)
        elif os.path.isdir(full_working_path):
            print(f"This is a folder: {full_working_path}")
            print(f"Running copy_to_dest with working dir: {full_working_path} and destination path: {full_dest_path}")
            os.mkdir(full_dest_path)
            copy_to_dest(full_working_path, full_dest_path)


if __name__ == "__main__":
    generate_site()