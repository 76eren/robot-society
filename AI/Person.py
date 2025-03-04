import requests
import DummyTime
from AI import Model


class Person:
    def __init__(self, firstname, lastname, username, biography):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.biography = biography

        self.register_on_platform()

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
        endpoint = "http://localhost:8000/post/all"
        pass

    def pick_interested_people(self):
        # This will ask the AI model to pick people that this person would be interested in
        # After that the current person will reply to the posts of the people that the AI picked

        pass
