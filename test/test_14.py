import pytest

from src.classes.modifier import Modifier
from src.classes.analyzer import Analyzer


@pytest.fixture
def sample_data_q14():
    """
    Test data for Question 14.

    We create children with two parents each.
    The Analyzer uses FamilyRelations.get_parents(child_cpr, data),
    so the parent CPRs must appear in the child's parent fields exactly
    as your parser stores them.

    If your parsed data uses different parent keys, change "mother" and "father"
    below to match your actual structure.
    """
    return [
        # ---------- Parent pair 1: Fat / Fat ----------
        {
            "cpr": "010170-1235",
            "height": 170,
            "weight": 90,
            "children": ["010100-1111"],
        },
        {
            "cpr": "020270-1234",
            "height": 160,
            "weight": 80,
            "children": ["010100-1111"],
        },
        {
            "cpr": "010100-1111",
            "height": 120,
            "weight": 25,
            "father": "010170-1235",
            "mother": "020270-1234",
            "children": [],
        },

        # ---------- Parent pair 2: Fat / Normal ----------
        {
            "cpr": "030175-1237",
            "height": 180,
            "weight": 95,
            "children": ["020100-2222"],
        },
        {
            "cpr": "040280-1238",
            "height": 170,
            "weight": 65,
            "children": ["020100-2222"],
        },
        {
            "cpr": "020100-2222",
            "height": 120,
            "weight": 25,
            "father": "030175-1237",
            "mother": "040280-1238",
            "children": [],
        },

        # ---------- Parent pair 3: Normal / Slim ----------
        {
            "cpr": "050180-1239",
            "height": 180,
            "weight": 75,
            "children": ["030100-3333"],
        },
        {
            "cpr": "060285-1230",
            "height": 170,
            "weight": 50,
            "children": ["030100-3333"],
        },
        {
            "cpr": "030100-3333",
            "height": 120,
            "weight": 25,
            "father": "050180-1239",
            "mother": "060285-1230",
            "children": [],
        },
    ]


def test_q14_calculate_bmi(sample_data_q14):
    modifier = Modifier(sample_data_q14)

    modifier.q14_calculate_bmi()

    person = sample_data_q14[0]

    expected_bmi = 90 / (1.70 ** 2)

    assert "bmi" in person
    assert person["bmi"] == pytest.approx(expected_bmi)


def test_q14_add_bmi_category(sample_data_q14):
    modifier = Modifier(sample_data_q14)

    modifier.q14_calculate_bmi()
    modifier.q14_add_bmi_category()

    people = {person["cpr"]: person for person in sample_data_q14}

    assert people["010170-1235"]["bmi_category"] == "Fat"
    assert people["020270-1234"]["bmi_category"] == "Fat"

    assert people["030175-1237"]["bmi_category"] == "Fat"
    assert people["040280-1238"]["bmi_category"] == "Normal"

    assert people["050180-1239"]["bmi_category"] == "Normal"
    assert people["060285-1230"]["bmi_category"] == "Slim"


def test_q14_parent_bmi_couple_distribution(sample_data_q14):
    modifier = Modifier(sample_data_q14)

    modifier.q14_calculate_bmi()
    modifier.q14_add_bmi_category()

    analyzer = Analyzer(sample_data_q14)

    result = analyzer.q14_parent_bmi_couple_distribution()

    assert result["Total parent pairs"] == 3

    assert result["Couple counts"]["Fat/Fat"] == 1
    assert result["Couple counts"]["Fat/Normal"] == 1
    assert result["Couple counts"]["Fat/Slim"] == 0
    assert result["Couple counts"]["Normal/Normal"] == 0
    assert result["Couple counts"]["Normal/Slim"] == 1
    assert result["Couple counts"]["Slim/Slim"] == 0

    assert result["Couple percentages"]["Fat/Fat"] == pytest.approx(33.3333333333)
    assert result["Couple percentages"]["Fat/Normal"] == pytest.approx(33.3333333333)
    assert result["Couple percentages"]["Normal/Slim"] == pytest.approx(33.3333333333)