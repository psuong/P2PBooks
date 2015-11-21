import sys
import database_objects
#from database import database_objects
import unittest, logging

class TestDatabaseObjects(unittest.TestCase):

    def test_scenario_1(self):
        # TEST Scenario 1 -----------------------------------------------------------------------------------------
        log = logging.getLogger("test_scenario_1")

        # Create user md
        md = database_objects.User('MD', 'mdrizzle', 'm@mdogy.net', 22, '07/30/1993', 30)
        # Save the object, preferably just call the __unicode__ property as the save filename
        database_objects.serialize_user(md, md.__unicode__)

        # Create ebook
        one_punch_man = database_objects.EBook("One-Punch Man, Vol. 1", "One", "Manga", "1421585642", "5", "Some text")
        database_objects.serialize_ebook(one_punch_man, one_punch_man.__unicode__)

        # md uploads ebook
        md.upload(one_punch_man, md.username)
        database_objects.serialize_user(md, md.__unicode__)

        # Create user chris
        chris = database_objects.User('Chris', 'passw0rd', 'cyang001@citymail.cuny.edu', 20, '01/26/1995', 30)
        database_objects.serialize_user(chris, chris.__unicode__)

        # chris reports md's ebook
        one_punch_man.report(database_objects.Report('Chris', 'Copyright Violation', 'DID YOU TORRENT THIS???'))
        database_objects.serialize_ebook(one_punch_man, one_punch_man.__unicode__)

        # Let's retrieve it
        is_this_md = database_objects.load_serialized_user('md')
        is_this_chris = database_objects.load_serialized_user('Chris')
        is_this_one_punch_man = database_objects.load_serialized_ebook("1421585642")

        #check if upload function assigned the uploader
        is_this_uploader_md = is_this_one_punch_man.uploader
        self.assertEquals(is_this_uploader_md, md.username)

        # Log the information
        #log.info(is_this_md.__unicode__ + ": %r", vars(is_this_md))
        #self.assertEquals(is_this_md.uploaded_books[0].title, "One-Punch Man, Vol. 1")


        #log.info(is_this_chris.__unicode__ + ": %r", vars(is_this_chris))

        #log.info(is_this_one_punch_man.__unicode__ + ": %r", vars(is_this_one_punch_man))
        #log.info(is_this_one_punch_man.__unicode__ + " reports: " + is_this_one_punch_man.reports[0].__unicode__)

        #log.info(is_this_uploader_md.__unicode__)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("test_scenario_1").setLevel( logging.DEBUG )
    unittest.main()
