from src.classes.analyzer import Analyzer
from src.func.dataloader import parse_file_to_json
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

def test_q11_child_has_more_than_one_partner():
        
    """
    A test to verify correct results
    """

    mockdata = [
        {
            'cpr': '1234',
            'children' : ['1111', '1112']
        },
        {
            'cpr': '4321',
            'children' : ['1111']
        },
        {
            'cpr': '5678',
            'children' : ['1112']
        },
    ]
    analyzer = Analyzer(mockdata)

    expected = {'Percentage of parents who have a child with more than one': approx((1/3*100))}

    results = analyzer.q11_has_child_with_more_than_one(mockdata)

    assert expected == results

def test_q11_child_has_more_than_two_partner():
        
    """
    A test to verify correct results
    """

    mockdata = [
        {
            'cpr': '1234',
            'children' : ['1111', '1112', '1113']
        },
        {
            'cpr': '4321',
            'children' : ['1111']
        },
        {
            'cpr': '5678',
            'children' : ['1112']
        },
        {
            'cpr': '8765',
            'children' : ['1113']
        },

    ]
    analyzer = Analyzer(mockdata)

    expected = {'Percentage of parents who have a child with more than one': approx((1/4*100))}

    results = analyzer.q11_has_child_with_more_than_one(mockdata)

    assert expected == results


