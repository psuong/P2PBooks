import cPickle
import os
from datetime import datetime

ACCOUNT_DIR_PATH = os.path.join('database', 'blobs', 'accounts')


# Save and load users
def serialize_user(db_object, save_file_name):
    with open(os.path.join(ACCOUNT_DIR_PATH, save_file_name + '.pickle'), 'wb') as out:
        cPickle.dump(db_object, out)


def load_serialized_user(save_file_name):
    try:
        with open(os.path.join('database', 'blobs', 'accounts', save_file_name + '.pickle'), 'rb') as input_file:
            return cPickle.load(input_file)
    except IOError:
        return None


# Save and load ebooks
def serialize_ebook(db_object, save_file_name):
    with open(os.path.join('database', 'blobs', 'ebooks', save_file_name + '.pickle'), 'wb') as out:
        cPickle.dump(db_object, out)


def load_serialized_ebook(save_file_name):
    try:
        with open(os.path.join('database', 'blobs', 'ebooks', save_file_name + '.pickle'), 'rb') as input_file:
            return cPickle.load(input_file)
    except IOError:
        return None


# Fill in dictionary, [Key=Genre; Value = Wrapper_Obj]
# Might have to move into a different file


class User(object):
    def __init__(self, username, password, email, dob, p2p_credits=300, group_policy='RU'):
        """
        Class definition for user objects
        :param username: str
        :param password: str
        :param email: str
        :param dob: str
        :param p2p_credits: int
        :param group_policy: str
        :return:
        """
        self.username = username
        self.password = password
        self.email = email
        self.dob = dob
        self.credits = p2p_credits
        self.group_policy = group_policy
        self.uploaded_books = []  # Make sure to store EBooks objects
        self.rented_books = []  # Make sure to store EBooks objects
        self.reported_books = []  # Make sure to store EBooks objects
        self.infractions = []
        self.currently_reading = (None, 0)
        self.default_pdf_reader = None

    @property
    def __unicode__(self):
        return self.username

    def upload(self, ebook, username):
        self.uploaded_books.append(ebook)
        ebook.uploader = username


class EBook(object):
    def __init__(self, title, author, genre, isbn, price, book_text, uploader, file_location, rating=0):
        """
        Class definition for a EBook object
        :param title: str
        :param author: str
        :param genre: list
        :param isbn: str
        :param price: int
        :param book_text: str
        :param uploader: str
        :param rating: int
        :param file_location: str
        :return:
        """
        self.uploader = uploader
        self.title = title
        self.author = author
        self.genres = genre
        self.isbn = isbn
        self.price = price
        self.book_text = book_text
        self.approved = False
        self.current_page = 0
        self.total_pages = 1.0
        self.checked_out_time = None
        self.return_time = None
        self.paused_time = None
        self.reports = []
        self.rating = rating
        self.file_location = file_location

    @property
    def __unicode__(self):
        return self.isbn

    @property
    def progress(self):
        return self.current_page / self.total_pages

    def report(self, report):
        """
        :param report: Report object
        :return:
        """
        self.reports.append(report)


class Report(object):
    def __init__(self, reporter, reason, comment):
        """
        Class definition for a Report object
        :param reporter: str
        :param reason: str
        :param comment: str
        """
        self.time_stamp = datetime.now()
        self.reporter = load_serialized_user(reporter)
        self.reason = reason
        self.comment = comment

    @property
    def __unicode__(self):
        return self.reason + " report sent by " + self.reporter.__unicode__ + " was created at " + str(self.time_stamp)
