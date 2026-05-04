# We want to assume that the user is a the repository root when running the program. This will make refrencing files easier.
import sys, os
def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

########## ---------- Imports ---------- ##########
from src.func.utils import get_max
from src.func.utils import get_min

from src.classes.modifier import Modifier
from src.classes.familyrelations import FamilyRelations


class Analyzer:
    def __init__(self, data):
        self.data = data
        
    def q1_value_distribution(self, column_name='age', data = None, bin_size=10):
        age_bins = {}

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()

        for person in data:
            age = person.get(column_name)

            if age is None or age < 0:
                continue

            # lower gives the bin index by dividing with binsize
            # 65 // 10 = 6, which means the bin is 60-70
            lower = (age // bin_size) * bin_size
            upper = lower + bin_size
            bin_label = f"{lower}-{upper}"

            age_bins[bin_label] = age_bins.get(bin_label, 0) + 1

        return age_bins

    def q1_gender_distribution(self):
        gender_counts = {}

        for person in self.data:
            gender = person.get("gender")

            if not gender:
                continue

            gender = gender.lower()
            gender_counts[gender] = gender_counts.get(gender, 0) + 1

        return gender_counts
    

    # We make the implementation for an arbitrary filter
    # we need thils later
    def q2_value_summary(self, data, val_col: str):
        values = []

        # If data is a dict, iterate over its values
        if isinstance(data, dict):
            data = data.values()

        for person in data:
            value = person.get(val_col)

            if value is not None:
                values.append(value)

        if not values:
            return None

        avg = sum(values) / len(values)
        minimum = get_min(values)
        maximum = get_max(values)
        count = len(values)

        return {
            "max": maximum,
            "min": minimum,
            "avg": avg,
            "count": count
        }
    
    def q6_parenthood_distribution(self, data = None):

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()

        
        men_total = 0
        women_total = 0

        women_no_children = 0
        men_no_children = 0

        #O(n), where n is number of persons in data
        for person in data:
            #gather cpr to differentiate between women/men
            cpr = person['cpr']
            last_degit = cpr[-1]

            #get is runtime O(1) on average
            has_children = person.get('children')
            
            #count total and if has no children for men and women
            if int(last_degit )% 2 == 1:
                men_total += 1

                if not has_children:
                    men_no_children += 1

            else:
                women_total += 1

                if not has_children:
                    women_no_children += 1
        
        men_percentages = 0
        women_percentages = 0
        total_percentages = 0

        #Check to avoid zer division, otherwise calculate percentage
        if men_total > 0:                       
            men_percentages = (men_no_children / men_total) * 100 

        if women_total > 0:                      
            women_percentages = (women_no_children / women_total) * 100

        if  women_total or men_total > 0:
            total_percentages = ((women_no_children + men_no_children) / (men_total + women_total )) * 100
        
        return {
            "Percentages of men without children": men_percentages,
            "Percentages of women without children": women_percentages,
            "Total amount of people without children": total_percentages
        }


    def q7_average_age_difference(self, data = None, pairs = None): 

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()


        total_pairs = len(pairs)
        total_difference = 0

        #runtime O(n), where n pair of parents
        for parent in pairs:
            parent1 = parent[0]
            parent2 = parent[1]

            #runtime O(m), where m is people in parents
            for person in data:

                if person.get('cpr') == parent1:
                    age1 = person.get('age')

                if person.get('cpr') == parent2:
                    age2 = person.get('age')

            if age1 is not None and age2 is not None:
                age_difference = abs(age1 - age2)

                total_difference += age_difference
                         
            
        if total_pairs == 0:
            average_difference = 0
        else: 
            average_difference = total_difference / total_pairs

        return {
            "Average age difference between parents is": average_difference
        }



    def q8_grandparents_count(self, data):

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()  

        familyrelations = FamilyRelations(data)

        total_people_has_grandparent = 0
        total = len(data)

        for person in data:
            cpr = person.get('cpr')

            grandparents = familyrelations.get_grandparents(cpr, data)

            if grandparents:
                total_people_has_grandparent += 1

        if total == 0.0:
            percentage_has_grandparents = 0.0
        else:
            percentage_has_grandparents = (total_people_has_grandparent / total)  * 100   
        
        return {
            "Amount of people who has a grandparent": total_people_has_grandparent,
            "Percentage of people who has a grandparent": percentage_has_grandparents
        }


