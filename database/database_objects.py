import cPickle
import os
from datetime import datetime
import shutil

ACCOUNT_DIR_PATH = os.path.join('database', 'blobs', 'accounts')
EBOOKS_DIR_PATH = os.path.join('database', 'blobs', 'ebooks')
REPORTS_DIR_PATH = os.path.join('database', 'blobs', 'reports')
REVIEWS_DIR_PATH = os.path.join('database', 'blobs', 'reviews')


# Save and load users
def serialize_user(db_object, save_file_name):
    with open(os.path.join(ACCOUNT_DIR_PATH, save_file_name + '.pickle'), 'wb') as out:
        cPickle.dump(db_object, out)


def update_serialized_user(user_instance):
    with open(os.path.join(ACCOUNT_DIR_PATH, user_instance.username + '.pickle'), 'wb') as out:
        cPickle.dump(user_instance, out)


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


def delete_ebook_from_users(isbn):
    try:
        for pickle in os.listdir(ACCOUNT_DIR_PATH):
            if pickle.endswith('.pickle'):
                user = load_serialized_user(pickle[:-7])
                if user.rented_books.get(isbn, None) is not None:
                    del user.rented_books[isbn]
                serialize_user(user, user.username)
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


# Save and load reviews
def serialize_review(db_object, save_file_name):
    with open(os.path.join(REVIEWS_DIR_PATH, save_file_name + '.pickle'), 'wb') as out:
        cPickle.dump(db_object, out)


def load_serialized_review(save_file_name):
    try:
        with open(os.path.join(REVIEWS_DIR_PATH, save_file_name + '.pickle'), 'rb') as input_file:
            return cPickle.load(input_file)
    except IOError:
        return None


def get_report_pickles():
    reports_list = []
    for pickle in os.listdir(REPORTS_DIR_PATH):
        if pickle.endswith('.pickle'):
            report = load_serialized_report(pickle[:-7])
            report.isbn = pickle[:10]
            reports_list.append(report)
    return reports_list


def get_ebook_pickles():
    ebooks_list = []
    for pickle in os.listdir(EBOOKS_DIR_PATH):
        if pickle.endswith('.pickle'):
            book_instance = load_serialized_ebook(pickle[:-7])
            elapsed_time = datetime.now() - book_instance.last_time_read

            if divmod(elapsed_time.total_seconds(), 60) <= (10.0, 0):
                # If elapsed_time is less than 10 minutes

                if len(book_instance.reports) >= 3:
                    # If book has at least 3 reports

                    # TODO: Ensure B points is definitely the uploader's book price
                    book_instance.uploader.credits -= (book_instance.reward_amount + 100)
                    update_serialized_user(book_instance.uploader)

                    os.remove(os.path.join(EBOOKS_DIR_PATH, pickle))
                    os.remove(os.path.join(EBOOKS_DIR_PATH, pickle[:-7] + '.pdf'))

                else:
                    ebooks_list.append(book_instance)  # -7 to truncate file ending
            else:
                # If elapsed_time is more than 10 minutes, delete it and subtract 5 points from the uploader
                book_instance.uploader.credits -= 5
                update_serialized_user(book_instance.uploader)
                os.remove(os.path.join(EBOOKS_DIR_PATH, pickle))
                os.remove(os.path.join(EBOOKS_DIR_PATH, pickle[:-7] + '.pdf'))
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
        self.reported_books = []  # Make sure to store EBooks objects
        self.reviewed_books = []  # Make sure to store EBooks objects
        self.infractions = {}
        self.currently_reading = None  # Stores an EBook obj
        self.default_pdf_reader = None
        self.is_blacklisted = False

    @property
    def __unicode__(self):
        return self.username

    def upload(self, ebook, username):
        self.uploaded_books.append(ebook)
        ebook.uploader = username


class EBook(object):
    def __init__(self, title, author, genre, isbn, price, summary, uploader, cover_img, book_text, rating=0,
                 approved=False, reward_amount=0):
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

        self.reward_amount = reward_amount
        self.reports = []
        self.reviews = []
        self.rating = rating
        self.history = []
        self.approved = approved

        self.total_seconds = 0.0
        self.count_seconds = 0

        self.last_time_read = datetime.now()

    @property
    def __unicode__(self):
        return self.isbn

    def add_report(self, report):
        """
        :param report: Report object
        :return:
        """
        self.reports.append(report)

    def add_review(self, review):
        self.reviews.append(review)

    def add_seconds(self, seconds):
        self.total_seconds += seconds

    def reset_count_seconds(self):
        self.count_seconds = 0

    def update_last_time_read(self):
        self.last_time_read = datetime.now()


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
        self.total_seconds = 0.0
        self.count_seconds = 0

    def add_seconds(self, seconds):
        self.total_seconds += seconds

    def reset_count_seconds(self):
        self.count_seconds = 0


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


class Review(object):
    def __init__(self, reviewer, review):
        """
        Class definition for a Report object
        :param reviewer: str
        :param review: str
        """
        self.time_stamp = datetime.now()
        self.reviewer = load_serialized_user(reviewer)
        self.review = review
