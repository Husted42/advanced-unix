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

    print("\n\nQustion 9 : ")

    results_q9 = analyzer.q9_cousins_calculations(data)

    print(results_q9)
if __name__ == "__main__":
    main()