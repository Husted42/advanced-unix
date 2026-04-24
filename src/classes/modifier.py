'''
    We will use this class whenever we need to add features to the data.
'''
class Modifier:
    def __init__(self, data):
        self.data = data

    '''
        Since data was constructed in 2000 it's fair to assumme that all are from 1900's
    '''
    def q1_add_age(self):
        for person in self.data:
            cpr = person["cpr"]
            age = 2026 - (1900 + int(cpr[4:6]))  # Assuming the first 4 digits are the birth year
            person["age"] = age

    def q1_add_gender(self):
        for person in self.data:
            cpr = person["cpr"]
            # We can determine the sex based ont the 5th digit of the CPR number
            gender = "Male" if int(cpr[4]) % 2 == 0 else "Female"
            person["gender"] = gender