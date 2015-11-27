import os
import datetime
from database.database_objects import serialize_user, User, load_serialized_user, serialize_ebook, EBook, \
    load_serialized_ebook, get_ebook_pickles, serialize_report, Report, load_serialized_report, \
    update_serialized_ebook, Review, serialize_review, load_serialized_review
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

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
        book_dict[book.genre].append(book)

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
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=2, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text.lower()


def submit_report_form(reporter, reason, description, book_instance):
    report_name = book_instance.isbn + "-" + str(datetime.datetime.now()).replace(":", "-")
    serialize_report(Report(reporter=reporter,
                            reason=reason,
                            description=description
                            ), report_name)
    add_report_to_book(book_instance, report_name)


def add_report_to_book(book_instance, report_name):
    book_instance.add_report(load_serialized_report(report_name))
    serialize_ebook(book_instance, book_instance.isbn, os.path.join(EBOOKS_DIR_PATH, book_instance.isbn + ".pickle"))


def submit_review_rate_form(book_instance, reviewer, rating, review):
    review_name = book_instance.isbn + "-" + str(datetime.datetime.now()).replace(":", "-")
    serialize_review(Review(reviewer=reviewer,
                            review=review), review_name)
    book_instance.add_review(load_serialized_review(review_name))

    book_instance.rating = (book_instance.rating*book_instance.count_seconds
                            + load_serialized_user(reviewer).rented_books[book_instance.isbn].count_seconds*rating)/\
                           book_instance.total_seconds
    print book_instance.rating
    book_instance.count_seconds = book_instance.total_seconds

    update_serialized_ebook(book_instance)
