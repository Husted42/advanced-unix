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
"""
This class is for functions to make lookup between familiy relationsship easier

"""

class FamilyRelations:
    def __init__(self, data):
        self.data = data

    def build_parents_children_lookup(self, data):

        if data is None:
            data = self.data

        if isinstance(data, dict):
            data = data.values()

        """
        Create dict for easy lookup of a child's parents

        """
        children_parents = {}

        #O(n), where n is persons in data
        for person in self.data:
            parent_cpr = person.get('cpr')

            #O(m), where m is children for each parent
            for child_cpr in person['children']:
                if child_cpr not in children_parents:
                    children_parents[child_cpr] = []

                children_parents[child_cpr].append(parent_cpr)

        return children_parents
    
    def get_parents(self, child_cpr, data):
        """
        A function to look-up parents of a child 
        """

        child_parents = self.build_parents_children_lookup(data)

        return child_parents.get(child_cpr)
    
    def get_parents_pair(self, data):
        """
        A function to get pairs of parents

        """

        child_parents = self.build_parents_children_lookup(data)

        pairs = []
        for child in child_parents:
            parents = child_parents[child]

            #check in case a child only has a single parent
            if len(parents) == 2:
                #Sort to avoid dublicates, runtime O(n log(n))
                pair = sorted([parents[0], parents[1]])

                #only append unique pairs
                if pair not in pairs:
                    pairs.append(pair)

        return pairs
    
