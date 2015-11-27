import os
import datetime
from database.database_objects import serialize_user, User, load_serialized_user, serialize_ebook, EBook, \
    load_serialized_ebook, get_ebook_pickles, serialize_report, Report, load_serialized_report, get_report_pickles, \
    REPORTS_DIR_PATH, delete_ebook_from_users, update_serialized_ebook, Review, serialize_review, \
    load_serialized_review, update_serialized_user
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from fuzzywuzzy import process
from recommendations import get_top_rated_books

ACCOUNT_DIR_PATH = os.path.join('database', 'blobs', 'accounts')
EBOOKS_DIR_PATH = os.path.join('database', 'blobs', 'ebooks')


def submit_upload_form(title, author, genre, isbn, price, uploader, summary, cover_img, file_location):
    """
    Saves file to the database folder, preferably under the blobs subdirectory.
    :param title: str
    :param author: str
    :param genre: str
    :param isbn: str
    :param price: int
    :param uploader: str
    :param summary: str
    :param cover_img: str
    :param file_location: str
    :return:
    """

    # Upload file to subdirectory
    serialize_ebook(EBook(title=title,
                          author=author,
                          genre=genre,
                          isbn=isbn,
                          price=price,
                          uploader=load_serialized_user(uploader),
                          summary=summary,
                          cover_img=cover_img,
                          book_text=convert_pdf_to_txt(file_location)
                          ), isbn, file_location)


def read_book():
    return True


def pause_book():
    return True


def register_user(username, password, email, dob):
    # TODO: Check if username or email already exists
    serialize_user(User(username=username,
                        password=password,
                        email=email,
                        dob=dob),
                   username)


def login_user(username, password):
    user = load_serialized_user(username)
    if user is not None:
        if user.password == password:
            return user
        else:
            return None
    else:
        return None


def catalogue_loader():
    book_dict = {
        "TOP": [],
        "Kids": [],
        "Adventure": [],
        "Education": [],
        "DIY": [],
        "Romance": [],
        "Comedy": [],
        "Fantasy": [],
        "Biography": [],
        "History": [],
        "Magazine": [],
        "Religion": [],
        "Sports": []
    }
    for book in get_ebook_pickles():
        if book.approved:
            book_dict[book.genre].append(book)

    for book in get_top_rated_books():
        book_dict["TOP"].append(book)

    return book_dict


def get_book_instance(isbn):
    return load_serialized_ebook(isbn)


def checkout_ebook(user_object, isbn):
    pass


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=1, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text.lower()


def submit_report_form(reporter, reason, description, book_instance):
    report_name = book_instance.isbn + "-" + str(datetime.datetime.now()).replace(":", "-")
    serialize_report(Report(reporter=reporter.username,
                            reason=reason,
                            description=description
                            ), report_name)
    add_report_to_book(book_instance, report_name)

    reporter.reported_books.append(book_instance)
    update_serialized_user(reporter)


def add_report_to_book(book_instance, report_name):
    book_instance.add_report(load_serialized_report(report_name))
    serialize_ebook(book_instance, book_instance.isbn, os.path.join(EBOOKS_DIR_PATH, book_instance.isbn + ".pickle"))


def search(query):
    try:
        query = int(query)
        book = load_serialized_ebook(str(query))
        if book is not None:
            return book
        else:
            return {}
    except ValueError:
        books = get_ebook_pickles()
        result_set_tuple = process.extract(query=query,
                                           choices=[book.title for book in books],
                                           limit=5)
        found_book_instance = []
        for title in result_set_tuple:
            for book in books:
                if book.title == title[0]:
                    found_book_instance.append(book)
        return found_book_instance


def not_approved_ebooks():
    book_list = get_ebook_pickles()
    not_approved_book_list = []
    for book in book_list:
        if not book.approved:
            not_approved_book_list.append(book)
    return not_approved_book_list


def reports_list():
    return get_report_pickles()


def report_info(isbn_datetime):
    return load_serialized_report(isbn_datetime)


def add_user_credits(username, credit):
    user = load_serialized_user(username)
    user.credits += credit
    serialize_user(user, username)


def remove_user_credits(username, credit):
    user = load_serialized_user(username)
    user.credits -= credit
    serialize_user(user, username)


def remove_ebook(isbn):
    os.remove(os.path.join(EBOOKS_DIR_PATH, isbn + '.pdf'))
    os.remove(os.path.join(EBOOKS_DIR_PATH, isbn + '.pickle'))


def remove_ebook_with_infraction(isbn, infraction_reason, timestamp=None):
    book = load_serialized_ebook(isbn)
    user = load_serialized_user(book.uploader.username)
    user.credits -= book.reward_amount
    user.infractions[isbn + str(datetime.datetime.now())] = infraction_reason
    serialize_user(user, user.username)
    delete_ebook_from_users(isbn)
    os.remove(os.path.join(EBOOKS_DIR_PATH, isbn + '.pdf'))
    os.remove(os.path.join(EBOOKS_DIR_PATH, isbn + '.pickle'))
    if timestamp is not None:
        report = isbn + '-' + timestamp.replace(':', '-')
        os.remove(os.path.join(REPORTS_DIR_PATH, report + '.pickle'))


def check_infractions(user_instance):
    """
    Checks if the # of infractions is greater >= 2
    :param user_instance: User
    :return:
    """
    if len(user_instance.infractions) >= 2:
        user_instance.is_blacklisted = True


def blacklist_book_uploader(isbn):
    book = load_serialized_ebook(isbn)
    user = load_serialized_user(book.uploader.username)
    user.is_blacklisted = True
    serialize_user(user, user.username)

def report_exists(reporter, book_instance):
    for book in reporter.reported_books:
        if book == book_instance:
            return True

    return False

def submit_review_rate_form(book_instance, reviewer, rating, review):
    review_name = book_instance.isbn + "-" + str(datetime.datetime.now()).replace(":", "-")
    serialize_review(Review(reviewer=reviewer.username,
                            review=review), review_name)
    book_instance.add_review(load_serialized_review(review_name))
    reviewer.reviewed_books.append(book_instance)
    update_serialized_user(reviewer)

    book_instance.rating = (book_instance.rating*book_instance.count_seconds
                            + reviewer.rented_books[book_instance.isbn].total_seconds*rating)/\
                           book_instance.total_seconds
    book_instance.count_seconds = book_instance.total_seconds

    update_serialized_ebook(book_instance)


def review_exists(reviewer, book_instance):
    for book in reviewer.reviewed_books:
        if book == book_instance:
            return True

    return False
