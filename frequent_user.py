# This python file creates a user who have rented books
import random
from database.database_objects import serialize_user, User, get_ebook_pickles
from recommendations import get_top_related_books

def populate_rented_books(user):
    """
    Get a random amount of EBook pickle files and loads them into
    rented_book field of a User object
    :param user:
    :return:
    """
    ebook_pickles = get_ebook_pickles()
    for index in range(0, random.randrange(3, 6)):
        user.rented_books[ebook_pickles[index].isbn] = ebook_pickles[index]



def create_user():
    user = User(username='John',
            password='pw',
            email='john@doe.com',
            dob='1/1/1990')

    populate_rented_books(user)
    return user

print get_top_related_books(create_user())


