# We want to assume that the user is a the repository root when running the program. This will make refrencing files easier.
import os
import sys
from pathlib import Path
from classes import analyzer
from classes import modifier
from func.utils import set_working_directory_to_repo_root
set_working_directory_to_repo_root()



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
    modifier.q1_add_age()
    modifier.q1_add_gender()

    print(analyzer.q1_age_distribution())
    print(analyzer.q1_gender_distribution())

if __name__ == "__main__":
    main()