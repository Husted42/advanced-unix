# We want to assume that the user is a the repository root when running the program. This will make refrencing files easier.
import sys, os
def set_working_directory_to_repo_root(root="advanced-unix"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = current_dir.find(root)
    if src_index != -1:
        sys.path.append(str(current_dir[:src_index + len(root)]))
set_working_directory_to_repo_root()

########## ---------- Imports ---------- ##########
import unittest

from src.func.dataloader import parse_file_to_json

########## ---------- Tests ---------- ##########
class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Resolve path relative to this test file
        self.test_file = os.path.join(
            os.getcwd(),
            "testdata",
            "people.db"
        )

    def test_parse_people_file(self):
        result = parse_file_to_json(self.test_file)

        expected = [
                {
                    "children": [],
                    "cpr": "121215-2968",
                    "first_name": "Sanne",
                    "last_name": "Lind",
                    "height": 187,
                    "weight": 74,
                    "eye_color": "Green",
                    "blood_type": "B+",
                },
                {
                    "children": ["081154-2786", "120853-1151"],
                    "cpr": "230226-9781",
                    "first_name": "Anton",
                    "last_name": "Gade",
                    "height": 201,
                    "weight": 65,
                    "eye_color": "Black",
                    "blood_type": "A+",
                },
            ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()