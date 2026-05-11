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
            "cpr": "1212"
        },

        # Normal/Tall couple
        {
            "cpr": "3333",
            "children": ["4343"],
            "tallness_category": "Normal"
        },
        {
            "cpr": "4444",
            "children": ["4343"],
            "tallness_category": "Tall"
        },
        {
            "cpr": "4343"
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
            "cpr": "5656"
        },
    ]

    analyzer = Analyzer(mockdata)

    result = analyzer.q12_do_tall_people_marry_each_other(mockdata)

    #assert each result one by one
    # 
    # total amount of parents part    
    assert result["Total parent pairs"] == 3

    #tall distribution in count
    assert result["Couple counts"] == {
        "Tall/Tall": 1,
        "Normal/Tall": 1,
        "Short/Tall": 0,
        "Normal/Normal": 0,
        "Normal/Short": 0,
        "Short/Short": 1
    }

    #tall distribution in percentage
    assert result["Couple percentages"]["Tall/Tall"] == approx((1/3) * 100)
    assert result["Couple percentages"]["Normal/Tall"] == approx((1/3) * 100)
    assert result["Couple percentages"]["Short/Short"] == approx((1/3) * 100)

    #count of total height distribution
    assert result["Tallness counts"] == {
        "Tall": 3,
        "Normal": 1,
        "Short": 2
    }

    assert result["Tallness percentages"]["Tall"] == approx((3/6) * 100)
    assert result["Tallness percentages"]["Normal"] == approx((1/6) * 100)
    assert result["Tallness percentages"]["Short"] == approx((2/6) * 100)
