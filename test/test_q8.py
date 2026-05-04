from src.classes.analyzer import Analyzer
from src.classes.modifier import Modifier
from src.classes.familyrelations import FamilyRelations
import pytest
from pytest import approx
from pathlib import Path
import os, sys

def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

def test_q8_grandparents():
        
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
        'cpr': '081154-2786',
        'children': ["081177-9473", "050679-5672"]
        },
        {
        'cpr': '300655-6723',
        'children': ["081177-9473", "050679-5672"]
        },
        {
        'cpr': '300680-6724',
        'children': ["081199-9473", "050698-5672"]
        },
        {
        'cpr': '081177-9473'
        },
        {
        'cpr': '050679-5672'
        }         
    ]

    modifier = Modifier(mock_dataset)
    analyzer = Analyzer(mock_dataset)
    familyrelations = FamilyRelations(mock_dataset)

    modifier.q1_add_age()

    pairs = familyrelations.get_parents_pair(mock_dataset)

    expected = {
            "Amount of people who has a grandparent": 2,
            "Percentage of people who has a grandparent": approx(2/7 *100)
        }

    results = analyzer.q8_grandparents_count(mock_dataset)

    assert results == expected


