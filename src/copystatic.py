import os
import shutil

def clear_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def copy_files_recursive(source, destination):
    for file in os.listdir(source):
        source_path = os.path.join(source, file)
        dest_path = os.path.join(destination, file)
        print(f" * {source_path} -> {dest_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_files_recursive(source_path, dest_path)
            