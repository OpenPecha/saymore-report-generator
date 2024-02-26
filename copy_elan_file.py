import os
import shutil
from pathlib import Path

def copy_eaf_files(repo_path, destination_file_path):

    # Check if the source directory exists
    if os.path.exists(repo_path):
        for path in Path(repo_path).rglob('*.eaf'):
            # Copy the file to the destination directory
            shutil.copy(path, destination_file_path)
            # Print a message indicating that the files were copied successfully
            print("eaf file copied successfully.")
            return
        print("no eaf file found")
    else:
        # Print a message indicating that the source directory does not exist
        print("Source directory does not exist.")