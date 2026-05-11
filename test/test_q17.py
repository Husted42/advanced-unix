import pytest

from src.classes.analyzer import Analyzer


@pytest.fixture
def sample_data_q17():
    """
    Test data for Question 17.

    q17_grandparents_can_donate_to_children() uses:
    - FamilyRelations.get_grandparents(child_cpr, data)
    - Analyzer.q16_can_donate_blood(grandparent, child)

    Family relations are created through the "children" lists.
    """

    return [
        # ============================================================
        # Family 1
        # Grandparent O- can donate to grandchild A+
        # Expected: child 010110-5555 is included
        # ============================================================

        # Grandparents
        {
            "cpr": "010140-1111",
            "blood_type": "O-",
            "children": ["010170-3333"],
        },
        {
            "cpr": "020145-2222",
            "blood_type": "AB+",
            "children": ["010170-3333"],
        },

        # Parent
        {
            "cpr": "010170-3333",
            "blood_type": "A+",
            "children": ["010110-5555"],
        },

        # Other parent
        {
            "cpr": "020175-4444",
            "blood_type": "B+",
            "children": ["010110-5555"],
        },

        # Child / grandchild
        {
            "cpr": "010110-5555",
            "blood_type": "A+",
            "children": [],
        },

        # ============================================================
        # Family 2
        # Grandparents AB+ and B+ cannot donate to grandchild O+
        # Expected: child 020112-9999 is NOT included
        # ============================================================

        # Grandparents
        {
            "cpr": "030150-6666",
            "blood_type": "AB+",
            "children": ["030180-8888"],
        },
        {
            "cpr": "040155-7777",
            "blood_type": "B+",
            "children": ["030180-8888"],
        },

        # Parent
        {
            "cpr": "030180-8888",
            "blood_type": "B+",
            "children": ["020112-9999"],
        },

        # Other parent
        {
            "cpr": "040185-0000",
            "blood_type": "O+",
            "children": ["020112-9999"],
        },

        # Child / grandchild
        {
            "cpr": "020112-9999",
            "blood_type": "O+",
            "children": [],
        },

        # ============================================================
        # Family 3
        # Grandparent A- can donate to grandchild AB+
        # Expected: child 030115-2468 is included
        # ============================================================

        # Grandparents
        {
            "cpr": "050150-1357",
            "blood_type": "A-",
            "children": ["050180-1113"],
        },
        {
            "cpr": "060155-2468",
            "blood_type": "O+",
            "children": ["050180-1113"],
        },

        # Parent
        {
            "cpr": "050180-1113",
            "blood_type": "A+",
            "children": ["030115-2468"],
        },

        # Other parent
        {
            "cpr": "060185-2224",
            "blood_type": "B+",
            "children": ["030115-2468"],
        },

        # Child / grandchild
        {
            "cpr": "030115-2468",
            "blood_type": "AB+",
            "children": [],
        },
    ]


def test_q17_grandparents_can_donate_to_children(sample_data_q17):
    analyzer = Analyzer(sample_data_q17)

    result = analyzer.q17_grandparents_can_donate_to_children()

    assert isinstance(result, dict)

    # We created two children with at least one compatible grandparent donor
    assert len(result) == 2

    # ------------------------------------------------------------
    # Child 1: A+
    # Grandparent O- can donate to A+
    # Grandparent AB+ cannot donate to A+
    # ------------------------------------------------------------
    assert "010110-5555" in result

    child_1 = result["010110-5555"]

    assert child_1["child_cpr"] == "010110-5555"
    assert child_1["child_blood_type"] == "A+"

    child_1_grandparents = child_1["grandparents_who_can_donate"]

    assert len(child_1_grandparents) == 1
    assert child_1_grandparents[0]["grandparent_cpr"] == "010140-1111"
    assert child_1_grandparents[0]["grandparent_blood_type"] == "O-"

    # ------------------------------------------------------------
    # Child 2: O+
    # Grandparents AB+ and B+ cannot donate to O+
    # Therefore this child should not be included
    # ------------------------------------------------------------
    assert "020112-9999" not in result

    # ------------------------------------------------------------
    # Child 3: AB+
    # Grandparent A- can donate to AB+
    # Grandparent O+ can also donate to AB+
    # ------------------------------------------------------------
    assert "030115-2468" in result

    child_3 = result["030115-2468"]

    assert child_3["child_cpr"] == "030115-2468"
    assert child_3["child_blood_type"] == "AB+"

    child_3_grandparents = child_3["grandparents_who_can_donate"]

    grandparent_cprs = {
        grandparent["grandparent_cpr"]
        for grandparent in child_3_grandparents
    }

    grandparent_blood_types = {
        grandparent["grandparent_blood_type"]
        for grandparent in child_3_grandparents
    }

    assert grandparent_cprs == {
        "050150-1357",
        "060155-2468",
    }

    assert grandparent_blood_types == {
        "A-",
        "O+",
    }


def test_q17_result_structure(sample_data_q17):
    analyzer = Analyzer(sample_data_q17)

    result = analyzer.q17_grandparents_can_donate_to_children()

    for child_cpr, child_result in result.items():
        assert "child_cpr" in child_result
        assert "child_blood_type" in child_result
        assert "grandparents_who_can_donate" in child_result

        assert child_result["child_cpr"] == child_cpr
        assert isinstance(child_result["grandparents_who_can_donate"], list)

        for grandparent in child_result["grandparents_who_can_donate"]:
            assert "grandparent_cpr" in grandparent
            assert "grandparent_blood_type" in grandparent