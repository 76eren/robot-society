import requests


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
    def create_post(post, cookies):
        endpoint = "http://localhost:8000/post/create"

        # Sets the cookie header
        headers = {
            "Cookie": cookies
        }

        r = requests.post(endpoint, json=post, headers=headers)
        if r.status_code == 400:
            print("Post creation failed")

    @staticmethod
    def login_on_platform(payload):
        endpoint = "http://localhost:8000/auth/login"
        r = requests.post(endpoint, json=payload)

        if r.status_code == 400:
            print("Login failed")
            return None

        unsanitised_cookie = r.headers.get("Set-Cookie", "")
        return unsanitised_cookie.split("; HttpOnly")[0]

