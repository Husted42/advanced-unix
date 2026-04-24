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

'''
    Get he largest value of a list
'''
def get_largest_number(lst: list):
    if not lst:
        raise ValueError("List is empty")

    largest = lst[0]
    for num in lst:
        if num > largest:
            largest = num

    return largest

def get_min(lst: list):
    if not lst:
        raise ValueError("get_min() arg is an empty list")

    minimum = lst[0]
    for x in lst:
        if x < minimum:
            minimum = x
    return minimum


def get_max(lst: list):
    if not lst:
        raise ValueError("get_max() arg is an empty list")

    maximum = lst[0]
    for x in lst:
        if x > maximum:
            maximum = x
    return maximum