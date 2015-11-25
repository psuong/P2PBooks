import os
from database.database_objects import EBook, serialize_ebook, load_serialized_user
from models.main_model import convert_pdf_to_txt


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
lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel massa non sem tristique condimentum.
Nullam egestas nibh nibh, nec gravida nunc pharetra nec. Nullam accumsan facilisis quam sed laoreet. Nam lorem nisi,
mattis eget justo eu, mattis congue arcu. Aenean vitae urna at justo ultrices congue at eget sem. Suspendisse sed
justo quis enim varius congue. Maecenas venenatis aliquam nulla et congue. Nulla sit amet pellentesque dui. Fusce
tempus massa et dui tempor iaculis."""

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
                              summary=lorem,
                              cover_img='',
                              isbn=str(init_ISBN),
                              book_text=convert_pdf_to_txt(PDF_DIR_PATH+"\\"+pdf)),
                        str(init_ISBN),
                        os.path.join(PDF_DIR_PATH, pdf))
        user_count += 1
        if user_count == len(user_list):
            user_count = 0
        init_ISBN += 1
        count += 1
