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


########## ---------- Main ---------- ##########
def main():
    data = parse_file_to_json("data/people.db")
    modifier = Modifier(data)
    analyzer = Analyzer(data)

    ########## ---------- Question 1 ---------- ##########
    # What is the age and gender distribution of the people in the database?
    print("Qustion 1 : ")
    modifier.q1_add_age()
    modifier.q1_add_gender()

    print(analyzer.q1_age_distribution())
    print(analyzer.q1_gender_distribution())

    ########## ---------- Question 2 ---------- ##########
    # At what age does the men become fathers first time (max age, min age, average age)?'
    print("\n\nQustion 2 : ")
    modifier.q2_add_fartherhood_year()
    result_q2 = analyzer.q2_value_summary_with_filter(
        val_col="height",
        filter_col="gender",
        filter_value="Male",
        operator="=="
    )
    print(result_q2)

if __name__ == "__main__":
    main()