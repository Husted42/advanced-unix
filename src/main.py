# We want to assume that the user is a the repository root when running the program. This will make refrencing files easier.
import os
import sys
from pathlib import Path
from classes import analyzer
from classes import modifier

########## ---------- Imports ---------- ##########
from src.func.dataloader import parse_file_to_json
from src.classes.analyzer import Analyzer
from src.classes.modifier import Modifier
from src.classes.familyrelations import FamilyRelations

from src.func.utils import filter_data


########## ---------- Main ---------- ##########
def main():
    data = parse_file_to_json("data/people.db")
    modifier = Modifier(data)
    analyzer = Analyzer(data)
    familyrelations = FamilyRelations(data)

    ########## ---------- Question 1 ---------- ##########
    # What is the age and gender distribution of the people in the database?
    print("Qustion 1 : ")
    modifier.q1_add_age()
    modifier.q1_add_gender()

    print(analyzer.q1_value_distribution())
    print(analyzer.q1_gender_distribution())

    ########## ---------- Question 2 ---------- ##########
    # At what age does the men become fathers first time (max age, min age, average age)?'
    print("\n\nQustion 2 : ")
    modifier.q2_add_fartherhood_year()
    filtered_data_male = filter_data(
        data,
        filter_col="gender",
        filter_value="Male",
        operator="=="
    )

    result_q2 = analyzer.q2_value_summary(
        filtered_data_male,
        val_col="parenthood_start"
    )
    print(result_q2)


    ########## ---------- Question 3 ---------- ##########
    # Is the distribution of first-time fatherhood age normal/sensible?
    print("\n\nQustion 3 : ")
    filtered_data_male_has_kids = filter_data(
        filtered_data_male,
        filter_col="parenthood_start",
        filter_value="None",
        operator="!="
    )

    result_q3 = analyzer.q1_value_distribution(
        column_name="parenthood_start",
        data=filtered_data_male_has_kids,
        bin_size=10
    )
    print(result_q3)

    ########## ---------- Question 4 ---------- ##########
    # At what age do women become mothers first time (max age, min age, average age)?
    print("\n\nQustion 4 : ")

    filtered_data_female = filter_data(
        data,
        filter_col="gender",
        filter_value="Female",
        operator="=="
    )

    result_q4 = analyzer.q2_value_summary(
        filtered_data_female,
        val_col="parenthood_start"
    )

    print(result_q4)


    ########## ---------- Question 5 ---------- ##########
    # Is the distribution of first-time motherhood age normal/sensible?
    print("\n\nQustion 5 : ")

    filtered_data_female_has_kids = filter_data(
        filtered_data_female,
        filter_col="parenthood_start",
        filter_value=None,
        operator="!="
    )

    result_q5 = analyzer.q1_value_distribution(
        column_name="parenthood_start",
        data=filtered_data_female_has_kids,
        bin_size=10
    )

    print(result_q5)


    ########## ---------- Question 6 ---------- ##########
    # How many men and women do not have children (in percent)?

    print("\n\nQustion 6 : ")
    result_q6 = analyzer.q6_parenthood_distribution(data)

    print(result_q6)

    ########## ---------- Question 7 ---------- ##########
    # What is the average age difference between the parents (with a child in common obviously)?
    print("\n\nQustion 7 : ")
    

    pairs = familyrelations.get_parents_pair(data)

    results_q7 = analyzer.q7_average_age_difference(data, pairs)

    print(results_q7)

    ########## ---------- Question 8 ---------- ##########
    # How many people has at least one grandparent that is still alive? A person is living if he/she is in the database. State the number both in percent and as a real number.

    print("\n\nQustion 8 : ")

    results_q8 = analyzer.q8_grandparents_count(data)

    print(results_q8)

    ########## ---------- Question 9 ---------- ########## 
    # How many has at least one cousin in the data set? What is the average number of cousins based on those who have cousins?
    print("\n\nQustion 9 : ")

    results_q9 = analyzer.q9_cousins_calculations(data)

    print(results_q9)

    ########## ---------- Question 14 ---------- ##########
    '''
        Do fat people marry?
    '''
    print("\n\nQustion 14 : ")
    modifier = Modifier(data)
    modifier.q14_calculate_bmi()
    modifier.q14_add_bmi_category()

    analyzer = Analyzer(data)
    result = analyzer.q14_parent_bmi_couple_distribution()

    print("\n########## Question 14 Results ##########\n")

    print(f"Total parent pairs: {result['Total parent pairs']}\n")

    print("Couple BMI distribution:")
    for couple_type in result["Couple counts"]:
        count = result["Couple counts"][couple_type]
        percentage = result["Couple percentages"][couple_type]
        print(f"{couple_type}: {count} pairs ({percentage:.2f}%)")

    ########## ---------- Question 15 ---------- ##########
    '''
    Using the knowledge of blood group type inheritance, 
    are there any children in the database where you can safely say that at least one of the parents are not the real parent. 
    If such children exists, make a list of them. In the report you must discuss how you determine that the parent(s) of the child are not the "true" parents.
    ''' 
    print("\n\nQustion 15 : ")
    print("Impossible combination of blood types between parents and children: ")
    results_q15 = analyzer.q15_impossible_parent_child_bloodtypes()
    print("len(results_q15):", len(results_q15))
    print(dict(list(results_q15.items())[:5]))

    ########## ---------- Question 16 ---------- ##########
    '''
    Make a list of fathers who can donate blood to their sons.
    '''
    print("\n\nQustion 16 : ")
    father_son_donations = analyzer.q16_fathers_can_donate_to_children()
    number_of_pairs = len(father_son_donations)

    number_of_fathers = len({
        pair["father_cpr"]
        for pair in father_son_donations.values()
    })

    number_of_sons = len({
        pair["son_cpr"]
        for pair in father_son_donations.values()
    })

    print("Number of father-son pairs:", number_of_pairs)
    print("Number of fathers:", number_of_fathers)
    print("Number of sons:", number_of_sons)

    # Print a few examples of father-son pairs
    print("Examples of father-son pairs:")
    for i, pair in enumerate(father_son_donations.values()):
        if i >= 5:  # Print only the first 5 pairs
            break
        print(pair)

    ########## ---------- Question 17 ---------- ##########
    '''
    Make a list of children where at least one grandparent can donate blood to them.
    '''
    print("\n\nQuestion 17 : ")

    grandparent_child_donations = analyzer.q17_grandparents_can_donate_to_children()

    number_of_children = len(grandparent_child_donations)

    number_of_grandparents = len({
        grandparent["grandparent_cpr"]
        for child in grandparent_child_donations.values()
        for grandparent in child["grandparents_who_can_donate"]
    })

    number_of_donation_relations = sum(
        len(child["grandparents_who_can_donate"])
        for child in grandparent_child_donations.values()
    )

    print("Number of children with at least one grandparent donor:", number_of_children)
    print("Number of unique grandparents who can donate:", number_of_grandparents)
    print("Number of grandparent-child donation relations:", number_of_donation_relations)

    print("Examples:")
    for i, child in enumerate(grandparent_child_donations.values()):
        if i >= 5:
            break
        print(child)


    ########## ---------- Question 10 ---------- ########## 
    print("\n\nQustion 10 : ")

    results_q10 = analyzer.q10_firstborn_gender(data)

    print(results_q10)

    print(analyzer.max_number_of_children(data))

    ########## ---------- Question 11 ---------- ########## 
    print("\n\nQustion 11 : ")

    results_q11 = analyzer.q11_has_child_with_more_than_one(data)

    print(results_q11)

    ########## ---------- Question 12 ---------- ########## 
    print("\n\nQustion 12 : ")

    women_stats, men_stats = analyzer.what_is_tallness(data)

    print({
            "Stats on women's heights" : women_stats,
            "Stats on men's heights": men_stats
            })

    modifier = Modifier(data)
    modifier.q12_add_tallness_category(women_stats, men_stats)

    analyzer = Analyzer(data)
    result = analyzer.q12_do_tall_people_marry_each_other(data)

    print("Couple tallness distribution:")
    for couple_type in result["Couple counts"]:
        count = result["Couple counts"][couple_type]
        percentage = result["Couple percentages"][couple_type]
        print(f"{couple_type}: {count} pairs ({percentage:.2f}%)")

    print("\nTallness distribution among parents:")
    for category in result["Tallness counts"]:
        count = result["Tallness counts"][category]
        percentage = result["Tallness percentages"][category]
        print(f"{category}: {count} parents ({percentage:.2f}%)")

    
if __name__ == "__main__":
    main()

