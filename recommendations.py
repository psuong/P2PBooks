from database.database_objects import load_serialized_ebook, get_ebook_pickles, EBOOKS_DIR_PATH


def sort_top_rated(pickle_list):
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


def sort_most_read_books(pickle_list):
    """
    Checks the buy count field in EBook and gets the most bought books
    :param pickle_list: list of EBooks
    :return: sorted list of EBooks
    """
    for index in range(0, len(pickle_list)):
        current_book = pickle_list[index]
        position = index

        while position > 0 and pickle_list[position - 1].buy_count < current_book.buy_count:
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
    top_books = sort_top_rated(pickle_files)
    return top_books[0:5]


def get_top_related_books(user_instance):
    """
    Gets at most 5 books that are similar to the one the reader read before.
    :param user_instance: User
    :return: list
    """
    #if not bool(user_instance.rented_books):
    pass

def get_most_read_books():
    pickle_files = get_ebook_pickles()
    most_read = sort_most_read_books(pickle_files)
    return most_read


for book in get_most_read_books():
    print book.title + " :" + str(book.buy_count)