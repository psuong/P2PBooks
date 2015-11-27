import cPickle
import os
from datetime import datetime
import shutil

ACCOUNT_DIR_PATH = os.path.join('database', 'blobs', 'accounts')
EBOOKS_DIR_PATH = os.path.join('database', 'blobs', 'ebooks')
REPORTS_DIR_PATH = os.path.join('database', 'blobs', 'reports')


# Save and load users
def serialize_user(db_object, save_file_name):
    with open(os.path.join(ACCOUNT_DIR_PATH, save_file_name + '.pickle'), 'wb') as out:
        cPickle.dump(db_object, out)


def load_serialized_user(save_file_name):
    try:
        with open(os.path.join(ACCOUNT_DIR_PATH, save_file_name + '.pickle'), 'rb') as input_file:
            return cPickle.load(input_file)
    except IOError:
        return None


# Save and load ebooks
def serialize_ebook(db_object, save_file_name, file_location):
    with open(os.path.join('database', 'blobs', 'ebooks', save_file_name + '.pickle'), 'wb') as out:
        cPickle.dump(db_object, out)
    shutil.copy(file_location, os.path.join('database', 'blobs', 'ebooks', save_file_name + '.pdf'))


def update_serialized_ebook(book_instance):
    with open(os.path.join(EBOOKS_DIR_PATH, book_instance.isbn + '.pickle'), 'wb') as out:
        cPickle.dump(book_instance, out)


def load_serialized_ebook(save_file_name):
    try:
        with open(os.path.join(EBOOKS_DIR_PATH, save_file_name + '.pickle'), 'rb') as input_file:
            return cPickle.load(input_file)
    except IOError:
        return None


# Save and load reports
def serialize_report(db_object, save_file_name):
    with open(os.path.join(REPORTS_DIR_PATH, save_file_name + '.pickle'), 'wb') as out:
        cPickle.dump(db_object, out)


def load_serialized_report(save_file_name):
    try:
        with open(os.path.join(REPORTS_DIR_PATH, save_file_name + '.pickle'), 'rb') as input_file:
            return cPickle.load(input_file)
    except IOError:
        return None


def get_ebook_pickles():
    ebooks_list = []
    for pickle in os.listdir(EBOOKS_DIR_PATH):
        if pickle.endswith('.pickle'):
            ebooks_list.append(load_serialized_ebook(pickle[:-7]))  # -7 to truncate file ending
    return ebooks_list


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
        self.rented_books = {}  # Make sure to store EBooks objects
        self.infractions = {}
        self.currently_reading = None # Stores an Ebook obj related
        self.default_pdf_reader = None

    @property
    def __unicode__(self):
        return self.username

    def upload(self, ebook, username):
        self.uploaded_books.append(ebook)
        ebook.uploader = username


class EBook(object):
    def __init__(self, title, author, genre, isbn, price, summary, uploader, cover_img, book_text, rating=0):
        """
        Class definition for a EBook object
        :param title: str
        :param author: str
        :param genre: list
        :param isbn: str
        :param price: int
        :param summary: str
        :param uploader: User
        :param rating: int
        :param cover_img: str
        :param book_text: str
        :return:
        """
        self.uploader = uploader
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn
        self.price = price
        self.summary = summary
        self.cover_img = cover_img
        self.book_text = book_text
        self.buy_count = 0

        self.approved = False
        self.reports = []
        self.rating = rating
        self.history = []

    @property
    def __unicode__(self):
        return self.isbn

    def add_report(self, report):
        """
        :param report: Report object
        :return:
        """
        self.reports.append(report)


class PurchasedEBook(object):
    def __init__(self, username, isbn, checked_out_time, length_on_rent, paused_time, total_time_bought):
        """

        :param username: str
        :param isbn: EBook
        :param checked_out_time: datetime
        :param length_on_rent: int
        :param paused_time: datetime
        :param total_time_bought: int
        :return:
        """
        self.isbn = isbn
        self.checked_out_time = checked_out_time
        self.length_on_rent = length_on_rent
        self.paused_time = paused_time
        self.total_time_bought = total_time_bought


class Report(object):
    def __init__(self, reporter, reason, description):
        """
        Class definition for a Report object
        :param reporter: str
        :param reason: str
        :param description: str
        """
        self.time_stamp = datetime.now()
        self.reporter = load_serialized_user(reporter)
        self.reason = reason
        self.description = description

    @property
    def __unicode__(self):
        return self.reason + " report sent by " + self.reporter.__unicode__ + " was created at " + str(self.time_stamp)
