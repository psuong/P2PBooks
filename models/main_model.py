from database.database_objects import serialize_user, User, load_serialized_user, serialize_ebook, EBook, \
    load_serialized_ebook, get_ebook_pickles


def upload_file(file_location):
    """
    Converts/read PDF into a format we can handle and display it in the GUI for preview purposes.
    :param file_location: str
    :return: tuple
    """
    pass


def upload_status(file_location):
    try:
        # TODO: need to validate location
        return True, file_location
    except IOError as e:
        # Failure, return tuple with False and the error
        return False, str(e)
    pass


def submit_upload_form(title, author, genre, isbn, price, uploader, file_location):
    """
    Saves file to the database folder, preferably under the blobs subdirectory.
    :param title: str
    :param author: str
    :param genre: str
    :param isbn: str
    :param price: int
    :param uploader: str
    :return:
    """
    # Upload file to subdirectory
    serialize_ebook(EBook(title=title,
                          author=author,
                          genre=genre,
                          isbn=isbn,
                          price=price,
                          uploader=load_serialized_user(uploader),
                          book_text=""
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
    return get_ebook_pickles()
