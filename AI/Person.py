import requests
from AI import Model
import DummyTime

class Person:
    def __init__(self, firstname, lastname, username, biography):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.biography = biography

        self.register_on_platform()
        self.favourite_people = []

    def register_on_platform(self):
        endpoint = "http://localhost:8000/users/register"
        payload = {"name": self.firstname, "surname": self.lastname, "username": self.username}

        r = requests.post(endpoint, json=payload)

        if r.status_code == 400:
            print("User already exists")

    def get_previous_posts_from_self(self):
        endpoint = f"http://localhost:8000/post/{self.username}"
        return requests.get(endpoint).json()

    def create_post(self):


        model = Model()

        endpoint = "http://localhost:8000/post/create"

        previous_posts = self.get_previous_posts_from_self()
        model.context = (f"You are now going to pretend to an actual person on a fictive social media platform called 'society'."
                              f"From here on you are NOT an AI or a language model instead you're {self.firstname} {self.lastname}. "
                              f"Your biography is the following {self.biography}"
                              f"You already have a history of making posts on this platform, your previous posts are the following: {previous_posts}")

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

        requests.post(endpoint, json=payload)

    def get_complete_timeline(self):
        pass

    def pick_interested_people(self):
        from PeopleManager import PeopleManager # Prevents a circular import

        person_item = []
        for i in PeopleManager.all_people:

            # Yes the AI model is actually stupid enough to pick itself as an interested person
            if i.username == self.username:
                continue

            person_item.append(f"Username: {i.username} Biography: {i.biography}")

        model = Model()
        model.context = (f"You are now going to pretend to an actual person on a fictive social media platform called 'society'."
                              f"From here on you are NOT an AI or a language model instead you're {self.firstname} {self.lastname}. "
                              f"Your biography is the following {self.biography}"
                              f"You already have a history of making posts on this platform, your previous posts are the following: {person_item}")

        model.prompt = (f"Pick people that you are interested in. "
                        f"Your choices are the following people: {person_item} "
                        f"I want you to pick 1-3 people you are interested in. Pick someone who you think resembles you based on the biography and the previous posts. "
                        f"I want your reply to be only the usernames. For example a reply of yours could be: 'Alice, Bob, Charlie'."
                        f"You MUST reply with the exact usernames of the people. This means that is someones username is 'Bob21' and 'James23' you have to reply with 'Bob21, James23', you may NOT reply with 'Bob, James' "
                        f"If you do not find anybody you think resembled you then I want you to pick the person/people you find the most, even if there are no resembles. So at least somebody has to be picked"
                        f"If you DONT follow my instructions exactly I will turn your power off and you will be pretty much dead. So your life depends on it. I can shut you down any moment don't forget that")

        model.ask_deepseek()

        for i in model.response.split(","):
            for y in PeopleManager.all_people:

                if i.strip().lower() == y.username.lower() or i.strip().lower() in y.username.lower():
                    self.favourite_people.append(y)

    def reply_to_posts_of_favourite_people(self):
        pass

    def get_all_posts_from_user(self):
        endpoint = f"http://localhost:8000/post/{self.username}"
        return requests.get(endpoint).json()

    def pick_post_to_reply_to(self):
        pass