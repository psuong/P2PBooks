# This script creates a blacklisted user.
from database.database_objects import serialize_user, User
from models.main_model import check_infractions


def populate_infractions(user_instance):
    infractions = user_instance.infractions
    infraction_reasons = [
        'Illegal Copy',
        'Inappropriate Content'
    ]
    for index in range(0, 2):
        infractions[infraction_reasons[index]] = "Reason here"


def create_user():
    user = User('Doe', 'pw', 'doe@gmail.com', '1/1/1980')
    populate_infractions(user)
    check_infractions(user)
    return user


serialize_user(create_user(), create_user().username)
