from Person import Person
import re

def seed_people():
    csv_location = "../dummy_data/dummy_people.csv"

    # CSV structure: firstname,lastname,username,biography
    with open(csv_location, 'r') as file:
        lines = file.readlines()

        people = []

        for index, line in enumerate(lines):
            if index == 0:
                continue

            data = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line) # Ugly ahhh regex
            people.append(Person(data[0].strip(), data[1].strip(), data[2].strip(), data[3].strip()))

        return people


persons = seed_people()

