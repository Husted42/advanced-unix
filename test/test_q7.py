from src.classes.analyzer import Analyzer
from src.classes.modifier import Modifier
from src.classes.familyrelations import FamilyRelations
import pytest
from pathlib import Path
import os, sys

def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

def test_q7_average_age_diffference():
        
    """
    A test to verify correct results
    """

    mock_dataset = [
        {
        'cpr': '230226-9781',
        'children': ["081154-2786", "120853-1151"]
        }, 
        {
        'cpr': '230226-9780',
        'children': ["081154-2786", "120853-1151"]
        },
        {
        'cpr': '010210-1233',
        'children': ["081135-9473", "050637-5672"]
        },
        {
        'cpr': '300612-6724',
        'children': ["081135-9473", "050637-5672"]
        },    
    ]

    modifier = Modifier(mock_dataset)
    analyzer = Analyzer(mock_dataset)
    familyrelations = FamilyRelations(mock_dataset)

    modifier.q1_add_age()

    pairs = familyrelations.get_parents_pair(mock_dataset)

    expected = {
        'Average age difference between parents is': 1.0}

    results = analyzer.q7_average_age_difference(mock_dataset, pairs)

    assert results == expected

def test_q7_division_by_zero():

    """
    A test to verify that function correctly avoid zero division, when no pair are present
    """

    mock_dataset = [
        {
        'cpr': '230226-9781',
        'children': ["081154-2786", "120853-1151"]
        }, 
        {
        'cpr': '230226-9780',
        'children': ["081154-2785", "120853-1154"]
        },
        {
        'cpr': '010210-1233',
        'children': ["081135-9473", "050637-5672"]
        },
        {
        'cpr': '300612-6724',
        'children': ["081135-9472", "050637-5679"]
        },    
    ]

    modifier = Modifier(mock_dataset)
    analyzer = Analyzer(mock_dataset)
    familyrelations = FamilyRelations(mock_dataset)


    modifier.q1_add_age()

    pairs = familyrelations.get_parents_pair(mock_dataset)

    expected = {
        'Average age difference between parents is': 0.0}

    results = analyzer.q7_average_age_difference(mock_dataset, pairs)
    print(results)
    assert results == expected



