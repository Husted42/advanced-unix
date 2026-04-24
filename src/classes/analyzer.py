# We want to assume that the user is a the repository root when running the program. This will make refrencing files easier.
import sys, os
def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

########## ---------- Imports ---------- ##########
from src.func.utils import get_min
from src.func.utils import get_max


class Analyzer:
    def __init__(self, data):
        self.data = data

    def q1_age_distribution(self):
        age_bins = {}
        bin_size = 10

        for person in self.data:
            age = person.get("age")

            if age is None or age < 0:
                continue

            # lower gives the bin index by dividing with binsize
            # 65 // 10 = 6, which means the bin is 60-70
            lower = (age // bin_size) * bin_size
            upper = lower + bin_size
            bin_label = f"{lower}-{upper}"

            age_bins[bin_label] = age_bins.get(bin_label, 0) + 1

        return age_bins

    def q1_gender_distribution(self):
        gender_counts = {}

        for person in self.data:
            gender = person.get("gender")

            if not gender:
                continue

            gender = gender.lower()
            gender_counts[gender] = gender_counts.get(gender, 0) + 1

        return gender_counts
    

    # We make the implementation for an arbitrary filter
    # we need thils later
    def q2_value_summary_with_filter(
        self,
        val_col: str,
        filter_col: str,
        filter_value,
        operator: str = "=="
    ):
        values = []

        for person in self.data:
            value = person.get(val_col)
            filter_val = person.get(filter_col)

            if value is None or filter_val is None:
                continue

            if operator == "==" and filter_val == filter_value:
                values.append(value)
            elif operator == "!=" and filter_val != filter_value:
                values.append(value)
            elif operator == ">" and filter_val > filter_value:
                values.append(value)
            elif operator == ">=" and filter_val >= filter_value:
                values.append(value)
            elif operator == "<" and filter_val < filter_value:
                values.append(value)
            elif operator == "<=" and filter_val <= filter_value:
                values.append(value)

        if not values:
            return None

        avg = sum(values) / len(values)
        min = get_min(values)
        max = get_max(values)

        return {"max": max, "min":min, "avg":avg }