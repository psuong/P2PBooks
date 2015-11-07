# This file is used to contain a datastructure of all books
import database_objects

class MasterDict(object):
    def __init__(self, user):
        master_dict = {
        "Top" : [],
        "Kids": [],
        "Adventure": [],
        "Education": [],
        "DIY": [],
        "Romance": [],
        "Comedy": [],
        "Fantasy:" [],
        "Biography:" [],
        "History:" [],
        "Magazine": [],
        "Religion": [],
        "Sport": []
        }
        self.user = database_objects.load_user(user)
    """
        populate_dict updates the MasterDict depending on the Category/Genre
    """

    def populate_dict(self):
        pass
