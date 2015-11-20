from database.database_objects import serialize_user, User, load_serialized_user


def upload_file(file_location):
    """
    Converts/read PDF into a format we can handle and display it in the GUI for preview purposes.
    :param file_location: str
    :return: tuple
    """
    pass


def submit_file(file_location):
    """
    Saves file to the database folder, preferably under the blobs subdirectory.
    :param file_location: str
    :return: tuple
    """
    try:
        # Upload file to subdirectory
        pass
    except IOError as e:
        # Failure, return tuple with False and the error
        return False, str(e)
    pass


def read_book():
    return True


def pause_book():
    return True


def register_user(username, password, email, dob):
    # Check if username or email already exists
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
