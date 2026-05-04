from src.classes.analyzer import Analyzer
import pytest
from pathlib import Path
import os, sys

def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

def test_q6_percentage_nonparent():
        
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
            'children': ["081154-2786"]
            },
            {
            'cpr': '230226-9782',
            },
            {
            'cpr': '230226-9783',
            },    
        ]

        analyzer = Analyzer(mock_dataset)

        expected = {'Percentages of men without children': 50.0, 
                    'Percentages of women without children': 50.0, 
                    'Total amount of people without children': 50.0
                    }
        
        results = analyzer.q6_parenthood_distribution(data = mock_dataset)

        assert results == expected

def test_empty_list():
     
    """
    A test to identify if the code correcty counts no children, even if 'children' is present at user,
    but column is empty

    """
    mock_dataset = [
        {
        'cpr': '230226-9781',
        'children': ["081154-2786", "120853-1151"]
        }, 
        {
        'cpr': '230226-9780',
        'children': ["081154-2786"]
        },
        {
        'cpr': '230226-9782',
        'children': []
        },
        {
        'cpr': '230226-9783',
        'children': []
        },    
    ]

    analyzer = Analyzer(mock_dataset)

    expected = {'Percentages of men without children': 50.0, 
                'Percentages of women without children': 50.0, 
                'Total amount of people without children': 50.0
                }
    
    results = analyzer.q6_parenthood_distribution(data = mock_dataset)

    assert results == expected

def test_one_gender():
     
    """
     This test verifies if the code runs correctly, even if one gender is present
     This could reveal division by zero errors:
    """
    mock_dataset = [
        {
        'cpr': '230226-9780',
        'children': ["081154-2786"]
        },
        {
        'cpr': '230226-9782',
        'children': []
        },  
    ]

    analyzer = Analyzer(mock_dataset)

    expected = {'Percentages of men without children': 0.0, 
                'Percentages of women without children': 50.0, 
                'Total amount of people without children': 50.0
                }
    
    results = analyzer.q6_parenthood_distribution(data = mock_dataset)

    assert results == expected

