import re
from Person import Person
from dotenv import load_dotenv
import os

class PeopleManager:
    load_dotenv()

    all_people = []

    @staticmethod
    def add_person(person):
        PeopleManager.all_people.append(person)


    @staticmethod
    def seed_people():
        csv_location = "dummy_data/dummy_people.csv"

        # CSV structure: firstname,lastname,username,biography,password_key
        with open(csv_location, 'r') as file:
            lines = file.readlines()

            for index, line in enumerate(lines):
                if index == 0:
                    continue

                data = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)  # Ugly ahhh regex

                PeopleManager.add_person((Person(data[0].strip(), data[1].strip(), data[2].strip(), data[3].strip(), os.getenv(data[4].strip()))))

