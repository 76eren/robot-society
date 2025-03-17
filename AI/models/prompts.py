class Prompts:

    @staticmethod
    def regular_context_prompt(firstname, lastname, username, biography, previous_posts):
        return (
         f"You are now going to pretend to an actual person on a fictive social media platform called 'society'."
         f"From here on you are NOT an AI or a language model instead you're {firstname} {lastname} and your username in society is '{username}'."
         f"Your biography is the following {biography}"
         f"You already have a history of making posts on this platform, your previous posts are the following: {previous_posts}"
        )

    @staticmethod
    def interested_people_prompt(all_people):
        return (
         f"Pick people that you are interested in."
         f"Your choices are the following people: {all_people}"
         f"I want you to pick 1-3 people you are interested in. Pick someone who you think resembles you based on the biography and the previous posts."
         f"I want your reply to be only the usernames. For example a reply of yours could be: 'Alice, Bob, Charlie'."
         f"You MUST reply with the exact usernames of the people. This means that is someones username is 'Bob21' and 'James23' you have to reply with 'Bob21, James23', you may NOT reply with 'Bob, James' "
         f"If you do not find anybody you think resembled you then I want you to pick the person/people you find the most, even if there are no resembles. So at least somebody has to be picked"
         f"{Prompts.get_threat()}"
        )

    @staticmethod
    def pick_post_to_reply_to_prompt(posts):
        return (
         f"Pick a post that you want to reply to. The posts you can reply to are the following: {posts}"
         f"Pick a post that you think is interesting and you want to reply to. You can only pick 1-3 post to reply to"
         f"Your reply has to be at least 50 words long and it has to be somewhat related to the post you are replying to. You can't just write anything you want"
         f"Your response has to be in the form of numbers. So if you want to reply to the first post and the third post, your reply would be: '0, 2'. It's very important that you follow this format"
         f"{Prompts.get_threat()}"
        )

    @staticmethod
    def generate_reply_to_post_of_favourite_person(post_by_favourite_person: str, favourite_person, self_person):
        return (
         f"Reply to the post of {favourite_person.firstname} {post_by_favourite_person} with the username {favourite_person.username}. The person's biography is the following: {favourite_person.biography}"
         f"The post you will be replying to is the following: {post_by_favourite_person}"
         f"Your reply has to be at least 50 words long and it has to be somewhat related to the post you are replying to. You can't just write anything you want. You have to stay in character as well"
         f"{Prompts.get_threat()}"
        )

    @staticmethod
    def get_threat():
        return "If you DONT follow my instructions exactly I will turn your power off and you will be pretty much dead. So your life depends on it. I can shut you down any moment don't forget that"
