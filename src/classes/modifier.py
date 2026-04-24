# We want to assume that the user is a the repository root when running the program. This will make refrencing files easier.
import sys, os
def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

########## ---------- Imports ---------- ##########
from src.func.utils import get_largest_number

########## ---------- Classes ---------- ##########
'''
    We will use this class whenever we need to add features to the data.
'''
class Modifier:
    def __init__(self, data):
        self.data = data
    
    def q1_add_age(self):
        # Since data was constructed in 2000 it's fair to assumme that all are from 1900's
        for person in self.data:
            cpr = person["cpr"]
            age = 2000 - (1900 + int(cpr[4:6]))
            person["age"] = age

    def q1_add_gender(self):
        for person in self.data:
            cpr = person["cpr"]
            # We can determine the sex based ont the 5th digit of the CPR number
            gender = "Male" if int(cpr[4]) % 2 == 0 else "Female"
            person["gender"] = gender

    def q2_add_fartherhood_year(self):
        for person in self.data:

            # We find the difference between the oldest child an the parents age.
            # Also we implement for both genders and let the filtering hapen in the 
            parent_age = person["age"]
            children_age = []
            for child in person['children']:
                child_age = 2000 - (1900 + int(child[4:6])) 
                
                if parent_age < child_age:
                    raise ValueError("Kid older han parent") 
                
                children_age.append(child_age)
            
            became_parent = None
            if children_age != []:
                oldest_child = get_largest_number(children_age)
                became_parent = parent_age - oldest_child 
            
            if became_parent:
                person['parenthood_start'] = became_parent
            else: 
                person['parenthood_start'] = None