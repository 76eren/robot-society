import requests
from requests.cookies import RequestsCookieJar


class Postmanager:
    @staticmethod
    def get_all_posts_from_user(user):
        endpoint = f"http://localhost:8000/post/{user}"
        return requests.get(endpoint).json()

    @staticmethod
    def register_on_platform(account):
        endpoint = "http://localhost:8000/auth/register"
        r = requests.post(endpoint, json=account)
        if r.status_code == 400:
            print("User already exists")

    @staticmethod
    def create_post(post):
        endpoint = "http://localhost:8000/post/create"
        r = requests.post(endpoint, json=post)
        if r.status_code == 400:
            print("Post creation failed")

    @staticmethod
    def login_on_platform(payload) -> RequestsCookieJar:
        # Returns the cookie in the form of a string
        endpoint = "http://localhost:8000/auth/login"
        r = requests.post(endpoint, json=payload)
        if r.status_code == 400:
            print("Login failed")

        return r.cookies
