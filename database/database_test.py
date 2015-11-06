from database import database_objects

# Create your DB object

# TEST Scenario 1 -----------------------------------------------------------------------------------------
# Create user md
md = database_objects.Users('md', 'mdrizzle', 'm@mdogy.net', 22, '07/30/1993', 30)

# Create ebook one_punch_man
one_punch_man = database_objects.EBooks("One-Punch Man, Vol. 1", "One", "Manga", "1421585642", "5", "Some text")

# md uploads one_punch_man
md.upload(one_punch_man)

# Create user chris
chris = database_objects.Users('Chris', 'passw0rd', 'cyang001@citymail.cuny.edu', 20, '01/26/1995', 30)

# Chris reports one_punch_man
one_punch_man.add_report('Chris', 'Copyright Violation', 'DID YOU TORRENT THIS???')



# Save the object, preferably just call the __unicode__ property as the save filename
database_objects.save_object(md, md.__unicode__)
database_objects.save_object(chris, chris.__unicode__)
database_objects.save_object(one_punch_man, one_punch_man.__unicode__)


# Let's retrieve it
is_this_md = database_objects.load_object('md')
is_this_chris = database_objects.load_object('Chris')
is_this_one_punch_man = database_objects.load_object("1421585642")

for books in is_this_md.uploaded_books:
    print books.title

print is_this_one_punch_man.reports['Chris']


