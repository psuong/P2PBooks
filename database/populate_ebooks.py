import os
from database_objects import EBook, serialize_ebook

PDF_DIR_PATH = os.path.join('database', 'blobs', 'ebooks', 'pdf')
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

USER_LIST = ["Chris",
             "MD",
             "Porrith",
             "Fioger"]

init_ISBN = 1000000000
count = 1

for pdf in os.listdir(PDF_DIR_PATH):
    if count < len(GENRE_LIST):
        break

    if pdf.endswith('.pdf'):
        serialize_ebook(EBook(title=(pdf[:-4]),
                              author="Author#" + count,
                              genre=GENRE_LIST[count],
                              price=count,
                              uploader=USER_LIST[count % 4],
                              ) , init_ISBN, pdf)
        init_ISBN += 1
        count += 1

