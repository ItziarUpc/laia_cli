import os
import shutil

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)

def copy_template(template_path: str, target_path: str):
    if os.path.isdir(template_path):
        shutil.copytree(template_path, target_path, dirs_exist_ok=True)
    else:
        shutil.copy2(template_path, target_path)