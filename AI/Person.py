from AI import Model
import DummyTime
from models.prompts import Prompts
from postmanager import Postmanager
import json
import random

class Person:
    def __init__(self, firstname, lastname, username, biography, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.biography = biography
        self.password = password
        self.favourite_people = []
        self.CHANCE_TO_REPLY_TO_A_POST = 0.6
        self.cookie = "" # This cookie is for authentication purposes


        self.register_on_platform()
        self.login_on_platform()

    def register_on_platform(self):
        payload = {
            "name": self.firstname,
            "surname": self.lastname,
            "username": self.username,
            "password": self.password
        }

        Postmanager.register_on_platform(payload)

    def login_on_platform(self):
        payload = {
            "username": self.username,
            "password": self.password
        }

        self.cookie = Postmanager.login_on_platform(payload)

    def create_post(self):
        model = Model()

        previous_posts = Postmanager.get_all_posts_from_user(self.username)

        model.context = Prompts.regular_context_prompt(self.firstname, self.lastname, self.username, self.biography, previous_posts)

        model.prompt = ("Create a new post for your society page. "
                             "Don't make the same post again. Stay in character, this means that your post has to be at least somewhat relatable to who you are. Your post may contain a max of 300 words")

        model.ask_deepseek()

        time = DummyTime.get_time()

        payload = {
            "content": model.response,
            "user": self.username,
            "parent": None,
            "created_at": time
        }

        Postmanager.create_post(payload)

        # Now we need to notify all people that have this person as a favourite person
        self.notify_all_people_subscribed_to_current_person()


    def notify_all_people_subscribed_to_current_person(self):
        from PeopleManager import PeopleManager # Prevents a circular import

        for i in PeopleManager.all_people:
            if self in i.favourite_people:
                i.notify_new_post(i)


    def pick_interested_people(self):
        from PeopleManager import PeopleManager # Prevents a circular import

        person_item = []
        for i in PeopleManager.all_people:

            # Yes the AI model is actually stupid enough to pick itself as an interested person
            if i.username == self.username:
                continue

            person_item.append(f"Username: {i.username} Biography: {i.biography}")

        model = Model()
        model.context = Prompts.regular_context_prompt(self.firstname, self.lastname, self.username, self.biography, person_item)

        model.prompt = Prompts.interested_people_prompt(person_item)
        model.ask_deepseek()

        for i in model.response.split(","):
            for y in PeopleManager.all_people:

                if i.strip().lower() == y.username.lower() or i.strip().lower() in y.username.lower():
                    self.favourite_people.append(y)


    # This method gets called by another person and notifies the person that there is a new post by person_caller
    def notify_new_post(self, person_caller):

        # We don't always want to reply to a post, so I'll just add a bit of randomness
        if random.random() > self.CHANCE_TO_REPLY_TO_A_POST:
            return

        # The post we want to reply to is the last post made by the person_caller
        post_to_reply_to = json.loads(Postmanager.get_all_posts_from_user(person_caller.username))[-1]

        ai = Model()
        ai.context = Prompts.regular_context_prompt(self.firstname, self.lastname, self.username, self.biography, Postmanager.get_all_posts_from_user(self.username))
        ai.prompt = Prompts.generate_reply_to_post_of_favourite_person(post_to_reply_to, person_caller, self)
        ai.ask_deepseek()

        time = DummyTime.get_time()

        payload = {
            "content": ai.response,
            "user": self.username,
            "parent": post_to_reply_to,
            "created_at": time
        }

