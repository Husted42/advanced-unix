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