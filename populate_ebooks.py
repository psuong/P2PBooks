import os
from database.database_objects import EBook, serialize_ebook, load_serialized_user

PDF_DIR_PATH = os.path.join('database', 'blobs', 'ebooks', 'pdf')
USER_DIR_PATH = os.path.join('database', 'blobs', 'accounts')
EBOOKS_DIR_PATH = os.path.join('database', 'blobs', 'ebooks')

GENRE_LIST = ["Kids",
              "Adventure",
              "Education",
              "DIY",
              "Romance",
              "Comedy",
              "Fantasy",
              "Biography",
              "History",
              "Magazine",
              "Religion",
              "Sports"]

init_ISBN = 1000000000
count, user_count = 0, 0
user_list = []

for user in os.listdir(USER_DIR_PATH):
    if user.endswith('.pickle'):
        user_list.append(load_serialized_user(user[:-7]))

for pdf in os.listdir(PDF_DIR_PATH):
    if count == len(GENRE_LIST):
        break

    if pdf.endswith('.pdf'):
        serialize_ebook(EBook(title=(pdf[:-4]),
                              author="Author#" + str(count),
                              genre=GENRE_LIST[count],
                              price=count,
                              uploader=user_list[user_count],
                              book_text="",
                              isbn=str(init_ISBN)),
                        str(init_ISBN),
                        os.path.join(PDF_DIR_PATH, pdf))
        user_count += 1
        if user_count == len(user_list):
            user_count = 0
        init_ISBN += 1
        count += 1
