import cPickle


def save_user(db_object, save_file_name):
    with open('blobs\\accounts\\' + save_file_name + '.pickle', 'wb') as out:
        cPickle.dump(db_object, out)


def load_user(save_file_name):
    with open('blobs\\accounts\\' + save_file_name + '.pickle', 'rb') as input_file:
        return cPickle.load(input_file)


class Users(object):
    def __init__(self, username, password, email, age, dob, p2p_credits, group_policy='RU'):
        """
        Class definition for user objects
        :param username: str
        :param password: str
        :param email: str
        :param age: int
        :param dob: str
        :param p2p_credits: int
        :param group_policy: str
        :return:
        """
        self.username = username
        self.password = password
        self.email = email
        self.age = age
        self.dob = dob
        self.credits = p2p_credits
        self.group_policy = group_policy
        self.uploaded_books = [] # Make sure to store EBooks objects
        self.rented_books = []  # Make sure to store EBooks objects
        self.reported_books = []  # Make sure to store EBooks objects
        self.infractions = []
        self.currently_reading = (None, 0)
        self.default_pdf_reader = None

    @property
    def __unicode__(self):
        return self.username

    def upload(self, Ebook):
        self.uploaded_books.append(Ebook)

class EBooks(object):
    def __init__(self, username, title, author, genres, isbn, price, book_text):
        """
        Class definition for a EBook object
        :param username: str
        :param title: str
        :param author: str
        :param genres: list
        :param isbn: str
        :param price: int
        :param book_text: str
        :return:
        """
        self.user = load_user(username)
        self.title = title
        self.author = author
        self.genres = genres
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

    @property
    def __unicode__(self):
        return self.isbn

    @property
    def progress(self):
        return self.current_page / self.total_pages


class Reports(object):
    def __init__(self, username, reason, comment, title):
        """
        Class definition for a Report object
        :param username: str
        :param reason: str
        :param comment: str
        :param title: str
        """
        self.time_stamp = None
        self.user = load_user(username)
        self.reason = reason
        self.comment = comment
        self.eBook = title

    @property
    def __unicode__(self):
        return self.reason + " report sent by: " + self.user + " for " + self.eBook

    def add_report(self, username, reason, comment):
        self.reports[username] = reason + ": " + comment
