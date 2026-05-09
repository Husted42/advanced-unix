# tests/test_questions_1_to_5.py
import os, sys

def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

import pytest

from src.classes.modifier import Modifier
from src.classes.analyzer import Analyzer
from src.func.utils import filter_data


@pytest.fixture
def sample_data():
    return [
        {
            "cpr": "010170-1234",
            "children": ["010190-1111"]
        },
        {
            "cpr": "020275-1234",
            "children": ["010195-2222"]
        },
        {
            "cpr": "030380-1234",
            "children": []
        },
        {
            "cpr": "040485-1234",
            "children": []
        },
    ]


@pytest.fixture
def modified_data(sample_data):
    """
    Applies the modifier methods needed for Question 1-5.
    The Analyzer depends on these added columns.
    """
    modifier = Modifier(sample_data)

    modifier.q1_add_age()
    modifier.q1_add_gender()
    modifier.q2_add_fartherhood_year()

    return sample_data


def test_q1_age_distribution(modified_data):
    analyzer = Analyzer(modified_data)

    result = analyzer.q1_value_distribution(
        column_name="age",
        bin_size=10
    )

    assert isinstance(result, dict)
    assert sum(result.values()) == 4

    # Ages:
    # 1970 -> 30
    # 1975 -> 25
    # 1980 -> 20
    # 1985 -> 15
    assert result["30-40"] == 1
    assert result["20-30"] == 2
    assert result["10-20"] == 1


def test_q1_gender_distribution(modified_data):
    analyzer = Analyzer(modified_data)

    result = analyzer.q1_gender_distribution()

    assert isinstance(result, dict)

    # Based on your current Modifier.q1_add_gender implementation:
    # gender = "Male" if int(cpr[4]) % 2 == 0 else "Female"
    assert sum(result.values()) == 4
    assert "male" in result or "female" in result


def test_q2_male_first_parenthood_summary(modified_data):
    analyzer = Analyzer(modified_data)

    filtered_data_male = filter_data(
        modified_data,
        filter_col="gender",
        filter_value="Male",
        operator="=="
    )

    result = analyzer.q2_value_summary(
        filtered_data_male,
        val_col="parenthood_start"
    )

    assert result is None


def test_q3_male_first_parenthood_distribution(modified_data):
    analyzer = Analyzer(modified_data)

    filtered_data_male = filter_data(
        modified_data,
        filter_col="gender",
        filter_value="Male",
        operator="=="
    )

    filtered_data_male_has_kids = filter_data(
        filtered_data_male,
        filter_col="parenthood_start",
        filter_value=None,
        operator="!="
    )

    result = analyzer.q1_value_distribution(
        column_name="parenthood_start",
        data=filtered_data_male_has_kids,
        bin_size=10
    )

    assert isinstance(result, dict)

def test_q4_female_first_parenthood_summary(modified_data):
    analyzer = Analyzer(modified_data)

    filtered_data_female = filter_data(
        modified_data,
        filter_col="gender",
        filter_value="Female",
        operator="=="
    )

    result = analyzer.q2_value_summary(
        filtered_data_female,
        val_col="parenthood_start"
    )

    if result is not None:
        assert isinstance(result, dict)

        assert "max" in result
        assert "min" in result
        assert "avg" in result
        assert "count" in result

        assert result["count"] >= 1
        assert result["min"] <= result["avg"] <= result["max"]


def test_q5_female_first_parenthood_distribution(modified_data):
    analyzer = Analyzer(modified_data)

    filtered_data_female = filter_data(
        modified_data,
        filter_col="gender",
        filter_value="Female",
        operator="=="
    )

    filtered_data_female_has_kids = filter_data(
        filtered_data_female,
        filter_col="parenthood_start",
        filter_value=None,
        operator="!="
    )

    result = analyzer.q1_value_distribution(
        column_name="parenthood_start",
        data=filtered_data_female_has_kids,
        bin_size=10
    )

    assert isinstance(result, dict)