from PeopleManager import PeopleManager


def main():
    PeopleManager.seed_people()

    # First all people need to register, if they have already registered the backend will just send back an error which is fine
    for i in PeopleManager.all_people:
        i.register_on_platform()

    # All people now need to login
    for i in PeopleManager.all_people:
        i.login_on_platform()

    # Now all the AI are going to create a single post
    for i in PeopleManager.all_people:
        i.create_post()

    # Now all people are going to pick a person they might be interested in. Earlier a post was made so the AI can get an idea of who the person really is they might be interested in
    for i in PeopleManager.all_people:
        i.pick_interested_people()


    AMOUNT_OF_POSTS_PER_PERSON = 1

    for y in range(AMOUNT_OF_POSTS_PER_PERSON):
        for i in PeopleManager.all_people:
            i.create_post()


if __name__ == "__main__":
    main()


