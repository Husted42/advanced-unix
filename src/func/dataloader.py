import json

def parse_file_to_json(file_path):
    people = []
    current_person = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # An empty line indicates the end of a person's record
            if not line:
                if current_person:
                    people.append(current_person)
                    current_person = {}
                continue

            # Skipping comments
            if line[0] == "#": 
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "CPR":
                current_person["cpr"] = value
            elif key == "First name":
                current_person["first_name"] = value
            elif key == "Last name":
                current_person["last_name"] = value
            elif key == "Height":
                current_person["height"] = int(value)
            elif key == "Weight":
                current_person["weight"] = int(value)
            elif key == "Eye color":
                current_person["eye_color"] = value
            elif key == "Blood type":
                current_person["blood_type"] = value
            elif key == "Children":
                # We save the children as a list of names, splitting by whitespace
                current_person["children"] = value.split()

        if current_person:
            people.append(current_person)

    return people
