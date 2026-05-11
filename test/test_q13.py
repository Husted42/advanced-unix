from src.classes.analyzer import Analyzer
from pytest import approx


def test_q12_do_tall_people_marry():

    mockdata = [
        # Tall/Tall couple
        {
            "cpr": "1111",
            "children": ["1212"],
            "tallness_category": "Tall"
        },
        {
            "cpr": "2222",
            "children": ["1212"],
            "tallness_category": "Tall"
        },
        {
            "cpr": "1212",
            "tallness_category": "Tall"
        },

        # Normal/short couple
        {
            "cpr": "3333",
            "children": ["4343"],
            "tallness_category": "Normal"
        },
        {
            "cpr": "4444",
            "children": ["4343"],
            "tallness_category": "Short"
        },
        {
            "cpr": "4343",
            "tallness_category": "Short"
        },

        # Short/Short couple
        {
            "cpr": "5555",
            "children": ["5656"],
            "tallness_category": "Short"
        },
        {
            "cpr": "6666",
            "children": ["5656"],
            "tallness_category": "Short"
        },
        {
            "cpr": "5656",
            "tallness_category": "Tall"
        },
    ]

    analyzer = Analyzer(mockdata)

    result = analyzer.q13_do_tal_people_get_tall_children(mockdata)

    #assert each result one by one

    #o tall parents
    assert result["O tall parents"] == {
        "Total children": 2,
        'Tall children': 1,
        "Percentage tall children": approx((1/2*100)),
    }


    #1 tall parent
    assert result["1 tall parents"] == {
        "Total children": 0,
        'Tall children': 0,
        "Percentage tall children": 0,
    }

    #2 tall parent
    assert result["2 tall parents"] == {
        "Total children": 1,
        'Tall children': 1,
        "Percentage tall children": 100,
    }


