import json

def parse_file_to_json(file_path):
    # Not all people has children, so we initialize this attribute to be empty, otherwise it would just be missing for some and we cound't iterate through them
    # Note that this happens each time we initialize a person 
    people = []
    current_person = {"children": []}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Checking if it is a new person based on empty lines
            # If it is we append and create a new one
            if not line:
                # cpr allows for doulbe line splits, st. two lines splits dones't append a person with only "{"children": []}"
                if current_person and "cpr" in current_person:
                    people.append(current_person)
                    current_person = {"children": []}
                continue

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
                current_person["children"] = value.split()


        if current_person and "cpr" in current_person:
            people.append(current_person)

    return people
