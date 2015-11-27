# This python file creates a user who have rented books
import random
from database.database_objects import serialize_user, User


def populate_rented_books(user):
    """
    Get a random amount of EBook pickle files and loads them into
    rented_book field of a User object
    :param user:
    :return:
    """
    pass


def create_user():
    user = User(username='John',
            password='pw',
            email='john@doe.com',
            dob='1/1/1990')

