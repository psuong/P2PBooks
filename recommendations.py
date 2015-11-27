from database.database_objects import load_serialized_ebook, get_ebook_pickles, EBOOKS_DIR_PATH
import random

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


def get_most_read_books():
    """
    Returns the top 5 most read/purchased books
    :return: list
    """
    pickle_files = get_ebook_pickles()
    most_read = sort_most_read_books(pickle_files)
    return most_read[0:5]


def get_genre_frequency(user_instance):
    """

    :param user_instance: User Object
    :return: list of genre
    """
    genre_frequency_dict = {
        "Kids": 0,
        "Adventure": 0,
        "Education": 0,
        "DIY": 0,
        "Romance": 0,
        "Comedy": 0,
        "Fantasy": 0,
        "Biography": 0,
        "History": 0,
        "Magazine": 0,
        "Religion": 0,
        "Sports": 0
    }

    genre_list = []

    for key, value in user_instance.rented_books.iteritems():
        genre_frequency_dict[value.genre] += 1

    frequency = 0
    for key, value in genre_frequency_dict.iteritems():
        if value >= frequency:
            genre_list.append(key)
            frequency = value
    return genre_list


def get_top_related_books(user_instance):
    """
    Gets at most 5 books that are similar to the one the reader read before.
    :param user_instance: User
    :return: list
    """
    if not bool(user_instance.rented_books):
        return get_most_read_books()
    else:
        random_book_genre = get_genre_frequency(user_instance)
        similar_books = []
        for book in get_ebook_pickles():
            if book.genre == random_book_genre[random.randrange(0, len(random_book_genre))]:
                # print "Genre: " + str(random_book_genre[random.randrange(0, len(random_book_genre))])
                similar_books.append(book)
            # similar_books.append(book)
        return similar_books
