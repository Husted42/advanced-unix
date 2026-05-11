import pytest

from src.classes.analyzer import Analyzer


@pytest.fixture
def sample_data_q16():
    """
    Test data for Question 16.

    q16_fathers_can_donate_to_children() uses:
    - FamilyRelations.get_father(child_cpr, data)
    - Analyzer.q16_can_donate_blood(father, child)

    The parents are found through the "children" lists.
    The father is determined by CPR gender logic in FamilyRelations.
    """

    return [
        # ------------------------------------------------------------
        # Father 1: O- can donate to everyone
        # Son: A+
        # Expected: father_can_donate_to_son = True
        # ------------------------------------------------------------
        {
            "cpr": "010160-1111",  # Male if last digit odd
            "blood_type": "O-",
            "children": ["010190-3333"],
        },
        {
            "cpr": "020260-2222",  # Female if last digit even
            "blood_type": "AB+",
            "children": ["010190-3333"],
        },
        {
            "cpr": "010190-3333",
            "blood_type": "A+",
            "children": [],
        },

        # ------------------------------------------------------------
        # Father 2: AB+ can only donate to AB+
        # Son: O+
        # Expected: father_can_donate_to_son = False
        # ------------------------------------------------------------
        {
            "cpr": "030165-4445",  # Male
            "blood_type": "AB+",
            "children": ["020195-6666"],
        },
        {
            "cpr": "040270-5556",  # Female
            "blood_type": "O-",
            "children": ["020195-6666"],
        },
        {
            "cpr": "020195-6666",
            "blood_type": "O+",
            "children": [],
        },

        # ------------------------------------------------------------
        # Father 3: A- can donate to A-, A+, AB-, AB+
        # Son: AB+
        # Expected: father_can_donate_to_son = True
        # ------------------------------------------------------------
        {
            "cpr": "050170-7777",  # Male
            "blood_type": "A-",
            "children": ["030198-9999"],
        },
        {
            "cpr": "060275-8888",  # Female
            "blood_type": "B+",
            "children": ["030198-9999"],
        },
        {
            "cpr": "030198-9999",
            "blood_type": "AB+",
            "children": [],
        },
    ]


def test_q16_can_donate_blood_true_cases(sample_data_q16):
    analyzer = Analyzer(sample_data_q16)

    donor = {"blood_type": "O-"}
    receiver = {"blood_type": "A+"}

    result = analyzer.q16_can_donate_blood(donor, receiver)

    assert result["person1_can_donate_to_person2"] is True
    assert result["person2_can_donate_to_person1"] is False


def test_q16_can_donate_blood_false_case(sample_data_q16):
    analyzer = Analyzer(sample_data_q16)

    donor = {"blood_type": "AB+"}
    receiver = {"blood_type": "O+"}

    result = analyzer.q16_can_donate_blood(donor, receiver)

    assert result["person1_can_donate_to_person2"] is False
    assert result["person2_can_donate_to_person1"] is True


def test_q16_can_donate_blood_missing_blood_type(sample_data_q16):
    analyzer = Analyzer(sample_data_q16)

    donor = {"blood_type": None}
    receiver = {"blood_type": "O+"}

    result = analyzer.q16_can_donate_blood(donor, receiver)

    assert result["person1_can_donate_to_person2"] is False
    assert result["person2_can_donate_to_person1"] is False
    assert result["error"] == "Missing blood type information"
