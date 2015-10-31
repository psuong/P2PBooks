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

