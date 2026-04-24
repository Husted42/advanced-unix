import os
from pathlib import Path
import sys

'''
    This function moves the user to the root of repo, given that they are calling in from the repo
'''
def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    # check if found then switch
    if src_index != -1:
        src_path = current_dir[:src_index + len(root)]
        os.chdir(src_path)
        sys.path.append(str(src_path))