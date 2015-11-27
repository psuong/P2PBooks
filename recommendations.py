from database.database_objects import load_serialized_ebook, get_ebook_pickles, EBOOKS_DIR_PATH


def insertion_sort(pickle_list):
    """
    Sorts a list of EBook objects from greatest value to smallest
    :param pickle_list: list
    :return: list
    """
    for index in range(0, len(pickle_list)):
        current_book = pickle_list[index]
        position = index

        while position > 0 and pickle_list[position - 1].rating < current_book.rating:
            pickle_list[position] = pickle_list[position - 1]
            position -= 1

        pickle_list[position] = current_book

    return pickle_list


def get_top_rated_books():
    """
    Returns the top 5 rated books
    :return: list
    """
    pickle_files = get_ebook_pickles()
    top_books = insertion_sort(pickle_files)
    return top_books[0:5]


def get_top_related_books(user_instance):
    """
    Gets at most 5 books that are similar to the one the reader read before.
    :param user_instance: User
    :return: list
    """
    pass
