import pytest

from src.classes.analyzer import Analyzer


@pytest.fixture
def sample_data_q15():
    """
    Test data for Question 15.

    FamilyRelations.get_parents(child_cpr, data) usually finds parents
    by checking which people have the child CPR in their "children" list.

    Therefore, parents must contain the child CPR in their "children" field.
    """

    return [
        # ------------------------------------------------------------
        # Case 1: impossible
        # Child has O+, parents are AB+ and AB+
        # AB + AB cannot produce O
        # ------------------------------------------------------------
        {
            "cpr": "010160-1111",
            "blood_type": "AB+",
            "children": ["010190-3333"],
        },
        {
            "cpr": "020260-2222",
            "blood_type": "AB-",
            "children": ["010190-3333"],
        },
        {
            "cpr": "010190-3333",
            "blood_type": "O+",
            "children": [],
        },

        # ------------------------------------------------------------
        # Case 2: possible
        # Child has A+, parents are A+ and O-
        # A + O can produce A
        # ------------------------------------------------------------
        {
            "cpr": "030165-4444",
            "blood_type": "A+",
            "children": ["020195-6666"],
        },
        {
            "cpr": "040270-5555",
            "blood_type": "O-",
            "children": ["020195-6666"],
        },
        {
            "cpr": "020195-6666",
            "blood_type": "A+",
            "children": [],
        },

        # ------------------------------------------------------------
        # Case 3: impossible
        # Child has AB-, parents are O+ and O-
        # O + O can only produce O
        # ------------------------------------------------------------
        {
            "cpr": "050170-7777",
            "blood_type": "O+",
            "children": ["030198-9999"],
        },
        {
            "cpr": "060275-8888",
            "blood_type": "O-",
            "children": ["030198-9999"],
        },
        {
            "cpr": "030198-9999",
            "blood_type": "AB-",
            "children": [],
        },
    ]


def test_q15_abo_removes_rhesus_factor(sample_data_q15):
    analyzer = Analyzer(sample_data_q15)

    assert analyzer.q15_abo("A+") == "A"
    assert analyzer.q15_abo("A-") == "A"
    assert analyzer.q15_abo("B+") == "B"
    assert analyzer.q15_abo("B-") == "B"
    assert analyzer.q15_abo("AB+") == "AB"
    assert analyzer.q15_abo("AB-") == "AB"
    assert analyzer.q15_abo("O+") == "O"
    assert analyzer.q15_abo("O-") == "O"


def test_q15_can_parents_have_child_possible_cases(sample_data_q15):
    analyzer = Analyzer(sample_data_q15)

    # A + O can produce A
    assert analyzer.q15_can_parents_have_child(
        child_blood="A+",
        parent1_blood="A+",
        parent2_blood="O-"
    ) is True

    # A + B can produce AB
    assert analyzer.q15_can_parents_have_child(
        child_blood="AB+",
        parent1_blood="A+",
        parent2_blood="B-"
    ) is True

    # O + O can produce O
    assert analyzer.q15_can_parents_have_child(
        child_blood="O-",
        parent1_blood="O+",
        parent2_blood="O-"
    ) is True


def test_q15_can_parents_have_child_impossible_cases(sample_data_q15):
    analyzer = Analyzer(sample_data_q15)

    # AB + AB cannot produce O
    assert analyzer.q15_can_parents_have_child(
        child_blood="O+",
        parent1_blood="AB+",
        parent2_blood="AB-"
    ) is False

    # O + O cannot produce AB
    assert analyzer.q15_can_parents_have_child(
        child_blood="AB-",
        parent1_blood="O+",
        parent2_blood="O-"
    ) is False

    # O + O cannot produce A
    assert analyzer.q15_can_parents_have_child(
        child_blood="A+",
        parent1_blood="O+",
        parent2_blood="O-"
    ) is False


def test_q15_impossible_parent_child_bloodtypes(sample_data_q15):
    analyzer = Analyzer(sample_data_q15)

    result = analyzer.q15_impossible_parent_child_bloodtypes()

    assert isinstance(result, dict)

    # We created exactly two impossible cases
    assert len(result) == 2

    # Child O+ with AB and AB parents should be impossible
    assert "010190-3333" in result
    assert result["010190-3333"] == {
        "child_blood_type": "O+",
        "parent1_cpr": "010160-1111",
        "parent1_blood_type": "AB+",
        "parent2_cpr": "020260-2222",
        "parent2_blood_type": "AB-",
    }

    # Child AB- with O and O parents should be impossible
    assert "030198-9999" in result
    assert result["030198-9999"] == {
        "child_blood_type": "AB-",
        "parent1_cpr": "050170-7777",
        "parent1_blood_type": "O+",
        "parent2_cpr": "060275-8888",
        "parent2_blood_type": "O-",
    }

    # This child should not be included because A + O can produce A
    assert "020195-6666" not in result