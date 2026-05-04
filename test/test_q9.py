from src.classes.analyzer import Analyzer
from src.func.dataloader import parse_file_to_json

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
        #grandparents
        {
        'cpr': '230226-9781',
        'children': ["081154-2786", "120853-1151"]
        }, 
        {
        'cpr': '230226-9780',
        'children': ["081154-2786", "120853-1151"]
        },
        #child1 and partner
        {
        'cpr': '081154-2786',
        'children': ["081177-9473", "050679-5672"]
        },
        {
        'cpr': '300680-6727',
        'children': ["081177-9473", "050679-5672"]
        },
        #child2 and partner
        {
        'cpr': '120853-1151',
        'children': ["081188-4322", "050683-1234", "241285-7862"]
        },
        {
        'cpr': '201054-1152',
        'children': ["081188-4322", "050683-1234", "241285-7862"]
        },
        #grandchildren
        {
        'cpr': '081177-9473'
        },
        {
        'cpr': '050679-5672'
        },
        {
        'cpr': '081188-4322'
        },
        {
        'cpr': '050683-1234'
        }, 
        {
        'cpr': '241285-7862'
        }, 
        #random
        {
        'cpr': '050683-7362'
        }

    ]

    analyzer = Analyzer(mock_dataset)
    
    expected = {
            "Number of people in the database who has a cousin": 5,
            "Average number of cousins, for people who has a cousin": approx(2.4),
            }

    results = analyzer.q9_cousins_calculations(mock_dataset)

    assert results == expected

def test_cousins_rules():

    data = parse_file_to_json("data/people.db")

    analyzer = Analyzer(data)
    cousin_pairs = analyzer.q9_cousins(data)

    #no duplicate tuble
    assert len(cousin_pairs) == len(set(cousin_pairs))

    #not cousins with yourself
    for cousin in cousin_pairs:
        assert cousin[0] != cousin[1]
    
    #symmetry check
    for cousin1, cousin2 in cousin_pairs:
        assert (cousin2, cousin1) in cousin_pairs

    cpr1 = []
    cpr2 = []

    #double symmetry check
    for cousin1, cousin2 in cousin_pairs:
        cpr1.append(cousin1)
        cpr2.append(cousin2)

    assert set(cpr1) == set(cpr2)
    assert sorted(cpr1) == sorted(cpr2)

def test_sibling():

    mock_dataset = [
        #grandparents
        {
        'cpr': '230226-9781',
        'children': ["081154-2786", "120853-1151"]
        }, 
        {
        'cpr': '230226-9780',
        'children': ["081154-2786", "120853-1151"]
        },
        #child1 and partner
        {
        'cpr': '081154-2786',
        'children': ["081177-9473", "050679-5672"]
        },
        {
        'cpr': '300680-6727',
        'children': ["081177-9473", "050679-5672"]
        },
        #child2 and partner
        {
        'cpr': '120853-1151',
        },
        #grandchildren, who are also siblings
        {
        'cpr': '081177-9473'
        },
        {
        'cpr': '050679-5672'
        },
    ]

    analyzer = Analyzer(mock_dataset)
    
    expected = {
            "Number of people in the database who has a cousin": 0,
            "Average number of cousins, for people who has a cousin": 0.0,
            }

    results = analyzer.q9_cousins_calculations(mock_dataset)

    assert results == expected