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
        self.familyrelations = FamilyRelations(data)
        
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

        total_people_has_grandparent = 0
        total = len(data)

        
        #O(n) where n is persons in data for loop
        for person in data:
            cpr = person.get('cpr')

            #O(1)
            grandparents = self.familyrelations.get_grandparents(cpr, data)

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
    
    def q9_comparelists(self, list1, list2):

        """
        Helper function to find common elements in list
        """

        for value in list1:
            if value in list2:
                return True
        return False

    def q9_cousins(self, data):

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()  

        #total runtime is O(n^2), as O(n^2) + O(n^2) ≈ O(n^2)

        parents_lookup = {}
        grandparents_lookup = {}

        #compute dicts of grandparents / parents for lookup

        #O(n)
        for person in data:
            cpr = person.get('cpr')

            parents_lookup[cpr] = self.familyrelations.get_parents(cpr, data)
            grandparents_lookup[cpr] = self.familyrelations.get_grandparents(cpr, data)

        cousins_pair = []

        #compare every person to every other person
        #O(n^2), where n is number of person in data
        for i in range(len(data)):
            for j in range(len(data)):

                #avoids making a person its own cousin
                if i == j:
                    continue

                #find cpr to compare
                cpr1 = data[i].get('cpr')
                cpr2 = data[j].get('cpr')

                #get their parents
                parents1 = parents_lookup[cpr1]
                parents2 = parents_lookup[cpr2]

                #get their grandparents
                grandparents1 = grandparents_lookup[cpr1]
                grandparents2 = grandparents_lookup[cpr2]

                #check if they share grandparents and/or parents,
                # O(1), constant time
                share_parent = self.q9_comparelists(parents1, parents2)
                share_grandparent = self.q9_comparelists(grandparents1, grandparents2)

                #check if they are parents
                if share_grandparent and not share_parent:
                    cousins_pair.append((cpr1, cpr2))

        return cousins_pair
        
    def q9_cousins_calculations(self, data):

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()   

        cousins_pair = self.q9_cousins(data)

        #find out how many people has a cousin
        people_who_has_cousins = set()

        for pair in cousins_pair:
            people_who_has_cousins.add(pair[0])

        #avoid zero divion
        if len(people_who_has_cousins) == 0:
            average_cousin_amount = 0

        #average must be count of cousin pairs divided between people who has a cousins
        else:
            average_cousin_amount = len(cousins_pair) / len(people_who_has_cousins)

        return {
            "Number of people in the database who has a cousin": len(people_who_has_cousins),
            "Average number of cousins, for people who has a cousin": average_cousin_amount,
            }
    
    def q10_get_precise_age(self, cpr):
        
        day = int(cpr[0:2])
        month = int(cpr[2:4])
        year = int(cpr[4:6])

        #We assume that everyone is born before 2000s
        year = 1900 + year

        return (year, month, day)


    def q10_firstborn_gender(self, data):

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()  

        eldest_daugther = 0
        eldest_son = 0 
        eldest_children = 0

        #get children of every person
        # O(n), where n is length of data
        for person in data:
            children = person.get('children', [])

            if not children:
                continue

            eldest_child = None
            eldest_age = (-1,-1,-1)

            #check age of siblings, find eldest
            #O(m), where m is length of children. Could argue for constant time.
            for child in children:
      
                #get age tuble to compare    
                child_age = self.q10_get_precise_age(child)
                
                #find eldest
                if child_age > eldest_age:
                    eldest_child = child_age
                    eldest_child = child

                #find gender
                last_digit = int(eldest_child[-1])
                
                if last_digit % 2 == 0:
                    eldest_daugther += 1
                else: 
                    eldest_son += 1

                eldest_children += 1

        #calculate percentages
        if eldest_children == 0:
            percentage_eldest_daugters = 0
            percentage_eldest_sons = 0
        else:
            percentage_eldest_daugters = (eldest_daugther / eldest_children) * 100 
            percentage_eldest_sons = (eldest_son / eldest_children) * 100 
        
        return {'The percentage of eldest children who are daugthers is': percentage_eldest_daugters,
                'The percentage of eldest children who are sons is': percentage_eldest_sons}

    
    def q11_has_child_with_more_than_one(self, data):

        # Check if external data was specified, if not use self.
        if data == None: data = self.data

        # Allow for passing a dict
        if isinstance(data, dict):
            data = data.values()

        #this list will only contain unique pairs
        pairs = self.familyrelations.get_parents_pair(data)
        

        parent_to_partners = {}

        #flattend pair
        ##O(n), where n is length of pairs
        for pair in pairs:
            parent1 = pair[0]
            parent2 = pair[1]

            #add parent to dict as key
            if parent1 not in parent_to_partners:
                parent_to_partners[parent1] = []

            if parent2 not in parent_to_partners:
                parent_to_partners[parent2] = []
            
            #add partner to parent as value
            if parent2 not in parent_to_partners[parent1]:
                parent_to_partners[parent1].append(parent2)
            
            if parent1 not in parent_to_partners[parent2]:
                parent_to_partners[parent2].append(parent1)
            
        more_than_one_partner = 0
        
        #check for each parent, if more than one partner
        #O(n*2), where n is length of pairs
        for parent in parent_to_partners:
            if len(parent_to_partners[parent]) > 1:
                more_than_one_partner +=1 

        total_parents = len(parent_to_partners) 

        if total_parents == 0:
            percentage_has_child_with_more_than_one = 0
        else:
            percentage_has_child_with_more_than_one = (more_than_one_partner / total_parents) * 100


        return {'Percentage of parents who have a child with more than one': percentage_has_child_with_more_than_one}
    
 #   def what_is_tallness(self, data):
 #   def q12_do_tall_people_marry_each_other(self, data):



        


    def q14_parent_bmi_couple_distribution(self, data=None):
        """
        Counts parent-pair BMI combinations:
        Fat/Fat, Fat/Normal, Fat/Slim, Normal/Normal, Normal/Slim, Slim/Slim.
        """

        if data is None:
            data = self.data

        if isinstance(data, dict):
            people = data
            people_list = list(data.values())
        else:
            people_list = data
            people = {person.get("cpr"): person for person in data}

        familyrelations = FamilyRelations(people_list)

        couple_counts = {
            "Fat/Fat": 0,
            "Fat/Normal": 0,
            "Fat/Slim": 0,
            "Normal/Normal": 0,
            "Normal/Slim": 0,
            "Slim/Slim": 0
        }

        seen_parent_pairs = set()

        for child in people_list:
            child_cpr = child.get("cpr")
            parents = familyrelations.get_parents(child_cpr, people_list)

            if len(parents) != 2:
                continue

            parent_pair = tuple(sorted(parents))

            if parent_pair in seen_parent_pairs:
                continue

            seen_parent_pairs.add(parent_pair)

            parent1 = people.get(parents[0])
            parent2 = people.get(parents[1])

            if parent1 is None or parent2 is None:
                continue

            bmi1 = parent1.get("bmi_category")
            bmi2 = parent2.get("bmi_category")

            if bmi1 is None or bmi2 is None:
                continue

            # Sort so Fat/Normal and Normal/Fat are counted together
            pair = sorted([bmi1, bmi2])

            if pair == ["Fat", "Fat"]:
                couple_counts["Fat/Fat"] += 1
            elif pair == ["Fat", "Normal"]:
                couple_counts["Fat/Normal"] += 1
            elif pair == ["Fat", "Slim"]:
                couple_counts["Fat/Slim"] += 1
            elif pair == ["Normal", "Normal"]:
                couple_counts["Normal/Normal"] += 1
            elif pair == ["Normal", "Slim"]:
                couple_counts["Normal/Slim"] += 1
            elif pair == ["Slim", "Slim"]:
                couple_counts["Slim/Slim"] += 1

        total_parent_pairs = sum(couple_counts.values())

        couple_percentages = {}

        for couple_type, count in couple_counts.items():
            if total_parent_pairs == 0:
                couple_percentages[couple_type] = 0
            else:
                couple_percentages[couple_type] = (count / total_parent_pairs) * 100

        return {
            "Total parent pairs": total_parent_pairs,
            "Couple counts": couple_counts,
            "Couple percentages": couple_percentages
        }

    def q15_abo(self, blood_type):
        """Remove Rh factor: A+ -> A, O- -> O."""
        # O(1), since blood type strings have constant length
        if blood_type is None:
            return None
        return blood_type.replace("+", "").replace("-", "")


    def q15_can_parents_have_child(self, child_blood, parent1_blood, parent2_blood):
        """
        Checks ABO inheritance using the Wikipedia phenotype table.
        Ignores Rh factor (+/-).
        """
        # O(1), fixed number of blood type checks

        child = self.q15_abo(child_blood)        
        p1 = self.q15_abo(parent1_blood)         
        p2 = self.q15_abo(parent2_blood)         

        parent_pair = frozenset([p1, p2])        

        allowed_parent_pairs = {
            "O": {
                frozenset(["O", "O"]),
                frozenset(["O", "A"]),
                frozenset(["O", "B"]),
                frozenset(["A", "A"]),
                frozenset(["A", "B"]),
                frozenset(["B", "B"]),
            },
            "A": {
                frozenset(["O", "A"]),
                frozenset(["O", "AB"]),
                frozenset(["A", "A"]),
                frozenset(["A", "B"]),
                frozenset(["A", "AB"]),
                frozenset(["B", "AB"]),
                frozenset(["AB", "AB"]),
            },
            "B": {
                frozenset(["O", "B"]),
                frozenset(["O", "AB"]),
                frozenset(["A", "B"]),
                frozenset(["A", "AB"]),
                frozenset(["B", "B"]),
                frozenset(["B", "AB"]),
                frozenset(["AB", "AB"]),
            },
            "AB": {
                frozenset(["A", "B"]),
                frozenset(["A", "AB"]),
                frozenset(["B", "AB"]),
                frozenset(["AB", "AB"]),
            }
        }

        return parent_pair in allowed_parent_pairs[child]   # O(1)


    def q15_impossible_parent_child_bloodtypes(self, data=None):
        """
        Go through everyone in the database and check if their parents
        are a possible blood type match.

        Returns a dict of children where at least one listed parent
        cannot be the true biological parent.
        """

        if data is None:
            data = self.data

        # O(n), where n is the number of people
        if isinstance(data, dict):
            people = data
            people_list = data.values()
        else:
            people_list = data
            people = {person.get("cpr"): person for person in data}   

        familyrelations = FamilyRelations(people_list)                

        impossible_cases = {}

        # O(n), loops through every person once
        for child in people_list:
            child_cpr = child.get("cpr")                              
            child_blood = child.get("blood_type")                     

            parents = familyrelations.get_parents(child_cpr, people_list) # O(n)

            # O(1)
            if len(parents) != 2:
                continue

            parent1 = people.get(parents[0])                           
            parent2 = people.get(parents[1])                           

            if parent1 is None or parent2 is None:                     
                continue

            parent1_blood = parent1.get("blood_type")                  
            parent2_blood = parent2.get("blood_type")                  

            if not child_blood or not parent1_blood or not parent2_blood: 
                continue

            possible = self.q15_can_parents_have_child(
                child_blood,
                parent1_blood,
                parent2_blood
            )                                                          

            if not possible:                                           
                impossible_cases[child_cpr] = {
                    "child_blood_type": child_blood,
                    "parent1_cpr": parent1.get("cpr"),
                    "parent1_blood_type": parent1_blood,
                    "parent2_cpr": parent2.get("cpr"),
                    "parent2_blood_type": parent2_blood,
                }                                                      

        return impossible_cases


    def q16_can_donate_blood(self, person1, person2):
        # O(1), because the compatibility table has a fixed size

        compatibility = {
            "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
            "O+": ["O+", "A+", "B+", "AB+"],
            "A-": ["A-", "A+", "AB-", "AB+"],
            "A+": ["A+", "AB+"],
            "B-": ["B-", "B+", "AB-", "AB+"],
            "B+": ["B+", "AB+"],
            "AB-": ["AB-", "AB+"],
            "AB+": ["AB+"]
        }

        blood1 = person1.get('blood_type')                             
        blood2 = person2.get('blood_type')                             

        if not blood1 or not blood2:                                    
            return {
                "person1_can_donate_to_person2": False,
                "person2_can_donate_to_person1": False,
                "error": "Missing blood type information"
            }

        can_1_to_2 = blood2 in compatibility.get(blood1, [])            
        can_2_to_1 = blood1 in compatibility.get(blood2, [])            

        return {
            "person1_can_donate_to_person2": can_1_to_2,
            "person2_can_donate_to_person1": can_2_to_1
        }

    def q16_fathers_can_donate_to_children(self, data=None):
        """
        Checks whether each father can donate blood to each of his children.

        Returns a dict containing:
        - father CPR
        - father blood type
        - child/son CPR
        - child/son blood type
        - whether donation is possible
        """

        if data is None:
            data = self.data

        if isinstance(data, dict):
            people = data
            people_list = list(data.values())
        else:
            people_list = data
            people = {person.get("cpr"): person for person in data}

        familyrelations = FamilyRelations(people_list)

        results = {}

        # O(n), where n is number of people
        for child in people_list:
            child_cpr = child.get("cpr")
            child_blood = child.get("blood_type")

            if not child_cpr or not child_blood:
                continue

            father_cpr = familyrelations.get_father(child_cpr, people_list)

            if father_cpr is None:
                continue

            father = people.get(father_cpr)

            if father is None:
                continue

            father_blood = father.get("blood_type")

            if not father_blood:
                continue

            donation_result = self.q16_can_donate_blood(father, child)

            results[child_cpr] = {
                "father_cpr": father_cpr,
                "father_blood_type": father_blood,
                "son_cpr": child_cpr,
                "son_blood_type": child_blood,
                "father_can_donate_to_son": donation_result["person1_can_donate_to_person2"]
            }

        return results
    

    def q17_grandparents_can_donate_to_children(self, data=None):
        if data is None:
            data = self.data

        if isinstance(data, dict):
            people = data
            people_list = list(data.values())
        else:
            people_list = data
            people = {person.get("cpr"): person for person in data}

        familyrelations = FamilyRelations(people_list)

        results = {}

        # O(n), where n is number of people
        for child in people_list:
            child_cpr = child.get("cpr")
            child_blood = child.get("blood_type")

            if not child_cpr or not child_blood:
                continue

            grandparents = familyrelations.get_grandparents(child_cpr, people_list)

            grandparents_who_can_donate = []

            for grandparent_cpr in grandparents:
                grandparent = people.get(grandparent_cpr)

                if grandparent is None:
                    continue

                grandparent_blood = grandparent.get("blood_type")

                if not grandparent_blood:
                    continue

                donation_result = self.q16_can_donate_blood(grandparent, child)

                if donation_result["person1_can_donate_to_person2"]:
                    grandparents_who_can_donate.append({
                        "grandparent_cpr": grandparent_cpr,
                        "grandparent_blood_type": grandparent_blood
                    })

            if grandparents_who_can_donate:
                results[child_cpr] = {
                    "child_cpr": child_cpr,
                    "child_blood_type": child_blood,
                    "grandparents_who_can_donate": grandparents_who_can_donate
                }

        return results